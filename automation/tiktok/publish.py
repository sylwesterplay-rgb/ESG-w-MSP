"""Fail-closed ESG360 Cloudinary -> Buffer scheduler. Secrets from Actions only."""
import os,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timedelta,time
from zoneinfo import ZoneInfo
import requests
BASE=Path(__file__).resolve().parent
TZ=ZoneInfo("Europe/Warsaw")
ORG="6acd37f788a9ef6b52a7a556"
CHANNEL="6ad1dedb778b240e2f269549"
CLOUD="dvtirowe"
def gql(query,vars=None):
    response=requests.post("https://api.buffer.com",headers={"Authorization":"Bearer "+os.environ["BUFFER_API_KEY"]},json={"query":query,"variables":vars or {}},timeout=45)
    response.raise_for_status();data=response.json()
    if data.get("errors"):raise RuntimeError(str(data["errors"])[:800])
    return data["data"]
def channel_ok():
    query='query($org:OrganizationId!){channels(input:{organizationId:$org}){id name service isDisconnected isLocked}}'
    return any(c["id"]==CHANNEL and c["name"]=="esg360.academy" and c["service"]=="tiktok" and not c["isDisconnected"] and not c["isLocked"] for c in gql(query,{"org":ORG})["channels"])
def posts():
    query='query($org:OrganizationId!,$ids:[ChannelId!]){posts(first:100,input:{organizationId:$org,filter:{channelIds:$ids}}){edges{node{id status dueAt text channelId}} pageInfo{hasNextPage}}}'
    result=gql(query,{"org":ORG,"ids":[CHANNEL]})["posts"]
    if result["pageInfo"]["hasNextPage"]:raise RuntimeError("Pagination required; fail-closed before scheduling")
    return [x["node"] for x in result["edges"]]
def cloud_upload(path,ident):
    url=f"https://api.cloudinary.com/v1_1/{CLOUD}/video/upload"
    with path.open("rb") as fh:
        resp=requests.post(url,data={"upload_preset":os.environ["CLOUDINARY_UPLOAD_PRESET"],"folder":"esg360_tiktok","public_id":ident,"overwrite":"false"},files={"file":(path.name,fh,"video/mp4")},timeout=180)
    resp.raise_for_status(); result=resp.json()
    video=result["secure_url"]
    if result.get("resource_type")!="video" or not video.startswith(f"https://res.cloudinary.com/{CLOUD}/video/upload/"):
        raise RuntimeError("Unexpected Cloudinary response")
    return video
def schedule(episode,video,due):
    mutation='''mutation($input:CreatePostInput!){createPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId schedulingType}} ... on InvalidInputError{message} ... on LimitReachedError{message} ... on RestProxyError{message} ... on UnexpectedError{message}}}'''
    inp={"channelId":CHANNEL,"mode":"customScheduled","dueAt":due.isoformat(timespec="seconds"),"schedulingType":"automatic","text":episode["caption"],"assets":[{"video":{"url":video,"metadata":{"title":episode["title"],"thumbnailOffset":0}}}]}
    result=gql(mutation,{"input":inp})["createPost"]
    if result["__typename"]!="PostActionSuccess":raise RuntimeError("Buffer rejected scheduling "+str(result))
    return result["post"]
def verify(id,due):
    q='query($id:PostId!){post(input:{id:$id}){id status dueAt channelId schedulingType assets{type}}}'
    item=gql(q,{"id":id})["post"]
    assert item["status"]=="scheduled" and item["channelId"]==CHANNEL and item["schedulingType"]=="automatic"
    assert any(a["type"]=="video" for a in item["assets"])
    assert datetime.fromisoformat(item["dueAt"].replace("Z","+00:00"))==due
    return item
def main():
    if not os.getenv("BUFFER_API_KEY") or not os.getenv("CLOUDINARY_UPLOAD_PRESET"):raise RuntimeError("GitHub secrets missing")
    if not channel_ok():raise RuntimeError("Wrong TikTok channel, stopping")
    now=datetime.now(TZ)
    existing=posts()
    episodes=json.loads((BASE/"episodes.json").read_text())
    for ep in episodes:
        due=datetime.combine(datetime.fromisoformat(ep["date"]).date(),time(18,0),TZ)
        if due<=now+timedelta(minutes=60):continue
        if any(p["text"]==ep["caption"] and p["status"] in ("scheduled","sending","sent") for p in existing):
            print("SKIP duplicate "+ep["id"]);continue
        if any(p["dueAt"] and datetime.fromisoformat(p["dueAt"].replace("Z","+00:00"))==due.astimezone(ZoneInfo("UTC")) and p["status"] in ("scheduled","sending","sent") for p in existing):
            print("SKIP slot occupied "+ep["id"]);continue
        os.environ["EPISODE_ID"]=ep["id"]
        subprocess.run([sys.executable,str(BASE/"render.py")],check=True)
        video=cloud_upload(BASE/"generated"/(ep["id"]+".mp4"),ep["id"])
        post=schedule(ep,video,due)
        confirmed=verify(post["id"],due.astimezone(ZoneInfo("UTC")))
        print(json.dumps({"status":"SCHEDULED_VERIFIED","postId":confirmed["id"],"dueAt":confirmed["dueAt"],"videoUrl":video},ensure_ascii=False))
        return
    print("NO_NEW_EPISODE")
if __name__=="__main__":main()

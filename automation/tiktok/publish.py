"""Fail-closed ESG360 Cloudinary -> Buffer scheduler. Secrets from Actions only."""
import os,json,subprocess,sys
from pathlib import Path
from datetime import datetime,timedelta,time
from zoneinfo import ZoneInfo
import requests
from social_guard import assert_tiktok_target, assert_tiktok_queue, SecurityGateError
BASE=Path(__file__).resolve().parent
TZ=ZoneInfo("Europe/Warsaw")
ORG="6acd37f788a9ef6b52a7a556"
CHANNEL="6ad1dedb778b240e2f269549"
CLOUD="dvtirowe"
LINKEDIN="6acd3857778b240e2febc3c1"
def gql(query,vars=None):
    response=requests.post("https://api.buffer.com",headers={"Authorization":"Bearer "+os.environ["BUFFER_API_KEY"]},json={"query":query,"variables":vars or {}},timeout=45)
    response.raise_for_status();data=response.json()
    if data.get("errors"):raise RuntimeError(str(data["errors"])[:800])
    return data["data"]
def channel_ok():
    # Verify ID + org + name + service + account type + exact public link + connection.
    query=f'query{{channels(input:{{organizationId:"{ORG}"}}){{id name organizationId service type externalLink isDisconnected isLocked}}}}'
    try:
        assert_tiktok_target(gql(query)["channels"], CHANNEL)
        return True
    except SecurityGateError as exc:
        print("SOCIAL_GUARD_DENIED: "+str(exc))
        return False
def posts(channel=CHANNEL):
    if channel!=CHANNEL:
        raise SecurityGateError("DENY: this GitHub scheduler may read/write ESG360 TikTok only")
    query=f'query{{posts(first:100,input:{{organizationId:"{ORG}",filter:{{channelIds:["{channel}"]}}}}){{edges{{node{{id status dueAt text channelId schedulingType}}}} pageInfo{{hasNextPage}}}}}}'
    result=gql(query)["posts"]
    if result["pageInfo"]["hasNextPage"]:
        raise SecurityGateError("DENY: incomplete Buffer queue pagination")
    items=[x["node"] for x in result["edges"]]
    assert_tiktok_queue(items, CHANNEL)
    return items
def cloud_upload(path,ident):
    url=f"https://api.cloudinary.com/v1_1/{CLOUD}/video/upload"
    with path.open("rb") as fh:
        resp=requests.post(url,data={"upload_preset":os.environ["CLOUDINARY_UPLOAD_PRESET"]},files={"file":(path.name,fh,"video/mp4")},timeout=180)
    if not resp.ok:
        try:
            info=resp.json().get("error",{}).get("message","Unknown Cloudinary error")
        except ValueError:
            info="Non-JSON response from Cloudinary"
        raise RuntimeError(f"Cloudinary upload failed (HTTP {resp.status_code}): {str(info)[:500]}")
    result=resp.json()
    video=result["secure_url"]
    if result.get("resource_type")!="video" or not video.startswith(f"https://res.cloudinary.com/{CLOUD}/video/upload/"):
        raise RuntimeError("Unexpected Cloudinary response")
    return video
def schedule(episode,video,due,channel=CHANNEL):
    if channel!=CHANNEL:
        raise SecurityGateError("DENY: LinkedIn cross-posting and other channels disabled by ACC-SOCIAL-GUARD-01")
    if not channel_ok():
        raise SecurityGateError("DENY: live TikTok identity verification failed")
    mutation='''mutation($input:CreatePostInput!){createPost(input:$input){__typename ... on PostActionSuccess{post{id status dueAt channelId schedulingType}} ... on MutationError{message}}}'''
    inp={"channelId":channel,"mode":"customScheduled","dueAt":due.isoformat(timespec="seconds"),"schedulingType":"automatic","text":episode["caption"],"assets":[{"video":{"url":video,"metadata":{"title":episode["title"],"thumbnailOffset":0}}}]}
    result=gql(mutation,{"input":inp})["createPost"]
    if result["__typename"]!="PostActionSuccess":raise RuntimeError("Buffer rejected scheduling "+str(result))
    return result["post"]
def verify(id,due,channel=CHANNEL):
    if channel!=CHANNEL:
        raise SecurityGateError("DENY: verification target not on TikTok allowlist")
    matching=[p for p in posts(channel) if p["id"]==id]
    if len(matching)!=1:
        raise RuntimeError("Post not found after scheduling")
    item=matching[0]
    if item["status"]!="scheduled" or item["channelId"]!=channel or item["schedulingType"]!="automatic":
        raise RuntimeError("Post status, target or automatic mode is incorrect")
    if datetime.fromisoformat(item["dueAt"].replace("Z","+00:00"))!=due:
        raise RuntimeError("Wrong due date after scheduling")
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
        if any(p["text"]==ep["caption"] for p in existing):
            print("SKIP duplicate "+ep["id"]);continue
        if any(p["dueAt"] and datetime.fromisoformat(p["dueAt"].replace("Z","+00:00"))==due.astimezone(ZoneInfo("UTC")) for p in existing):
            print("SKIP slot occupied "+ep["id"]);continue
        os.environ["EPISODE_ID"]=ep["id"]
        subprocess.run([sys.executable,str(BASE/"render.py")],check=True)
        video=cloud_upload(BASE/"generated"/(ep["id"]+".mp4"),ep["id"])
        post=schedule(ep,video,due)
        confirmed=verify(post["id"],due.astimezone(ZoneInfo("UTC")))
        print(json.dumps({"status":"SCHEDULED_VERIFIED","postId":confirmed["id"],"dueAt":confirmed["dueAt"],"videoUrl":video},ensure_ascii=False))
        # ACC-SOCIAL-GUARD-01: no LinkedIn cross-posting from TikTok Autopilot.
        # Existing LinkedIn posts already scheduled in Buffer/Metricool are untouched.
        print("LINKEDIN_CROSSPOST_DISABLED_BY_POLICY")
        return
    print("NO_NEW_EPISODE")
if __name__=="__main__":main()

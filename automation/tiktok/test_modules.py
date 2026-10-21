"""Validate every ESG360 training module without external APIs or secrets."""
import json, csv, os, subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
episodes=json.loads((BASE/"episodes.json").read_text(encoding="utf-8"))
demos=[x for x in episodes if x.get("demo")]
assert len(demos)==14, f"Expected 14 modules, got {len(demos)}"
assert sorted({x["demo"]["module"] for x in demos})==[str(i).zfill(2) for i in range(1,15)]
assert len({x["date"] for x in episodes})==len(episodes), "Duplicated calendar date"
assert len({x["id"] for x in episodes})==len(episodes), "Duplicated episode ID"
for e in demos:
    dm=e["demo"];keys={r[0] for r in dm["rows"]}
    assert 2<=len(dm["headers"])<=4, e["id"]
    assert 3<=len(dm["steps"])<=5, e["id"]
    assert len(dm["headers"])==len(dm["rows"][0]), e["id"]
    assert all(len(r)==len(dm["headers"]) for r in dm["rows"]), e["id"]
    assert all(st["field"] in keys for st in dm["steps"]), e["id"]
    assert all("PRZYKŁADOWE" in dm["disclaimer"] for _ in [0]), e["id"]
print("VALIDATED",len(demos),"file walkthrough modules, unique dates and field references.")
if "--render-smoke" in sys.argv:
    os.environ["EPISODE_ID"]=demos[0]["id"]
    subprocess.run([sys.executable,str(BASE/"render.py")],check=True)
    video=BASE/"generated"/(demos[0]["id"]+".mp4")
    subprocess.run([sys.executable,str(BASE/"check_media.py"),str(video)],check=True)
    expected=[BASE/"generated"/"demo_files"/(demos[0]["id"]+"_"+s+".csv") for s in ["START","WYPELNIONY"]]
    for p in expected:
        assert p.exists(),p
        with p.open(encoding="utf-8-sig",newline="") as fh:assert len(list(csv.reader(fh,delimiter=";")))>1
    print("RENDER AND CSV SMOKE TEST PASSED",video)

if "--render-all" in sys.argv:
    for i,ep in enumerate(demos,1):
        os.environ["EPISODE_ID"]=ep["id"]
        subprocess.run([sys.executable,str(BASE/"render.py")],check=True)
        video=BASE/"generated"/(ep["id"]+".mp4")
        subprocess.run([sys.executable,str(BASE/"check_media.py"),str(video)],check=True)
        start=BASE/"generated"/"demo_files"/(ep["id"]+"_START.csv")
        filled=BASE/"generated"/"demo_files"/(ep["id"]+"_WYPELNIONY.csv")
        assert start.exists() and filled.exists()
        print("PREVIEW_READY",i,"/",len(demos),ep["demo"]["module"],video,flush=True)
    print("ALL_MODULE_PREVIEWS_READY",len(demos),flush=True)

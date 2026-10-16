"""Check MP4 format and actual audio before upload. Fail closed on error."""
import sys, json, subprocess
if len(sys.argv)!=2:
    raise SystemExit("Usage: check_media.py FILE.mp4")
raw=subprocess.check_output(["ffprobe","-v","error","-show_streams","-of","json",sys.argv[1]],text=True)
streams=json.loads(raw)["streams"]
video=[s for s in streams if s.get("codec_type")=="video"]
audio=[s for s in streams if s.get("codec_type")=="audio"]
if len(video)!=1 or video[0].get("width")!=1080 or video[0].get("height")!=1920:
    raise SystemExit("Video must be 1080x1920")
if not audio or audio[0].get("codec_name")!="aac":
    raise SystemExit("Missing AAC soundtrack")
print("MEDIA VERIFIED: 1080x1920 and AAC audio")

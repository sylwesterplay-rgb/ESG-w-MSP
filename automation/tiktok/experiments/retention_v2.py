"""ESG360 experimental 9:16 retention-first renderer.

Manual/branch-only experiment. NOT connected to Buffer or GitHub scheduling.
Requires Pillow and ffmpeg, no copyrighted audio.
"""
import argparse
import json
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H, FPS = 720, 1280, 12
DARK, CREAM, GOLD, SOFT = (7, 40, 35), (248, 244, 228), (220, 185, 106), (183, 207, 190)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def center(draw, content, top, face, fill, max_width=640, leading=1.1):
    for i, line in enumerate(content.split("\n")):
        bbox = draw.textbbox((0, 0), line, font=face)
        width = bbox[2]-bbox[0]
        if width > max_width:
            raise ValueError("Text outside TikTok safe zone: " + line)
        draw.text(((W-width)//2, top + i*int(face.size*leading)),
                  line, font=face, fill=fill)

def render(ep, output):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not installed")
    beats = ep["beats"]
    if not 3 <= len(beats) <= 7 or not all(1 <= b["duration"] <= 4 for b in beats):
        raise ValueError("Invalid beat timing")
    total = sum(b["duration"] for b in beats)
    if total > 21:
        raise ValueError("Max experiment length is 21 seconds")
    output.parent.mkdir(parents=True, exist_ok=True)
    prefix = output.with_suffix("")
    raw = prefix.with_suffix(".raw.mp4")
    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
           "-f", "rawvideo", "-vcodec", "rawvideo",
           "-s", f"{W}x{H}", "-pix_fmt", "rgb24", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
           "-r", "30", "-movflags", "+faststart", str(raw)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    counts = [round(b["duration"] * FPS) for b in beats]
    frame_count = sum(counts)
    n = 0
    for beat_index, beat in enumerate(beats):
        for j in range(counts[beat_index]):
            fraction = j/max(counts[beat_index]-1, 1)
            t = n/FPS
            im = Image.new("RGB", (W, H), DARK)
            d = ImageDraw.Draw(im)
            cx = int(600 - 28*math.sin(t*1.7))
            cy = int(130 + 20*math.sin(t*1.1))
            for radius in (115, 154, 194):
                d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius),
                          outline=(28, 77, 65), width=3)
            d.rectangle((0, 0, W, 13), fill=GOLD)
            d.text((44, 40), "ESG360 ACADEMY", font=font(BOLD, 25), fill=GOLD)
            d.text((44, 79), "WIEDZA · NARZĘDZIA · WDROŻENIE",
                   font=font(REG, 15), fill=SOFT)
            label = beat["eyebrow"]
            d.rounded_rectangle((44, 278, 44+min(618,20+len(label)*14), 336),
                                radius=12, fill=(30, 81, 67))
            d.text((59, 292), label, font=font(BOLD, 22), fill=GOLD)
            title = beat["headline"]
            face = font(BOLD, 61 if len(title.replace("\n","")) < 17 else 51)
            dy = int(8*math.sin(t*3))
            center(d, title, (440 if "\n" not in title else 391)+dy, face, CREAM, leading=1.22)
            detail = beat["detail"]
            f = font(REG, 27)
            dw = d.textbbox((0,0), detail, font=f)[2]
            if dw > 640:
                raise ValueError("Detail text too wide: "+detail)
            d.text(((W-dw)//2,695+dy), detail, font=f, fill=SOFT)
            yy = 850+int(6*math.sin(t*2.4))
            d.rounded_rectangle((84,yy,636,yy+125), radius=24,
                                outline=(51,106,85), width=3)
            d.ellipse((115,yy+36,164,yy+85), fill=GOLD)
            d.line((130,yy+62,139,yy+72,153,yy+48),fill=DARK,width=6)
            for q in range(3):
                d.rounded_rectangle((190,yy+34+q*22,570-int((1-fraction)*38),yy+43+q*22),
                                    radius=4,fill=(58+q*12,112+q*12,93+q*12))
            d.rounded_rectangle((44,1110,W-44,1119),radius=4,fill=(38,90,74))
            d.rounded_rectangle((44,1110,44+int((W-88)*(n+1)/frame_count),1119),
                                radius=4,fill=GOLD)
            d.text((44,1148),f"ESG BEZ CHAOSU   •   {beat_index+1}/{len(beats)}",
                   font=font(BOLD,20),fill=SOFT)
            proc.stdin.write(im.tobytes())
            n+=1
    proc.stdin.close()
    if proc.wait()!=0:
        raise RuntimeError("Video encoding failed")
    audio = prefix.with_suffix(".wav")
    sample_rate = 22050
    with wave.open(str(audio),"wb") as wav:
        wav.setnchannels(1);wav.setsampwidth(2);wav.setframerate(sample_rate)
        buf=bytearray()
        for k in range(int(total*sample_rate)):
            sec=k/sample_rate
            pulse=math.exp(-22*(sec%0.5))*math.sin(2*math.pi*360*sec)*0.09
            ambient=0.07*math.sin(2*math.pi*131*sec)+0.04*math.sin(2*math.pi*196*sec)
            fade=min(1,sec/0.2,(total-sec)/0.5)
            buf+=struct.pack("<h",int(max(-1,min(1,(pulse+ambient)*fade))*15000))
            if len(buf)>64000:
                wav.writeframes(buf);buf.clear()
        if buf: wav.writeframes(buf)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y",
                    "-i",str(raw),"-i",str(audio),"-c:v","copy",
                    "-c:a","aac","-b:a","112k","-shortest",
                    "-movflags","+faststart",str(output)],check=True)
    raw.unlink();audio.unlink()
    return {"id":ep["id"],"duration_s":total,"output":str(output)}

if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--id",required=True)
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    episodes=json.loads((ROOT/"retention_v2_storyboards.json").read_text(encoding="utf-8"))
    episode=next((e for e in episodes if e["id"]==args.id),None)
    if episode is None:
        raise SystemExit("Unknown storyboard; no publishing performed")
    print(json.dumps(render(episode,args.out),ensure_ascii=False))

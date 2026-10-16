"""ESG360: branded 9:16 educational slideshow; cloud runner only."""
import json, os, subprocess, shutil
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
BASE=Path(__file__).resolve().parent
episode=next(e for e in json.loads((BASE/"episodes.json").read_text()) if e["id"]==os.environ["EPISODE_ID"])
out=BASE/"generated"; out.mkdir(exist_ok=True)
frames=out/episode["id"];frames.mkdir(exist_ok=True)
regular="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
bold="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def wrap(draw,msg,font,width):
    lines=[];line=""
    for word in msg.split():
        trial=(line+" "+word).strip()
        if draw.textbbox((0,0),trial,font=font)[2]>width and line:
            lines.append(line);line=word
        else:line=trial
    return lines+[line] if line else lines
for i,(heading,body) in enumerate(episode["slides"]):
    im=Image.new("RGB",(1080,1920),(7,40,35));d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,24),fill=(187,148,72))
    d.ellipse((730,-190,1320,400),outline=(51,99,81),width=9)
    d.text((90,115),"ESG360 ACADEMY",font=ImageFont.truetype(bold,48),fill=(220,185,106))
    d.text((90,194),"WIEDZA  •  NARZĘDZIA  •  WDROŻENIE",font=ImageFont.truetype(regular,26),fill=(221,230,213))
    y=580
    f=ImageFont.truetype(bold,76)
    for line in wrap(d,heading,f,900): d.text((90,y),line,font=f,fill=(250,245,225));y+=110
    y+=55;f=ImageFont.truetype(regular,56)
    for line in wrap(d,body,f,900): d.text((90,y),line,font=f,fill=(221,230,213));y+=86
    d.rectangle((90,1665,90+round(900*(i+1)/len(episode["slides"])),1678),fill=(220,185,106))
    d.text((90,1730),f'ESG W MŚP  •  {i+1}/{len(episode["slides"])}',font=ImageFont.truetype(regular,29),fill=(221,230,213))
    im.save(frames/f"{i:03d}.png")
video=out/(episode["id"]+".mp4")
n=len(episode["slides"]); seconds=n*5
cmd=["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","1/5","-i",str(frames/"%03d.png"),"-f","lavfi","-i","anullsrc=channel_layout=stereo:sample_rate=44100","-shortest","-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac","-t",str(seconds),"-movflags","+faststart",str(video)]
subprocess.run(cmd,check=True)
print(f"RENDERED {video} {video.stat().st_size}")

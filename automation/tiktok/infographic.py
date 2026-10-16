"""Create a 1080x1350 ESG360 infographic PNG from approved episode facts."""
import json, os, textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
BASE=Path(__file__).resolve().parent
episodes=json.loads((BASE/"episodes.json").read_text(encoding="utf-8"))
id_=os.getenv("EPISODE_ID","piecdanych")
episode=next(e for e in episodes if e["id"]==id_)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def ft(size,bold=False):return ImageFont.truetype(BOLD if bold else FONT,size)
def wrap(d,txt,font,width):
    lines=[]; cur=""
    for w in txt.split():
        test=(cur+" "+w).strip()
        if cur and d.textbbox((0,0),test,font=font)[2]>width:
            lines.append(cur);cur=w
        else:cur=test
    return lines+([cur] if cur else [])
im=Image.new("RGB",(1080,1350),(9,43,37))
d=ImageDraw.Draw(im)
gold=(218,177,92);white=(246,240,218);muted=(197,214,199)
d.rectangle((0,0,1080,17),fill=gold)
d.text((75,66),"ESG360 ACADEMY",font=ft(42,True),fill=gold)
d.text((75,123),"WIEDZA • NARZĘDZIA • WDROŻENIE",font=ft(24),fill=muted)
y=225
for line in wrap(d,episode["title"].upper(),ft(62,True),940):
    d.text((75,y),line,font=ft(62,True),fill=white);y+=82
y+=35
items=episode["slides"][1:6]
room=1000-y
step=min(155,max(100,int(room/max(len(items),1))))
for ix,(head,body) in enumerate(items,1):
    d.rounded_rectangle((75,y,1005,y+step-12),radius=20,fill=(19,61,53),outline=(74,106,84),width=2)
    d.text((100,y+14),str(ix).zfill(2),font=ft(38,True),fill=gold)
    d.text((175,y+14),head[:36],font=ft(28,True),fill=white)
    lines=wrap(d,body,ft(25),790)
    for j,line in enumerate(lines[:2]):d.text((175,y+56+30*j),line,font=ft(25),fill=muted)
    y+=step
d.rectangle((75,1250,1005,1254),fill=gold)
d.text((75,1280),"ESG W MŚP   •   VSME   •   PRAKTYKA",font=ft(23),fill=muted)
out=BASE/"generated";out.mkdir(exist_ok=True)
path=out/(id_+"-linkedin-infographic.png")
im.save(path,optimize=True)
print("INFOGRAPHIC_READY",path,str(path.stat().st_size))

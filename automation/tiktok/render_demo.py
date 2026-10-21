"""ESG360 Academy: educational file walkthrough, demo-only CSV and MP4.
Uses invented demonstration data; never presents this as a real company's records.
Generates file content and visibly fills its cells step by step.
"""
import csv, json, math, os, struct, subprocess, wave
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BASE=Path(__file__).resolve().parent
episode=next(e for e in json.loads((BASE/"episodes.json").read_text(encoding="utf-8")) if e["id"]==os.environ["EPISODE_ID"])
demo=episode["demo"]; steps=demo["steps"]
OUT=BASE/"generated"; OUT.mkdir(parents=True,exist_ok=True)
FOLDER=OUT/episode["id"];FOLDER.mkdir(parents=True,exist_ok=True)
FILES=OUT/"demo_files";FILES.mkdir(parents=True,exist_ok=True)

HEAD=list(demo["headers"]); INITIAL=[list(row) for row in demo["rows"]]
# Only the second (value) column is changed by the demo, retaining source notes.
def data_at(count):
    rows=[r.copy() for r in INITIAL]
    for change in steps[:count]:
        row=next((x for x in rows if x[0]==change["field"]),None)
        if row is None: raise ValueError("Unknown demo row: "+change["field"])
        if len(row)<2: raise ValueError("Demo row has no value column")
        row[1]=change["value"]
    return rows
for suffix,rows in [("START",INITIAL),("WYPELNIONY",data_at(len(steps)))]:
    with (FILES/(episode["id"]+"_"+suffix+".csv")).open("w",newline="",encoding="utf-8-sig") as f:
        wr=csv.writer(f,delimiter=";")
        wr.writerow(HEAD);wr.writerows(rows)

FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
def font(sz,bold=False):return ImageFont.truetype(BOLD if bold else FONT,sz)
GOLD=(222,184,106);DARK=(7,37,33);WHITE=(251,249,244);MUTED=(199,214,205);BORDER=(205,217,208)
def lines(draw,text,f,maxwidth):
    out=[];cur=""
    for word in str(text).split():
        candidate=(cur+" "+word).strip()
        if cur and draw.textbbox((0,0),candidate,font=f)[2]>maxwidth:
            out.append(cur);cur=word
        else: cur=candidate
    if cur:out.append(cur)
    return out
def put(draw,x,y,text,f,color,width,maxlines=3,step=None):
    l=lines(draw,text,f,width)[:maxlines]
    for line in l:
        draw.text((x,y),line,font=f,fill=color)
        y+=step or round(f.size*1.28)
    return y
def frame(number):
    # frame 0 opens file; frames 1..N edit one row; final frame saves result
    if number==0: label="OTWÓRZ PLIK";note="Zobacz pola i dokumenty źródłowe.";filled=0;highlight=None
    elif number<=len(steps):
        edit=steps[number-1]
        label=f'UZUPEŁNIJ {number}/{len(steps)}'
        note=edit["instruction"];filled=number;highlight=edit["field"]
    else: label="ZAPISZ PLIK";note=demo["result"];filled=len(steps);highlight=None
    rows=data_at(filled)
    im=Image.new("RGB",(1080,1920),DARK)
    d=ImageDraw.Draw(im)
    d.rectangle((0,0,1080,18),fill=GOLD)
    d.text((70,70),"ESG360 ACADEMY",font=font(49,True),fill=GOLD)
    d.text((70,142),"WIEDZA • NARZĘDZIA • WDROŻENIE",font=font(24),fill=MUTED)
    d.text((70,225),f'MODUŁ {demo["module"]}  /  {demo["code"]}',font=font(39,True),fill=WHITE)
    put(d,70,294,episode["title"].split(" — ",1)[-1],font(55,True),WHITE,930,maxlines=2)
    # File editor representation; not a captured real screen recording.
    d.rounded_rectangle((56,460,1024,1342),radius=23,fill=(241,246,241))
    d.rounded_rectangle((56,460,1024,563),radius=23,fill=(25,87,72))
    d.rectangle((56,537,1024,563),fill=(25,87,72))
    d.ellipse((88,500,109,521),fill=(222,184,106))
    d.text((132,494),"PRZYKŁADOWY PLIK CSV",font=font(29,True),fill=WHITE)
    put(d,85,588,demo["filename"],font(29,True),(18,49,40),880,maxlines=2,step=35)
    y=685;colw=[300,300,305];starts=[80,380,680]
    d.rounded_rectangle((75,y,1004,y+72),radius=10,fill=(35,95,78))
    for j,h in enumerate(HEAD):
        put(d,starts[j]+11,y+18,h,font(25,True),WHITE,colw[j]-18,maxlines=1)
    y+=78
    for idx,row in enumerate(rows):
        h=126;is_active=highlight==row[0]
        d.rounded_rectangle((75,y,1004,y+h),radius=8,fill=(255,249,224) if is_active else ((249,251,247) if idx%2==0 else (232,241,235)),outline=GOLD if is_active else BORDER,width=5 if is_active else 2)
        for j,col in enumerate(row):
            color=(24,66,54) if j!=1 else ((124,82,24) if is_active else (33,73,61))
            put(d,starts[j]+10,y+18,col or "—",font(25,j==0),color,colw[j]-24,maxlines=3,step=32)
        if is_active:
            d.polygon([(650,y+101),(676,y+116),(668,y+90)],fill=(9,67,47))
        y+=131
    d.rounded_rectangle((75,1382,1005,1579),radius=18,fill=(27,81,66),outline=(110,148,120),width=2)
    d.text((103,1416),label,font=font(35,True),fill=GOLD)
    put(d,103,1471,note,font(30),WHITE,875,maxlines=2,step=42)
    d.text((75,1630),"DANE PRZYKŁADOWE — SYMULACJA PRACY Z PLIKIEM",font=font(23,True),fill=GOLD)
    d.text((75,1691),"Pobierz plik START i powtórz ćwiczenie.",font=font(28),fill=MUTED)
    d.rectangle((75,1772,75+round(930*(number+1)/(len(steps)+2)),1786),fill=GOLD)
    d.text((75,1810),f'ETAP {number+1}/{len(steps)+2}  •  {demo["code"]}',font=font(25),fill=WHITE)
    p=FOLDER/(f"{number:03d}.png");im.save(p)

for i in range(len(steps)+2):frame(i)
n=len(steps)+2; duration=n*5
sound=OUT/(episode["id"]+"-original-music.wav")
hz=22050;chords=[[130.81,164.81,196.0],[146.83,174.61,220],[110.0,130.81,164.81],[130.81,174.61,196]]
with wave.open(str(sound),"wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(hz)
    block=bytearray()
    for k in range(duration*hz):
        t=k/hz;notes=chords[int(t/5)%len(chords)]
        fade=min(1.0,t/0.5,max(0.0,(duration-t)/1.0))
        sample=sum(math.sin(2*math.pi*f*t)*0.17+math.sin(2*math.pi*2*f*t)*0.025 for f in notes)*fade
        block+=struct.pack("<h",int(max(-1,min(1,sample))*13500))
        if len(block)>=88200:
            w.writeframes(block);block.clear()
    if block:w.writeframes(block)
video=OUT/(episode["id"]+".mp4")
subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-framerate","1/5","-i",str(FOLDER/"%03d.png"),"-i",str(sound),"-shortest","-c:v","libx264","-pix_fmt","yuv420p","-r","30","-c:a","aac","-b:a","128k","-t",str(duration),"-movflags","+faststart",str(video)],check=True)
print("MODULE_RENDERED",demo["module"],video,video.stat().st_size)

from pathlib import Path
import json, math, shutil
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
ROOT=Path(__file__).resolve().parent
A=ROOT/'assets'; A.mkdir(exist_ok=True)
W,H=1024,1536
ink='#34105d'; pink='#ff2799'; yellow='#fff23b'; cyan='#00cde8'
def label(d,xy,s,size,fill=ink,anchor=None):
    d.text(xy,s,font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc',size),fill=fill,anchor=anchor)
# Identical layout transforms preserve registration between the three cutouts.
layers=ROOT.parent/'分层素材/01-巫女'
def place(im):
    canvas=Image.new('RGBA',(W,H))
    canvas.alpha_composite(im.resize((580,1242),Image.Resampling.LANCZOS),(235,90))
    return canvas
tail=Image.open(layers/'AI补绘参考/01-狐尾-补绘.png').convert('RGBA').resize((712,1524),Image.Resampling.LANCZOS)
tail.alpha_composite(Image.open(layers/'原像素分层/01-狐尾.png').convert('RGBA'))
parts={'tail':place(tail),'gohei':place(Image.open(layers/'视差补全分层/02-御币.png').convert('RGBA')),'subject':place(Image.open(layers/'视差补全分层/03-角色主体.png').convert('RGBA'))}
for name,im in parts.items(): im.save(A/(name+'.png'))
white=Image.new('RGBA',(W,H),'white'); white.alpha_composite(parts['subject'])
line=ImageOps.invert(white.convert('L').filter(ImageFilter.FIND_EDGES)).point(lambda x:0 if x<190 else 255)
ImageDraw.Draw(line).rectangle((0,0,W-1,H-1),outline='white',width=3); line.save(A/'lineart.png')
bg=Image.open(A/'background-options/party-pop-shrine.png').convert('RGB')
assert bg.size==(W,H)
bg.save(A/'background.png')
def star(d,x,y,r,fill):
    points=[(x+math.sin(i*math.pi/4)*(r if i%2==0 else r*.28),
             y-math.cos(i*math.pi/4)*(r if i%2==0 else r*.28)) for i in range(8)]
    d.polygon(points,fill=fill,outline=ink,width=5)
fx=Image.new('RGBA',(W,H));d=ImageDraw.Draw(fx)
for x,y,r,color in [(186,475,42,yellow),(864,530,34,'white'),(181,1040,44,pink),(838,1150,52,yellow)]:
    star(d,x+5,y+8,r+8,'white');star(d,x,y,r,color)
fx.save(A/'effects.png')
text=Image.new('RGBA',(W,H));d=ImageDraw.Draw(text)
d.rounded_rectangle((14,14,1009,1521),radius=45,outline=ink,width=22)
d.rounded_rectangle((31,31,992,1504),radius=30,outline='white',width=8)
d.line([(43,250),(43,47),(340,47)],fill=yellow,width=13)
d.line([(981,1270),(981,1493),(694,1493)],fill=pink,width=13)
d.polygon([(65,75),(222,62),(204,222),(53,230)],fill=ink)
d.polygon([(57,61),(208,48),(190,203),(45,211)],fill=yellow,outline=ink,width=6)
label(d,(127,127),'巫',87,ink,'mm')
d.rounded_rectangle((768,66,952,119),radius=12,fill=ink)
label(d,(860,91),'NO. 001',24,'white','mm')
d.polygon([(85,1310),(939,1273),(963,1448),(69,1480)],fill=ink)
d.polygon([(70,1288),(923,1251),(942,1419),(53,1450)],fill='white',outline=ink,width=8)
d.polygon([(63,1316),(302,1307),(278,1422),(57,1431)],fill=pink)
label(d,(182,1365),'照',106,'white','mm')
label(d,(610,1346),'三神御主',83,ink,'mm')
d.polygon([(385,1410),(924,1389),(919,1449),(370,1470)],fill=yellow,outline=ink,width=5)
label(d,(650,1432),'DIVINE TRINITY',26,ink,'mm')
text.save(A/'text.png')
# The same wordless print and graphic vocabulary continue on the reverse.
back=bg.convert('RGBA');d=ImageDraw.Draw(back)
d.rounded_rectangle((14,14,1009,1521),radius=45,outline=ink,width=22)
d.rounded_rectangle((34,34,989,1501),radius=28,outline='white',width=8)
d.polygon([(130,330),(862,267),(931,1175),(181,1240)],fill=ink)
d.polygon([(153,350),(836,295),(905,1149),(205,1211)],outline=cyan,width=9)
star(d,520,708,255,pink);star(d,506,690,234,yellow)
d.text((506,694),'照',font=ImageFont.truetype('C:/Windows/Fonts/msyhbd.ttc',166),fill='white',anchor='mm',stroke_width=7,stroke_fill=ink)
label(d,(512,455),'SHRINE PARTY',46,'white','mm')
label(d,(532,1020),'三神御主',65,'white','mm')
label(d,(536,1100),'COLLECTION / 001',26,yellow,'mm')
back.save(A/'back.png')
preview=bg.convert('RGBA')
for k in ('tail','gohei','subject'):preview.alpha_composite(parts[k])
preview.alpha_composite(fx);preview.alpha_composite(text);preview.save(ROOT/'design-preview.png')
cfg={'title':'照','subtitle':'三神御主','technique':'','tagline':'','edition':'001 / 神社典藏','collection':'神社典藏','description':'粉发狐耳巫女 · 三神御主','assets':{k:'./assets/'+k+'.png' for k in ['subject','tail','gohei','background','effects','lineart','text']},'parameters':{'subjectScale':1,'subjectDepth':0.42,'backgroundDepth':-0.32,'effectsScale':1,'effectsDepth':0.8,'foil':0.42},'characterLayers':{'tailDepth':-0.35,'bodyDepth':0.42,'goheiDepth':0.9,'gripUV':[0.685,0.363]},'safeArea':{'scale':1,'offset':[0,0]},'appearance':{'background':'#fff7e7'}}
cfg['assets']['model']='./assets/card.glb'
cfg['assets']['back']='./assets/back.png'
cfg['collection']='神社派对'
cfg['edition']='001 / 神社派对'
cfg['appearance']['background']='#f3f0ff'
(ROOT/'card-config.json').write_text(json.dumps(cfg,ensure_ascii=False,indent=2),encoding='utf8')
for k in parts: assert parts[k].getextrema()[3]==(0,255)
assert all(Image.open(p).size==(W,H) for p in A.glob('*.png'))
if (ROOT/'web/assets').exists():
    for p in A.glob('*.png'):shutil.copy2(p,ROOT/'web/assets'/p.name)
    shutil.copy2(ROOT/'card-config.json',ROOT/'web/card-config.json')

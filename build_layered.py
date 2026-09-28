"""Build the existing card pipeline, then add the actual tail/gohei compositing nodes."""
from pathlib import Path
import sys, runpy, math
import bpy

root=Path(__file__).resolve().parent
sys.argv=['build_card.py','--',str(root),'--skip-render']
ns=runpy.run_path('C:/Users/shenf/.codex/skills/RuiC-card-skill/scripts/build_card.py')
t=ns['t']; g=ns['g']; pS=ns['pS']; previous=ns['ba']
for index,(key,depth) in enumerate([('tail',-.35),('gohei',.9)]):
    im=bpy.data.images.load(str(root/'assets'/(key+'.png')));im.pack()
    par=ns['parallax'](t,key+' 独立景深',1,depth,-1200,-1450-index*400)
    if key=='gohei':
        dist=ns['vec'](t,'DISTANCE','御币握持点距离',-1450,-1850)
        dist.inputs[1].default_value=(.664,.635,0)
        ns['link'](t,pS,'视差效果',dist,0)
        # Smooth transition keeps the handle at the body's depth and the tip forward.
        ramp=ns['node'](t,'ShaderNodeMapRange','手掌固定 / 顶端前伸',-1200,-2100)
        ramp.interpolation_type='SMOOTHSTEP';ramp.clamp=True
        ramp.inputs['From Min'].default_value=.025;ramp.inputs['From Max'].default_value=.20
        ramp.inputs['To Min'].default_value=.42;ramp.inputs['To Max'].default_value=.9
        ns['link'](t,dist,'Value',ramp,'Value');ns['link'](t,ramp,'Result',par,'深度')
    tex=ns['node'](t,'ShaderNodeTexImage',key+' 分层 PNG',-900,-1450-index*400)
    tex.image=im;tex.extension='CLIP';ns['link'](t,par,'视差效果',tex,'Vector')
    bs=ns['bsdf'](t,key+' 印刷层',-600,-1450-index*400);ns['link'](t,tex,'Color',bs,'Base Color')
    mx=ns['node'](t,'ShaderNodeMixShader',key+' Alpha 合成',1000,-1450-index*400)
    ns['link'](t,tex,'Alpha',mx,0);ns['link'](t,previous,0,mx,1);ns['link'](t,bs,0,mx,2)
    previous=mx
ns['link'](t,previous,0,ns['mix'],1)
scene=bpy.context.scene
scene['素材来源']='角色：项目已有分层；背景：内置 imagegen；派对卡框、排版和卡背：prepare.py。'
back_image=bpy.data.images.load(str(root/'assets/back.png'));back_image.pack()
back_tex=ns['node'](ns['bt'],'ShaderNodeTexImage','派对卡背',-600,0);back_tex.image=back_image
coords=ns['node'](ns['bt'],'ShaderNodeTexCoord','卡背 UV',-1000,0)
mapping=ns['node'](ns['bt'],'ShaderNodeMapping','卡背镜像校正',-800,0)
mapping.inputs['Scale'].default_value=(-1,1,1);mapping.inputs['Location'].default_value=(1,0,0)
ns['link'](ns['bt'],coords,'UV',mapping,'Vector');ns['link'](ns['bt'],mapping,'Vector',back_tex,'Vector')
ns['link'](ns['bt'],back_tex,'Color',ns['bp'],'Base Color')
ns['link'](ns['bt'],back_tex,'Color',ns['bp'],'Emission Color');ns['bp'].inputs['Emission Strength'].default_value=.35
ns['gp'].inputs['Base Color'].default_value=(.12,.01,.28,1)
scene['角色分层']='狐尾 -0.35 / 身体 0.42 / 御币顶端 0.90；握持位置维持身体深度。'
bpy.context.preferences.filepaths.save_version=0
scene.frame_set(25)
bpy.ops.wm.save_as_mainfile(filepath=str(root/'card.blend'))
for frame,name in [(25,'hero'),(1,'tilt-left'),(49,'tilt-right')]:
    scene.frame_set(frame);scene.render.filepath=str(root/'renders'/(name+'.png'))
    bpy.ops.render.render(write_still=True)

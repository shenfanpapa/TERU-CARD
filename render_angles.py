from pathlib import Path
import bpy

root=Path(__file__).resolve().parent
bpy.ops.wm.open_mainfile(filepath=str(root/'card.blend'))
scene=bpy.context.scene
scene['素材来源']='角色：项目原图/01-巫女.png；背景、符纸与排版：本项目原创。'
bpy.context.preferences.filepaths.save_version=0
bpy.ops.wm.save_as_mainfile(filepath=str(root/'card.blend'))
for frame,name in [(1,'tilt-left'),(49,'tilt-right')]:
    scene.frame_set(frame)
    scene.render.filepath=str(root/'renders'/(name+'.png'))
    bpy.ops.render.render(write_still=True)

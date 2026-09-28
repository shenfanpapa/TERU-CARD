# 照 · 四款全息闪卡

启动：进入 `web/`，运行 `node server.mjs`，打开 http://127.0.0.1:4173 。网页已打包，无需安装 npm 依赖。可切换巫女、蓝伞、护士和歌姬四张卡，并支持翻面、镭射材质与下载。

每张卡的合并立绘、底纹、卡背及配置位于 `web/cards/<卡片>/`。四张卡面的 PNG 导出在 `cards-export/`。

角色使用现有的狐尾、身体、御币透明分层；三者共用同一排版坐标，但采用独立视差采样。狐尾景深 -0.35，身体 0.42，御币顶端 0.90。御币在手掌附近回到身体景深，防止握持位置脱节。网页新增狐尾与御币景深滑块。

背景采用选定的高饱和青、粉、黄、紫派对插画（内置 imagegen），搭配神社、樱花、棋盘格和网点。深紫粗线卡框、斜切姓名贴纸、巫女标识、编号、前景星星及卡背统一采用派对设计；网页同步更新为同套配色。文字仍是独立透明图层。完整背景提示词见 assets/background-options/party-pop-prompt.md。

拖动旋转，滚轮缩放；方向键微调，R 重置，空格切换自动转动，F 翻面。右上角下载 PNG。

- assets/：同尺寸图层，包含 tail.png、gohei.png、subject.png 和 back.png。
- design-preview.png：平面设计稿。
- card.blend：内嵌图层和独立视差节点的可编辑 Blender 场景。
- renders/：正面与左右倾斜渲染。
- web/：完整网页源文件和打包文件。
- prepare.py：从既有分层重建排版素材。
- build_layered.py：生成带角色分层的 Blender 场景。
- verify_web.mjs：浏览器交互检查；报告在 verification/report.json。

参考：用户提供的卡图与 https://se.feimogames.com/home 。角色没有重新生成；狐尾使用已有补绘参考填充遮挡部分，再叠加原像素。背景由内置 imagegen 生成，排版与卡背由 prepare.py 构建。个人作品，无官方关联。

网页使用 GLSL 重建 Blender 节点，GLB 携带几何与材质角色；两者并非像素一致。CSS 降级模式保留图层，御币握持约束以正常 WebGL 模式为准。

派对版验证（2026-09-22）：Chrome 桌面 29 项、Edge 手机端 6 项全部通过，包括材质、分层景深、翻面、缩放、1400×1800 PNG 下载及减少动态效果。报告位于 verification/report.json。

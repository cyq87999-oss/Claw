# I2V Prompt Playbook（要素词库与规则）

Detailed vocabulary and rules for each of the 10 mandatory elements. Use when drafting prompts or
when the user wants richer, more precise phrasing. Combine freely; keep every element present.

---

## 1. 主体锁定 (Subject Lock)

Purpose: pin identity so the model does NOT swap faces, clothing, or props between frames.

Required sub-fields:
- **外貌**: 年龄感、发型发色、五官特征、体型、肤色、标志性配饰。
- **服装**: 具体款式、颜色、材质、纹样、穿着状态（整洁/破损/湿润）。
- **位置与朝向**: 在画面中相对位置（中景偏左、画面下方）、朝向（正对镜头 / 侧身 3/4 / 背对）。

Phrasing patterns:
- "保持同一位黑发及肩、左眼角有泪痣的年轻女子，身着墨色交领长袍、袖口绣银纹，正对镜头站于画面中下。"
- "锁定画面中央的青铜古剑，剑身刻云雷纹，剑柄缠深红丝绦，不更换道具。"
- 强烈建议追加锁词："人物外貌与服装全程保持一致，不得改变发型、脸型、服饰配色。"

## 2. 动作描述 (Action)

Purpose: specify motion so it is not vague ("动一下") but concrete.

Required sub-fields: 具体动作 + 幅度 + 方向 + 速度。

Verb banks:
- 头部/视线: 缓慢转头、抬眼、垂眸、侧脸、瞪视、挑眉。
- 上肢: 抬手、握紧、挥砍、拉弓、掩面、指向前方。
- 躯干/下肢: 挺直脊背、俯身、后仰、迈步、单膝跪地、腾空跃起。
- 道具交互: 拔剑出鞘、翻页、举杯、收伞、拉栓。

Speed words: 缓慢 / 匀速 / 骤然 / 疾速 / 轻柔地 / 猛地。
Amplitude words: 微微 / 小幅 / 大幅度 / 完全。

Examples:
- "右手握剑由右上向左下劈砍，大幅度、快速，刀光带残影。"
- "缓慢转头看向镜头，幅度约 30 度，用时 2 秒。"

## 3. 镜头运动 (Camera Move)

Purpose: drive cinematic feel; must suit 9:16 vertical frame.

Move types (use Chinese + optional English tag):
- 推 (push in / dolly in): 镜头缓慢向前推进，主体放大。
- 拉 (pull out / dolly out): 镜头后退，环境展开。
- 摇 (pan / tilt): 横摇 / 上摇 / 下摇。竖屏多用**上摇/下摇**。
- 移 (tracking / lateral): 注意竖屏限制，移速宜慢、幅度小。
- 跟 (follow): 跟随主体移动。
- 升降 (crane / boom): 镜头自低处缓缓升起至平视。
- 旋转 (orbit / roll): 环绕主体旋转，或轻微荷兰角倾斜。

Vertical-friendly patterns:
- "镜头从胸口缓慢上摇至面部特写。"
- "镜头自地面缓缓升起，掠过裙摆至上半身。"
- "轻微环绕主体旋转 15 度，营造紧张感。"

## 4. 景别与构图 (Shot & Composition)

Shot sizes: 特写 (CU) / 近景 (MCU) / 中景 (MS) / 全景 (WS) / 远景 (EWS)。

Composition rules for 9:16:
- 主体居中或置于三分线（左 1/3 或右 1/3 竖线）。
- 头顶留白 10–15%，避免顶天立地。
- 重要信息（脸、手、关键道具）置于中心安全区（画面中 60%）。
- 竖屏少用大远景，多用中近景突出人物。

Phrasing:
- "近景，人物居中偏左三分线，头顶留白，背景虚化。"
- "特写，面部占画面 70%，眼神清晰。"

## 5. 光影氛围 (Lighting & Mood)

Sub-fields: 光源方向 + 色调 + 明暗 + 时间/天气。

Light directions: 顺光 / 侧光 / 逆光 / 顶光 / 底光 / 轮廓光。
Color tones: 冷蓝 / 暖橙 / 青绿 / 霓虹紫红 / 自然日光。
Mood/time/weather: 雨夜 / 黄昏 / 正午烈阳 / 雾晨 / 雪天 / 室内烛光。

Examples:
- "冷蓝逆光，雨夜，湿地面霓虹反射，整体偏暗高对比。"
- "暖橙侧光，黄昏，发丝镀金边，柔和明暗过渡。"

## 6. 风格一致性 (Style Consistency)

Always pair a 画风 + 材质/渲染 + 质量词.

Style banks:
- 国风漫剧 / 水墨 / 厚涂 / 赛璐璐 / 日式动漫 / 美式卡通。
- 3D 渲染 / 虚幻引擎风格 / Blender 质感 / 皮克斯风。
- 写实 / 胶片感 / 电影级调色。

Quality words (质量词): 电影感、8K、超清、细节丰富、光线追踪、高质感、统一美术风格。

Examples:
- "国风漫剧、厚涂笔触、电影感、细节丰富、统一美术风格。"
- "3D 渲染、虚幻引擎风格、光线追踪、电影级调色、8K。"

Note: when continuing a sequence, REPEAT the exact style string on every shot to hold consistency.

## 7. 节奏与时长 (Rhythm & Duration)

State action duration and, for sequences, transition rhythm.
- 单镜时长: "本镜 4 秒" / "2–3 秒快切"。
- 动作时长: "3 秒内完成转身拔刀" / "用 1.5 秒缓缓睁眼"。
- 转场节奏: "硬切衔接下一镜" / "淡出过渡"。

Short-video guidance: 单镜 3–6 秒，冲突/表情钩子放镜 1。

## 8. 空间关系 (Spatial Relation)

Sub-fields: 前后景 + 景深 + 遮挡，防穿模。

Patterns:
- "前景树叶虚化，人物在中景清晰。"
- "背景人群景深虚化，前景栏杆半遮挡主体，不穿模。"
- "主体与背景分层明确，避免肢体与道具错误重叠。"

Depth words: 浅景深 / 大光圈虚化 / 前景虚化 / 背景压缩。

## 9. 首尾帧约束 (Start/End Frame)

Use when a shot must connect to a reference image or the previous shot.
- 起始帧: "起始画面：人物静立，手扶剑柄，眼神下视。"
- 结束帧: "结束画面：人物已拔剑横于胸前，抬眼盯镜头。"
- 序列衔接: 上一镜结束帧 = 下一镜起始帧（连续叙事）。

If no continuity needed, write "无强制首尾帧约束，以参考图为首帧。"

## 10. 负面提示词 (Negative Prompt)

Exclude defects. Provide both a CN and (when model supports) EN list.

CN negatives:
- 模糊、低分辨率、变形、扭曲、肢体多余或缺失、手指异常、面部畸变。
- 字幕、水印、logo、文字、签名、时间戳。
- 风格跳变、画风不一致、低质量、过曝、死黑、噪点。
- 穿模、物体悬浮、不合理遮挡、画面抖动、闪烁、抽帧。

EN negatives (for Jimeng/Kling/Runway/Wan):
- blurry, lowres, deformed, distorted, extra limbs, missing limbs, bad hands, bad fingers,
  mutated face, text, watermark, logo, signature, inconsistent style, low quality,
  overexposed, flickering, jitter, clipping, floating object.

---

## Vertical-Screen Logic Checklist (apply every shot)

- [ ] 主体位于中心 60% 安全区，未贴左右边。
- [ ] 主要动作为纵向（抬头/俯身/跃起/下坠）或小幅横向。
- [ ] 头顶留白 10–15%，未顶天立地。
- [ ] 关键脸/手/道具在中心安全区。
- [ ] 单镜时长标注（3–6 秒为宜）。
- [ ] 若为首镜，含冲突/表情特写钩子。
- [ ] 风格串与前后镜一致。

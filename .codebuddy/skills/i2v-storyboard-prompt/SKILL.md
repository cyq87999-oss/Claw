---
name: i2v-storyboard-prompt
description: Generate structured image-to-video (图生视频 / I2V) storyboard prompts for vertical short-form video 9:16, with support for 1–10 reference storyboard images and a plot/narrative layer. This skill should be used when a user wants to turn a character, prop, or scene image into a video-generation prompt, needs a storyboard shot list, asks for 图生视频分镜提示词, 视频生成提示词, 分镜脚本, 竖屏视频提示词, 剧情提示词, or I2V image-to-video prompt, or wants to attach 分镜图 / first-frame images across multiple shots. It enforces 10 mandatory elements (subject lock, action, camera move, shot/composition, lighting, style, rhythm/duration, spatial relation, start-end frame, negative prompt) plus vertical-screen logic, and produces copy-ready prompts compatible with Jimeng/即梦, Kling/可灵, Wan, Seedance, Runway and similar models.
---

# I2V Storyboard Prompt（图生视频分镜提示词）

## Overview

This skill produces high-fidelity, production-ready **image-to-video storyboard prompts** for
vertical (9:16) short-form video. It guarantees every generated prompt covers the 10 mandatory
elements and respects vertical-screen composition logic, so generated clips stay on-subject,
on-character, and on-composition instead of drifting, deforming, or going off-frame.

Use it whenever a user supplies a reference image (or describes one) and wants motion, a shot,
or a sequence for video generation.

## Core Principle: The 10-Element Mandatory Skeleton

Never emit a prompt that omits any of these. When the user provides partial info, infer the rest
and mark inferred parts, but keep all 10 present.

1. **主体锁定 (Subject Lock)** — 人物/道具的外貌、服装、位置、朝向。防止变形或替换。
2. **动作描述 (Action)** — 具体动作、幅度、方向、速度。如"缓慢转头看向镜头""右手握剑下劈"。
3. **镜头运动 (Camera Move)** — 推、拉、摇、移、跟、升降、旋转；适配竖屏。如"镜头从胸口缓慢上摇至面部"。
4. **景别与构图 (Shot & Composition)** — 特写/近景/中景/全景；竖屏 9:16，主体居中或三分线，头顶留白，重要信息放中心安全区。
5. **光影氛围 (Lighting & Mood)** — 光源方向、色调、明暗、时间天气。如"冷蓝逆光，雨夜，霓虹反射"。
6. **风格一致性 (Style Consistency)** — 画风、材质、质量词。如"国风漫剧、厚涂、3D 渲染、电影感"。
7. **节奏与时长 (Rhythm & Duration)** — 动作持续时间、转场节奏，适配快节奏。如"3 秒内完成转身拔刀"。
8. **空间关系 (Spatial Relation)** — 前后景、景深、遮挡，避免穿模。如"前景树叶虚化，人物在中景清晰"。
9. **首尾帧约束 (Start/End Frame)** — 如需首尾帧衔接，明确起始与结束画面。
10. **负面提示词 (Negative Prompt)** — 排除模糊、变形、多余肢体、字幕水印、低质量等。

## Vertical-Screen Additional Logic (竖屏附加逻辑) — ALWAYS apply

- **人物不贴边**：主体保持画面中心 60% 安全区内，左右留呼吸空间。
- **动作纵向优先**：优先上下向运动（抬头、俯身、跃起、下坠），避免大幅横向出画。
- **开篇强钩子**：前 1–2 秒给冲突或表情特写，适配滑屏节奏。
- **构图留白**：头顶预留 10–15% 空白，避免顶天立地；关键信息置于中心安全区。
- **单镜时长**：短视频单镜通常 3–6 秒，快节奏序列 2–3 秒。

## Advanced: Storyboard Images (1–10) & Plot Layer（进阶：分镜图与剧情层）

Image-to-video is anchored by input images, and a sequence needs a narrative spine. Extend the
skeleton with two layers whenever the user supplies images or wants a coherent multi-shot story.

### A. 分镜图输入（1–10 张）
Support 1–10 reference images across a sequence (one or more per shot). Each image plays a role:
- **首帧图 (first-frame)** — the starting frame the model animates from.
- **尾帧图 (end-frame)** — the target ending frame for start→end morph / continuity.
- **参考图 (reference)** — character / prop / scene identity lock, not necessarily a frame.

In the text prompt, label each image explicitly so the user knows what to upload where:
`（首帧图）人物静立持剑，墨袍，参考文件 shot01.png` ·
`（尾帧图）剑已出鞘，参考文件 shot01_end.png`.
For continuity, the end-frame image of shot N doubles as the first-frame / identity reference of
shot N+1 — keep filenames and descriptions aligned.

Platform note: 即梦 / 可灵 / Wan / Runway take the image as a **dedicated input field**
(first-frame / image-to-video), NOT inside the text. The text label is the instruction; the file
is uploaded separately in the platform UI/API. The generator/script accept an `images` list with
`{role, file, caption}` per image.

### B. 剧情提示词层（Plot Layer）
Capture the narrative before generating shots so identity and mood never drift:
- **Logline（一句话梗概）** — e.g., "少女为复仇潜入雨夜古堡，三镜内完成拔剑对峙。"
- **角色卡 (character sheet)** — name, look, costume, weapon; reused for 主体锁定 on every shot.
- **情绪曲线 (emotion arc)** — per-shot mood (惊→怒→释); drives 光影 / 节奏.
- **分场清单 (shot list)** — which story beat each of the 1–10 shots covers.

Embed the logline once at the top of a sequence as a `【剧情】` block. Per shot, reuse the exact
character and style strings from the sheet. Generator accepts a `plot` string and an `images` list.

## Workflow

1. **Confirm inputs.** Identify from the user's request: reference subject (or image description),
   intended style, desired mood, and whether it is a single shot or a sequence. If a story is
   implied, capture the **plot layer** (logline + character sheet + emotion arc) first.
2. **Map images.** For I2V, collect the 1–10 reference images and assign each a role
   (首帧图 / 尾帧图 / 参考图) and a target shot. Keep ≤10 total.
3. **Fill the skeleton.** For each of the 10 elements, write concrete Chinese phrasing. Pull
   vocabulary from `references/prompt-playbook.md` when stuck. Do not leave placeholders.
4. **Apply vertical logic.** Run the vertical-screen checks above; adjust composition and action
   wording so nothing exits frame horizontally.
5. **Assemble with the template.** Use the canonical order below to join elements into one prompt
   string. Quote the reference image / previous end frame where continuity matters, and prepend the
   `【剧情】` block for a sequence.
6. **(Optional) Use the generator.** For batch or guaranteed-completeness output, run
   `scripts/generate_prompt.py` with a JSON of the 10 fields plus optional `plot` and `images`
   — it enforces structure, applies vertical logic, and flags any missing element.
7. **Deliver copy-ready text.** Output the final prompt plus a one-line plain-language
   explanation of the shot for the user, and list which image file(s) to upload for each shot.

### Canonical Template（模板示例）

```
[主体锁定 + 服装外貌] + [动作描述] + [镜头运动] + [景别/构图] + [光影氛围] + [风格一致性] + [节奏与时长] + [空间关系] + [首尾帧约束] + [负面提示词]
```

Order is a guideline, not law — but keep negative prompt last and subject first.

## Output Format

For each shot, return:

- **Shot label** (e.g., 镜 1 / SC01)
- **Prompt (CN)** — the assembled prompt string
- **Negative (CN)** — the negative prompt (also embedded at the end)
- **Reference / continuity note** — which image or previous end frame this shot continues from
- **Image uploads** — for I2V, the exact file(s) to attach per shot (首帧图 / 尾帧图 / 参考图) and
  where in the platform UI they go.

For a sequence, prepend a single `【剧情】` block (logline) and keep `首尾帧约束` consistent across
adjacent shots (shot N's end frame = shot N+1's start frame). The end-frame image of shot N is the
first-frame / reference image of shot N+1.

## Resources

- `references/prompt-playbook.md` — vocabulary banks and rules for every element (camera moves,
  shot sizes, lighting, styles, negative prompts, continuity). Load when drafting or when the user
  wants richer phrasing.
- `references/templates.md` — full worked examples across styles (国风漫剧 / 厚涂 / 3D 渲染 / 写实),
  single shots and multi-shot sequences, with start-end continuity.
- `references/styles_apocalypse.md` — **末日废墟 / 废土** 风格扩展包：核心风格词、光影、细节、
  构图运镜、通用模板、运镜大全、动作库、即梦音效(dB)速查、末日专属负面词、3 分钟分镜范例
  《余烬》。生成时把对应词串填入 10 要素即可。
- `references/action_cinematic.md` — **动作 / 电影感分镜描述词体系**：镜头运动、景别、动态节奏、
  视听氛围四大弹药库 + 万能结构模板 + 进阶技巧（静默对比/POV/比喻通感/子弹时间/快速剪辑）+
  一场完整仓库枪战高潮戏范例。解决「画面描述怎么写才专业」，可直接作为即梦「画面描述」产出标准。
- `scripts/generate_prompt.py` — deterministic assembler. Reads a JSON of the 10 fields, applies
  vertical logic, and prints a validated prompt. Use for batch or guaranteed completeness.
- `assets/webapp/index.html` — **零安装网页版 / 单文件 App**：10 要素表单、实时预览、竖屏逻辑
  自动检查、风格预设、中英负面词、多镜序列（首尾帧自动衔接），并支持**剧情提示词层**与**每镜
  1–10 张分镜图（首帧/尾帧/参考，含文件名标注）**。直接用浏览器打开即可，可离线使用，也随 skill
  一起分发。把它当成「app」用最方便。

See `references/templates.md` for the canonical input→output pattern before writing prompts.

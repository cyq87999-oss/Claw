---
name: i2v-storyboard-prompt
description: Generate structured image-to-video (图生视频 / I2V) storyboard prompts for vertical short-form video 9:16. This skill should be used when a user wants to turn a character, prop, or scene image into a video-generation prompt, needs a storyboard shot list, or asks for 图生视频分镜提示词, 视频生成提示词, 分镜脚本, 竖屏视频提示词, or I2V image-to-video prompt. It enforces 10 mandatory elements (subject lock, action, camera move, shot/composition, lighting, style, rhythm/duration, spatial relation, start-end frame, negative prompt) plus vertical-screen logic, and produces copy-ready prompts compatible with Jimeng/即梦, Kling/可灵, Wan, Seedance, Runway and similar models.
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

## Workflow

1. **Confirm inputs.** Identify from the user's request: reference subject (or image description),
   intended style, desired mood, and whether it is a single shot or a sequence.
2. **Fill the skeleton.** For each of the 10 elements, write concrete Chinese phrasing. Pull
   vocabulary from `references/prompt-playbook.md` when stuck. Do not leave placeholders.
3. **Apply vertical logic.** Run the vertical-screen checks above; adjust composition and action
   wording so nothing exits frame horizontally.
4. **Assemble with the template.** Use the canonical order below to join elements into one prompt
   string. Quote the reference image / previous end frame where continuity matters.
5. **(Optional) Use the generator.** For batch or guaranteed-completeness output, run
   `scripts/generate_prompt.py` with a JSON of the 10 fields — it enforces structure, applies
   vertical logic, and flags any missing element.
6. **Deliver copy-ready text.** Output the final prompt plus a one-line plain-language
   explanation of the shot for the user.

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

When producing a sequence, keep `首尾帧约束` consistent across adjacent shots (shot N's end frame =
shot N+1's start frame).

## Resources

- `references/prompt-playbook.md` — vocabulary banks and rules for every element (camera moves,
  shot sizes, lighting, styles, negative prompts, continuity). Load when drafting or when the user
  wants richer phrasing.
- `references/templates.md` — full worked examples across styles (国风漫剧 / 厚涂 / 3D 渲染 / 写实),
  single shots and multi-shot sequences, with start-end continuity.
- `scripts/generate_prompt.py` — deterministic assembler. Reads a JSON of the 10 fields, applies
  vertical logic, and prints a validated prompt. Use for batch or guaranteed completeness.
- `assets/webapp/index.html` — **零安装网页版 / 单文件 App**：10 要素表单、实时预览、竖屏逻辑
  自动检查、风格预设、中英负面词、多镜序列（首尾帧自动衔接）。直接用浏览器打开即可，可离线使用，
  也随 skill 一起分发。把它当成「app」用最方便。

See `references/templates.md` for the canonical input→output pattern before writing prompts.

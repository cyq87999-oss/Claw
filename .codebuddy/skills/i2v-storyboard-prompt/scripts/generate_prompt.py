#!/usr/bin/env python3
"""Assemble a validated image-to-video (I2V) storyboard prompt.

Reads a JSON describing the 10 mandatory elements, applies vertical-screen logic,
validates completeness, and prints a copy-ready prompt plus an EN negative list.

Usage:
    python3 generate_prompt.py shot.json
    python3 generate_prompt.py shot.json --no-vertical
    cat shot.json | python3 generate_prompt.py -

JSON schema (all 10 fields required unless noted):
{
  "label": "镜 1",                       # optional
  "subject":  "黑发女子墨袍持剑静立...",  # 主体锁定
  "action":   "右手缓缓拔剑...",          # 动作描述
  "camera":   "镜头从胸口上摇至面部",     # 镜头运动
  "shot":     "特写，面部占70%...",       # 景别/构图
  "lighting": "冷蓝逆光，雨夜...",        # 光影氛围
  "style":    "国风漫剧、厚涂、电影感",   # 风格一致性
  "rhythm":   "本镜4秒，前1秒表情钩子",  # 节奏与时长
  "spatial":  "前景雨丝虚化...",          # 空间关系
  "frames":   "起始帧...结束帧...",       # 首尾帧约束 (str or {start,end})
  "negative": ["模糊","变形",...]         # 负面提示词 (list or str)
}
"""
import json
import sys

ELEMENTS = [
    ("subject", "主体锁定"),
    ("action", "动作描述"),
    ("camera", "镜头运动"),
    ("shot", "景别/构图"),
    ("lighting", "光影氛围"),
    ("style", "风格一致性"),
    ("rhythm", "节奏与时长"),
    ("spatial", "空间关系"),
    ("frames", "首尾帧约束"),
    ("negative", "负面提示词"),
]

EN_NEGATIVE = (
    "blurry, lowres, deformed, distorted, extra limbs, missing limbs, bad hands, "
    "bad fingers, mutated face, text, watermark, logo, signature, inconsistent style, "
    "low quality, overexposed, flickering, jitter, clipping, floating object"
)

DEFAULT_CN_NEGATIVE = [
    "模糊", "低分辨率", "变形", "扭曲", "多余肢体", "缺失肢体", "手指异常",
    "面部畸变", "字幕", "水印", "logo", "文字", "风格跳变", "低质量",
    "过曝", "死黑", "噪点", "穿模", "画面抖动", "闪烁", "抽帧",
]


def load_data(path):
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt_frames(frames):
    if isinstance(frames, dict):
        s = frames.get("start", "")
        e = frames.get("end", "")
        return f"起始帧：{s}；结束帧：{e}" if (s or e) else "无强制首尾帧约束，以参考图为首帧。"
    return str(frames)


def fmt_negative(neg):
    if isinstance(neg, list):
        return "、".join(neg)
    return str(neg)


def vertical_warnings(d):
    """Return list of human-readable vertical-logic warnings."""
    w = []
    subject = d.get("subject", "")
    if not any(k in subject for k in ["居中", "中下", "中上", "中心", "三分"]):
        w.append("主体锁定未明确画面位置（建议注明居中/中下/三分线，避免贴边）。")
    rhythm = d.get("rhythm", "")
    if "秒" not in rhythm:
        w.append("节奏与时长未标注秒数（竖屏建议单镜 3–6 秒）。")
    shot = d.get("shot", "")
    if "留白" not in shot and "特写" not in shot:
        w.append("景别/构图未提头顶留白（建议留白 10–15%）。")
    return w


def build(d, vertical=True):
    missing = [cn for key, cn in ELEMENTS if not str(d.get(key, "")).strip()]
    if missing:
        raise ValueError("缺少必备要素：" + "、".join(missing))

    parts = [
        f"（主体锁定）{d['subject']}",
        f"（动作描述）{d['action']}",
        f"（镜头运动）{d['camera']}",
        f"（景别/构图）{d['shot']}",
        f"（光影氛围）{d['lighting']}",
        f"（风格一致性）{d['style']}",
        f"（节奏与时长）{d['rhythm']}",
        f"（空间关系）{d['spatial']}",
        f"（首尾帧约束）{fmt_frames(d['frames'])}",
    ]
    negative = fmt_negative(d["negative"]) if d.get("negative") else "、".join(DEFAULT_CN_NEGATIVE)
    parts.append(f"（负面提示词）排除{negative}。")

    prompt = "".join(parts)
    if vertical:
        prompt += "\n[竖屏附加逻辑已应用：人物不贴边、动作纵向优先、开篇强钩子、中心安全区构图。]"
    return prompt, negative


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return
    path = args[0]
    vertical = "--no-vertical" not in args

    d = load_data(path)
    prompt, cn_neg = build(d, vertical)
    warns = vertical_warnings(d) if vertical else []

    out = []
    if d.get("label"):
        out.append(f"=== {d['label']} ===")
    out.append(prompt)
    out.append("")
    out.append(f"Negative (CN): 排除{cn_neg}。")
    out.append(f"Negative (EN): {EN_NEGATIVE}")
    if warns:
        out.append("")
        out.append("⚠ 竖屏检查建议：")
        for w in warns:
            out.append(f"  - {w}")
    print("\n".join(out))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Assemble a validated image-to-video (I2V) storyboard prompt.

Reads a JSON describing the 10 mandatory elements, applies vertical-screen logic,
validates completeness, and prints a copy-ready prompt plus an EN negative list.

Usage:
    python3 generate_prompt.py shot.json
    python3 generate_prompt.py shot.json --no-vertical
    python3 generate_prompt.py shot.json --preset moji   # 套用末日废墟风格 + 专属负面词
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
  "negative": ["模糊","变形",...],        # 负面提示词 (list or str)
  "plot":    "少女为复仇潜入雨夜古堡...", # 剧情提示词层 (可选)
  "images":  [                            # 分镜图 1-10 张 (可选)
    {"role": "首帧图", "file": "shot01.png", "caption": "人物静立持剑"},
    {"role": "参考图", "file": "ref.png",   "caption": "身份锁定"}
  ]
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


PRESETS = {
    "guofeng":  {"style": "国风漫剧、厚涂笔触、电影感、细节丰富、统一美术风格"},
    "houqi":    {"style": "厚涂、日式动漫、赛璐璐、电影感、统一美术风格"},
    "render3d": {"style": "3D 渲染、虚幻引擎风格、光线追踪、电影级调色、8K"},
    "xieshi":   {"style": "写实、胶片感、电影级调色、细节丰富、高质感"},
    "moji":     {"style": "末日废墟城市，断壁残垣崩塌高楼，锈蚀残破建筑，荒草丛生藤蔓缠绕，"
                          "废弃破碎街道，灰蒙蒙沙尘弥漫，低饱和冷色调，阴郁压抑末世氛围，"
                          "电影级光影，8K 超高清，极致细节，写实质感，广角全景，死寂无人空城",
                "negative": "漂浮的物体，反重力，人物穿模，四肢扭曲，动作僵硬，表情崩坏，"
                            "多余的手指，畸形的身体，干净整洁的建筑，没有锈迹，没有灰尘，"
                            "明亮鲜艳的色彩，现代完好的车辆，正常的行人，蓝天白云，阳光明媚，"
                            "卡通风格，二次元，低分辨率，模糊，噪点过多，水印，文字"},
}


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

    # plot layer (剧情提示词) — prepend once
    plot = str(d.get("plot", "")).strip()
    if plot:
        prompt = f"【剧情】{plot}\n\n" + prompt

    # storyboard images (1-10 张) — append upload map
    imgs = d.get("images") or []
    if imgs:
        lines = ["【分镜图上传】"]
        for im in imgs:
            role = im.get("role", "参考图")
            file = im.get("file", "")
            cap = im.get("caption", "")
            lines.append(f"  - （{role}）{cap}" + (f"（文件：{file}）" if file else ""))
        prompt += "\n" + "\n".join(lines)
    return prompt, negative


def main():
    raw = sys.argv[1:]
    if not raw or raw[0] in ("-h", "--help"):
        print(__doc__)
        return
    path = None
    vertical = True
    preset = None
    i = 0
    while i < len(raw):
        a = raw[i]
        if a == "--no-vertical":
            vertical = False
        elif a == "--preset":
            preset = raw[i + 1]
            i += 2
            continue
        elif path is None:
            path = a
        i += 1
    if path is None:
        print("用法：python3 generate_prompt.py shot.json [--preset moji] [--no-vertical]")
        return

    d = load_data(path)
    if preset:
        p = PRESETS.get(preset)
        if not p:
            print("未知预设：%s（可选：%s）" % (preset, " / ".join(PRESETS)))
            return
        if not d.get("style"):
            d["style"] = p.get("style", "")
        if "negative" in p and not d.get("negative"):
            d["negative"] = p["negative"]
    prompt, cn_neg = build(d, vertical)
    warns = vertical_warnings(d) if vertical else []
    imgs = d.get("images") or []
    if len(imgs) > 10:
        warns.append(f"分镜图共 {len(imgs)} 张，超过建议上限 10 张，请拆分或精简。")

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

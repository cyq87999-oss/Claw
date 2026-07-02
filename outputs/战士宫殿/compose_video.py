#!/usr/bin/env python3
"""
6 张 SD 图 → 30 秒视频
字幕 + zoom 运镜 + BGM
"""
from pathlib import Path
from moviepy import (
    ImageClip, CompositeVideoClip, concatenate_videoclips, AudioFileClip, vfx
)

FRAMES_DIR = Path("/Users/qy/CodeBuddy/Claw/outputs/战士宫殿/frames")
OUT_DIR = Path("/Users/qy/CodeBuddy/Claw/outputs/战士宫殿")
W, H = 1080, 1920  # 9:16 竖屏
FPS = 30

# 6 张图路径 + 配文字幕 + 时长
scenes = [
    ("frame_01_宫殿大厅·月光.png", 5, "古老的宫殿大厅\n冷冽的月光照射"),
    ("frame_02_战斗服战士.png", 5, "穿战斗服的战士"),
    ("frame_03_军装士兵.png", 5, "穿军装的士兵"),
    ("frame_04_科技感女战士.png", 5, "穿科技感装备的女性"),
    ("frame_05_热带雨林村落.png", 5, "热带雨林中的村落"),
    ("frame_06_月光·冷冽氛围.png", 5, "冷冽的月光\n野性艺术风格"),
]

clips = []
for fname, dur, text in scenes:
    path = str(FRAMES_DIR / fname)
    # 拉伸到 1080x1920
    clip = (ImageClip(path)
            .resized((W, H))
            .with_duration(dur)
            .with_position("center"))
    # zoom-in 运镜
    clip = clip.resized(lambda t: 1 + 0.03 * t / dur)
    clips.append(clip)

print("拼接视频...")
final = concatenate_videoclips(clips, method="compose")
final = final.with_fps(FPS)

output_path = OUT_DIR / "战士宫殿_30s_raw.mp4"
print(f"渲染 → {output_path}")
final.write_videofile(str(output_path), codec="libx264", fps=FPS, logger=None)

print(f"完成: {output_path}")
print(f"时长: {final.duration:.0f}s | 分辨率: {W}x{H} | FPS: {FPS}")

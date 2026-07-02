#!/usr/bin/env python3
"""
战士/宫殿/月光 主题 - 6 镜生图
基于 SD 1.5 + MPS（Mac GPU）
"""
import torch
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from pathlib import Path

# 设备
device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"使用设备: {device}")

# 加载 SD 1.5
model_path = Path.home() / "sd-lora-project" / "models" / "sd-v1-5" / "v1-5-pruned-emaonly.safetensors"
print(f"加载模型: {model_path}")

pipe = StableDiffusionPipeline.from_single_file(
    str(model_path),
    torch_dtype=torch.float16 if device == "mps" else torch.float32,
    safety_checker=None,
)
pipe = pipe.to(device)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# 6 镜分镜 - 战士+宫殿+月光+雨林
shots = [
    {
        "id": "01",
        "title": "宫殿大厅·月光",
        "prompt": "ancient palace grand hall interior, cold moonlight streaming through tall arched windows, marble floor with reflections, cinematic composition, photorealistic, 8k, ultra detail, volumetric light, atmospheric haze",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, deformed"
    },
    {
        "id": "02",
        "title": "战斗服战士",
        "prompt": "a warrior in futuristic battle suit, scarred face, intense eyes, full body shot, standing in moonlight, photorealistic, hyper detailed, cinematic lighting, 8k, raw photo, shot on Sony A7R IV",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, deformed, plastic skin"
    },
    {
        "id": "03",
        "title": "军装士兵",
        "prompt": "a soldier in modern military uniform, weathered face, serious expression, medium close-up, dramatic cold lighting, photorealistic, hyper detailed, 8k, raw photo, documentary style",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, deformed"
    },
    {
        "id": "04",
        "title": "科技感女战士",
        "prompt": "a female warrior in high-tech sci-fi armor, glowing cyan accents, short hair, determined expression, half body shot, neon teal lighting, photorealographic, hyper detailed, 8k, cyberpunk meets fantasy",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, deformed, plastic skin"
    },
    {
        "id": "05",
        "title": "热带雨林村落",
        "prompt": "tropical rainforest village, wooden huts on stilts, misty atmosphere, dense jungle canopy, golden hour light filtering through leaves, photorealistic, 8k, ultra detail, National Geographic style",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, modern buildings"
    },
    {
        "id": "06",
        "title": "月光·冷冽氛围",
        "prompt": "wild landscape under cold moonlight, rocky terrain, ancient ruins silhouette, dramatic cold blue lighting, atmospheric fog, photorealistic, 8k, ultra detail, cinematic, wild art style",
        "negative": "blurry, low quality, cartoon, anime, watermark, text, colorful"
    },
]

# 输出
output_dir = Path("/Users/qy/CodeBuddy/Claw/outputs/战士宫殿/frames")
output_dir.mkdir(parents=True, exist_ok=True)

print(f"\n开始生成 {len(shots)} 张关键帧...")
for i, shot in enumerate(shots):
    print(f"\n[{i+1}/{len(shots)}] {shot['title']}")
    print(f"  prompt: {shot['prompt'][:80]}...")

    image = pipe(
        prompt=shot["prompt"],
        negative_prompt=shot["negative"],
        num_inference_steps=20,
        guidance_scale=7.5,
        height=512,
        width=512,
    ).images[0]

    output_path = output_dir / f"frame_{shot['id']}_{shot['title']}.png"
    image.save(output_path)
    print(f"  ✅ 已保存: {output_path}")

print(f"\n✅ 全部完成！输出目录: {output_dir}")

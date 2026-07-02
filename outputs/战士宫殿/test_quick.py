#!/usr/bin/env python3
import torch, sys
from diffusers import StableDiffusionPipeline, DPMSolverMultistepScheduler
from pathlib import Path

device = "mps" if torch.backends.mps.is_available() else "cpu"
print(f"设备: {device}")
torch_dtype = torch.float16 if device == "mps" else torch.float32

model_path = str(Path.home() / "sd-lora-project" / "models" / "sd-v1-5" / "v1-5-pruned-emaonly.safetensors")
print(f"加载: {model_path}")

pipe = StableDiffusionPipeline.from_single_file(
    model_path, torch_dtype=torch_dtype, safety_checker=None
)
pipe = pipe.to(device)
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

prompt = "ancient palace hall, cold moonlight, cinematic, photorealistic"
print(f"生成: {prompt}")
image = pipe(prompt=prompt, num_inference_steps=20, guidance_scale=7.5, height=512, width=512).images[0]

out = Path("/Users/qy/CodeBuddy/Claw/outputs/战士宫殿/test_first.png")
image.save(out)
print(f"完成: {out}")

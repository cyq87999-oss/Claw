# 战士/宫殿/月光 - 6 镜 SD 提示词

**模型**: SD 1.5 / SDXL / Realistic Vision / DreamShaper 通用
**分辨率**: 512x768 (竖屏) 或 768x512 (横屏)
**Steps**: 25-30 | **CFG**: 7-8 | **Sampler**: DPM++ 2M Karras

---

## 镜 1 · 宫殿大厅·冷冽月光
**EN**:
```
ancient palace grand hall interior, cold moonlight streaming through tall arched windows, marble floor with reflections, cinematic composition, photorealistic, 8k, ultra detail, volumetric light, atmospheric haze, masterpiece, best quality
Negative: blurry, low quality, cartoon, anime, watermark, text, deformed
```

## 镜 2 · 战斗服战士
**EN**:
```
a warrior in futuristic battle suit, scarred face, intense eyes, full body shot, standing in moonlight, photorealistic, hyper detailed, cinematic lighting, 8k, raw photo, shot on Sony A7R IV
Negative: blurry, low quality, cartoon, anime, watermark, text, deformed, plastic skin
```

## 镜 3 · 军装士兵
**EN**:
```
a soldier in modern military uniform, weathered face, serious expression, medium close-up, dramatic cold lighting, photorealistic, hyper detailed, 8k, raw photo, documentary style, masterpiece
Negative: blurry, low quality, cartoon, anime, watermark, text, deformed
```

## 镜 4 · 科技感女战士
**EN**:
```
a female warrior in high-tech sci-fi armor, glowing cyan accents, short hair, determined expression, half body shot, neon teal lighting, photorealistic, hyper detailed, 8k, cyberpunk meets fantasy, masterpiece
Negative: blurry, low quality, cartoon, anime, watermark, text, deformed, plastic skin
```

## 镜 5 · 热带雨林村落
**EN**:
```
tropical rainforest village, wooden huts on stilts, misty atmosphere, dense jungle canopy, golden hour light filtering through leaves, photorealistic, 8k, ultra detail, National Geographic style, masterpiece
Negative: blurry, low quality, cartoon, anime, watermark, text, modern buildings
```

## 镜 6 · 冷冽月光·野性艺术
**EN**:
```
wild landscape under cold moonlight, rocky terrain, ancient ruins silhouette, dramatic cold blue lighting, atmospheric fog, photorealistic, 8k, ultra detail, cinematic, wild art style, masterpiece
Negative: blurry, low quality, cartoon, anime, watermark, text, colorful
```

---

## 跑图步骤

### ComfyUI
1. Load Checkpoint: v1-5-pruned-emaonly.safetensors
2. CLIP Text Encode: 粘贴正面提示词
3. CLIP Text Encode (Negative): 粘贴负面提示词
4. KSampler: steps=25, cfg=7, sampler=dpmpp_2m
5. Empty Latent: 512x768
6. VAE Decode -> Save Image

### 即梦 / 可灵 (在线)
直接复制 English 到提示词框, 选"写实"风格。

### 网络通后我立刻能跑
```
python3 -m pip install "transformers==4.45.0" "diffusers==0.30.0" "accelerate==0.34.0"
python3 /Users/qy/CodeBuddy/Claw/outputs/战士宫殿/generate_warrior.py
```

跑完 6 张图后我自动拼 30 秒视频(zoom 运镜+字幕+配音)。

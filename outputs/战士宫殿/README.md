# 战士/宫殿/月光 主题 - 交付清单

## 状态: 部分交付
本地 SD 跑图卡在 transformers/diffusers 兼容 + 网络不通。

## 已交付
- `SD提示词_6镜.md` - 6 段精调中英双版提示词
- `generate_warrior.py` - 跑图脚本(等网络通即跑)
- `frames/` - 待生成

## 等您操作恢复
1. 网络通后:
   ```
   python3 -m pip install "transformers==4.45.0" "diffusers==0.30.0" "accelerate==0.34.0"
   python3 /Users/qy/CodeBuddy/Claw/outputs/战士宫殿/generate_warrior.py
   ```
2. 或者手动到 ComfyUI 跑图 (复制 SD提示词_6镜.md 里的 EN 提示词)

## 后续 (跑图后)
- 6 张图 -> 30 秒视频 (zoom 运镜+字幕+配音)
- 视频 -> 抖音/B站发布包

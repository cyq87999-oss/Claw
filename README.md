# i2v-storyboard-prompt · 图生视频分镜提示词技能

把角色 / 道具 / 场景图变成可直接投喂视频模型的**图生视频分镜提示词**（9:16 竖屏短视频）。

## 核心能力

- **10 要素强制骨架** —— 主体锁定 / 动作描述 / 镜头运动 / 景别构图 / 光影氛围 / 风格一致性 / 节奏时长 / 空间关系 / 首尾帧约束 / 负面提示词，缺一不可
- **5 条实操铁律** —— 角色一致性优先 / 运镜描述精准（轨迹按秒焊死角度）/ 单核心动作 / 音效与画面绑定 / 分层调试策略
- **1–10 张分镜图 + 剧情层** —— 首帧图 / 尾帧图 / 参考图角色卡，配合一句话梗概、情绪曲线、分场清单，多镜不断人设
- **运镜 × 视觉特效词库** —— 内置词库自由组合，支持「融合 → 进化」两步法创新出全新运镜 / 特效
- **兼容平台** —— 即梦 / Kling 可灵 / Wan / Seedance / Runway

## 网页版生成器

`assets/webapp/index.html` —— 10 要素分镜提示词生成器（单文件 HTML）：

- 单镜生成 / 多镜序列 / 打斗版 / 创新实验室 / 剧情工坊（多集管理 + 分镜图）
- AI 接入：本地 Ollama（免 Key）或 DeepSeek / SiliconFlow / Groq / 通义 / Moonshot（填 Key）
- `scripts/serve.py` 提供本地代理，解决浏览器直连 Ollama 的跨域问题

```bash
# 方式一：直接双击打开 index.html（用云端 API 时）
# 方式二：本地 Ollama 需走代理
python scripts/serve.py   # 然后打开提示的本地地址
```

## 安装为 CodeBuddy Skill

```bash
git clone https://github.com/cyq87999-oss/Claw.git
cp -r Claw/.codebuddy/skills/i2v-storyboard-prompt ~/.codebuddy/skills/
```

## 目录结构

```
i2v-storyboard-prompt/
├── SKILL.md            # 技能主文档：10 要素骨架 + 5 铁律 + 工作流
├── references/         # 词库与创新方法（运镜/特效/融合进化）
├── scripts/            # serve.py 本地代理等脚本
└── assets/webapp/      # index.html 网页版生成器
```

## License

MIT

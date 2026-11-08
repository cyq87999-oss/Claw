/* 站点导航与本地搜索索引：唯一数据源，改这里即可增删栏目 */
window.SITE_NAV = [
  {
    group: 'CLAW 文档',
    flatGroup: true,
    items: [
      { t: '首页', p: '', id: 'home' }
    ]
  },
  {
    group: '快速上手',
    items: [
      { t: '快速开始', p: 'quick-start/', id: 'quick-start' },
      { t: '模型配置', p: 'models/', id: 'models' },
      { t: '选择工作台', p: 'workspace/', id: 'workspace' }
    ]
  },
  {
    group: '分镜规格',
    items: [
      { t: '8 行一镜到底规格', p: 'spec/', id: 'spec' },
      { t: '逐镜剧本与情绪弹簧', p: 'storyboard/', id: 'storyboard' }
    ]
  },
  {
    group: '视频生成',
    items: [
      { t: '生成工具总览', p: 'video/', id: 'video' },
      { t: '花夕 Web 生成器', p: 'video/#huaxi', id: 'v-huaxi', noPager: true },
      { t: '幕匠创作导演', p: 'video/#mujiang', id: 'v-mujiang', noPager: true },
      { t: '短剧自动化工厂', p: 'video/#auto-drama', id: 'v-autodrama', noPager: true },
      { t: 'ComfyUI 与锁脸', p: 'video/#comfyui', id: 'v-comfyui', noPager: true }
    ]
  },
  {
    group: '环境与排障',
    items: [
      { t: '本地环境与部署', p: 'environment/', id: 'environment' },
      { t: '常见问题', p: 'help/', id: 'help' }
    ]
  }
];

window.SITE_INDEX = [
  { t: '文档首页', p: '', k: '总览 入口 开始 导航 栏目', d: 'Claw 创作工作台文档的总入口。' },
  { t: '快速开始', p: 'quick-start/', k: '第一步 上手 流程 生成 复制 预览', d: '从一段剧情到一条可投喂的 8 行提示词。' },
  { t: '模型配置', p: 'models/', k: 'Ollama gemma4 8771 api/chat 代理 本地模型', d: '本地 8771 代理与 Ollama 模型的连接方式。' },
  { t: '选择工作台', p: 'workspace/', k: '分镜工作台 逐镜 图生视频 提示词 工作区', d: '按任务类型选择对应工作台。' },
  { t: '8 行一镜到底规格', p: 'spec/', k: '竖屏 9:16 一镜到底 无字幕 零硬切 胶片颗粒 128dB 首帧 尾帧 负面提示词', d: '固定 8 行的成品视频提示词硬规格与逐行说明。' },
  { t: '逐镜剧本与情绪弹簧', p: 'storyboard/', k: '分镜 剧本 情绪弹簧 强钩 尾钩 台词 景别 信息差', d: '剧情拆成竖屏分镜的固定字段与节奏纪律。' },
  { t: '生成工具总览', p: 'video/', k: '花夕 huaxi 幕匠 mujiang auto-drama ComfyUI 图生视频 可灵 xjai', d: '仓库内几个视频创作项目的定位与入口。' },
  { t: '本地环境与部署', p: 'environment/', k: 'server_proxy.py 8771 Desktop GitHub Pages 静态站 端口', d: '本地服务拓扑、静态站预览与 Pages 发布。' },
  { t: '常见问题', p: 'help/', k: '乱码 缓存 卡顿 旧标签 刷新 no-store 批量生成', d: '页面残留旧提示词、卡顿、缓存不更新的排查。' }
];

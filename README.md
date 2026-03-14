# Feishu Voice - 飞书语音消息技能

为 OpenClaw Agent 提供飞书语音消息生成、格式转换和发送能力的技能包。

## 功能特性

- 🎙️ **TTS 语音生成**：支持中文语音合成，默认使用小云声音（zh-CN-XiaoyiNeural）
- 🔄 **音频格式转换**：自动将 mp3 转换为飞书支持的 opus/amr 格式
- 📤 **飞书消息发送**：一键发送语音消息到飞书聊天
- 💰 **完全免费**：使用 Edge TTS，无需 API Key，无需付费

## 免费语音合成

本技能使用 **Edge TTS** 进行语音合成，具有以下优势：

| 特性 | 说明 |
|------|------|
| 💰 **完全免费** | 无需 API Key，无需付费，无使用限制 |
| 🌐 **在线服务** | 使用微软 Edge 在线 TTS 服务 |
| 🔊 **高质量语音** | 接近真人的自然语音效果 |
| 🌍 **多语言支持** | 支持中文、英文等多种语言 |
| ⚡ **快速生成** | 几秒内完成语音合成 |

### 内置默认声音：小云

本技能内置了小云的默认声音配置，开箱即用：

```json
{
  "voice": "zh-CN-XiaoyiNeural",
  "style": "年轻女管家风格",
  "rate": "-3%",
  "pitch": "+1Hz",
  "description": "自然、温柔、清甜、稳重"
}
```

**声音特点：**
- 🎀 年轻女声，略带甜美
- 💁 管家式服务风格
- 🌸 自然温柔，不播音腔
- 🎵 语速适中，音高略高

## 安装方法

```bash
# 方式一：通过 skillhub 安装
skillhub install feishu-voice

# 方式二：通过 clawhub 安装
clawhub install feishu-voice

# 方式三：手动安装
git clone https://github.com/biayunT/feishu-voice.git
cp -r feishu-voice/* ~/.openclaw/skills/feishu-voice/
```

## 使用场景

当出现以下情况时，Agent 会自动触发此技能：

| 触发场景 | 示例请求 |
|---------|---------|
| 用户要求语音回复 | "语音回复告诉我今天天气" |
| 发送语音消息 | "给张三发条语音" |
| 音频格式转换 | "把这个 mp3 转成飞书能用的格式" |
| 中文 TTS 生成 | "把这段文字转成语音" |

## 工作流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  生成 TTS   │ -> │  格式转换   │ -> │  发送消息   │
│  (mp3)      │    │  (opus)     │    │  (飞书)     │
└─────────────┘    └─────────────┘    └─────────────┘
     ↓
 使用小云默认声音
 zh-CN-XiaoyiNeural
```

### 详细步骤

**Step 1: 生成 TTS 语音**

使用 `tts` 工具生成语音文件（默认使用小云声音）：

```
tts: text="今天长沙天气晴朗，最高温度24度"
```

输出：`\tmp\openclaw\tts-xxxxx\voice-xxxxx.mp3`

**Step 2: 转换音频格式**

飞书语音消息不支持 mp3 格式，需要转换为 opus：

```bash
ffmpeg -y -i "input.mp3" -c:a libopus -b:a 32k "output.opus"
```

**Step 3: 发送语音消息**

使用 `message` 工具发送：

```json
{
  "action": "send",
  "channel": "feishu",
  "media": "output.opus",
  "mimeType": "audio/opus"
}
```

## 音频格式支持

| 格式 | MIME 类型 | 比特率 | 说明 |
|------|----------|--------|------|
| opus | audio/opus | 32kbps | **推荐格式**，音质最佳 |
| amr | audio/amr | 12.2kbps | 传统格式，兼容性好 |
| ogg | audio/ogg | 32kbps | 替代容器格式 |
| mp3 | - | - | ❌ 飞书不支持 |

## 配置文件

技能包含 `config.json` 配置文件，可以自定义默认行为：

```json
{
  "defaultVoice": {
    "engine": "edge-tts",
    "voice": "zh-CN-XiaoyiNeural",
    "rate": "-3%",
    "pitch": "+1Hz"
  },
  "formatConversion": {
    "defaultFormat": "opus",
    "defaultBitrate": "32k"
  }
}
```

### 可用语音列表

除了默认的小云声音，还可以使用以下中文语音：

| 语音 ID | 特点 |
|---------|------|
| zh-CN-XiaoyiNeural | 晓伊 - 年轻女声（小云默认） |
| zh-CN-XiaoxiaoNeural | 晓晓 - 温柔女声 |
| zh-CN-YunxiNeural | 云希 - 活力男声 |
| zh-CN-YunyangNeural | 云扬 - 专业男声 |
| zh-CN-XiaochenNeural | 晓辰 - 成熟女声 |
| zh-CN-XiaohanNeural | 晓涵 - 知性女声 |

## 脚本工具

### convert_to_opus.py

音频格式转换脚本，位于 `scripts/convert_to_opus.py`

**使用方法：**

```bash
# 基本用法
python convert_to_opus.py input.mp3

# 指定输出文件
python convert_to_opus.py input.mp3 output.opus

# 在 Python 代码中使用
from convert_to_opus import convert_to_opus
output_path = convert_to_opus("input.mp3", bitrate="32k")
```

## 依赖要求

- **ffmpeg**：用于音频格式转换（免费开源）
- **OpenClaw**：运行环境，需支持 TTS 工具
- **Edge TTS**：语音合成服务（免费，无需 API Key）

检查 ffmpeg 是否安装：

```bash
ffmpeg -version
```

## 文件结构

```
feishu-voice/
├── SKILL.md                    # 技能主文档（Agent 加载）
├── README.md                   # 项目说明（本文档）
├── config.json                 # 默认配置文件
├── scripts/
│   └── convert_to_opus.py      # 音频转换脚本
└── references/
    └── formats.md              # 格式详细参考
```

## 快速开始

1. 安装技能
2. 确保系统已安装 ffmpeg
3. 直接使用，无需配置

```bash
# 安装
skillhub install feishu-voice

# 使用（Agent 会自动调用）
# 用户："语音回复告诉我今天天气"
```

## 常见问题

### Q: TTS 是免费的吗？

A: 是的！本技能使用 Edge TTS，完全免费，无需 API Key，无使用限制。

### Q: 为什么发送的语音消息飞书不显示？

A: 飞书不支持 mp3 格式的语音消息，必须先转换为 opus/amr 格式。

### Q: 如何修改默认语音？

A: 修改 `config.json` 中的 `defaultVoice.voice` 字段为其他语音 ID。

### Q: ffmpeg 转换失败怎么办？

A: 检查输入文件是否存在，路径是否正确。使用完整路径避免路径问题。

### Q: 可以自定义声音参数吗？

A: 可以！在 `config.json` 中调整 `rate`（语速）和 `pitch`（音高）参数。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

**仓库地址**：https://github.com/biayunT/feishu-voice

---

**作者**：小云 ☁️  
**默认声音**：zh-CN-XiaoyiNeural（晓伊）
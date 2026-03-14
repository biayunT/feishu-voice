# Feishu Voice - 飞书语音消息技能

为 OpenClaw Agent 提供飞书语音消息生成、格式转换和发送能力的技能包。

## 功能特性

- 🎙️ **TTS 语音生成**：支持中文语音合成，默认使用 `zh-CN-XiaoyiNeural` 女声
- 🔄 **音频格式转换**：自动将 mp3 转换为飞书支持的 opus/amr 格式
- 📤 **飞书消息发送**：一键发送语音消息到飞书聊天

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
```

### 详细步骤

**Step 1: 生成 TTS 语音**

使用 `tts` 工具生成语音文件：

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

- **ffmpeg**：用于音频格式转换
- **OpenClaw**：运行环境，需支持 TTS 工具

检查 ffmpeg 是否安装：

```bash
ffmpeg -version
```

## 文件结构

```
feishu-voice/
├── SKILL.md                    # 技能主文档（Agent 加载）
├── README.md                   # 项目说明（本文档）
├── scripts/
│   └── convert_to_opus.py      # 音频转换脚本
└── references/
    └── formats.md              # 格式详细参考
```

## 配置建议

在 `TOOLS.md` 中添加以下配置，避免每次都要手动指定参数：

```markdown
## 飞书语音消息

- **格式要求**：飞书语音消息不支持 mp3，需使用 opus/amr/ogg 格式
- **推荐格式**：opus (32kbps)
- **转换命令**：`ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k output.opus`
- **发送方式**：使用 message 工具，`mimeType: "audio/opus"`
- **重要提示**：发送语音前必须转换格式，不要直接发送 mp3
```

## 常见问题

### Q: 为什么发送的语音消息飞书不显示？

A: 飞书不支持 mp3 格式的语音消息，必须先转换为 opus/amr 格式。

### Q: ffmpeg 转换失败怎么办？

A: 检查输入文件是否存在，路径是否正确。使用完整路径避免路径问题。

### Q: 如何修改默认语音？

A: 在 TTS 调用时指定不同的语音参数，或在 SKILL.md 中修改默认配置。

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

**仓库地址**：https://github.com/biayunT/feishu-voice
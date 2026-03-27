# Feishu Voice - 飞书语音消息技能

为 OpenClaw Agent 提供飞书语音消息生成、格式转换和发送能力的技能包。

## 功能特性

- 🎙️ **中文 TTS 语音生成**：默认使用小云声音（`zh-CN-XiaoyiNeural`）
- 🔄 **音频格式转换**：自动将 mp3 转换为飞书支持的 OPUS
- 📤 **飞书语音发送**：支持通过 OpenClaw Feishu 通道发送语音消息
- 💰 **完全免费**：使用 Edge TTS，无需 API Key，无需付费

## 当前推荐方案（2026-03-27 更新）

### 推荐链路

对于飞书语音发送，当前推荐使用 **OpenClaw Feishu 通道**，而不是默认走飞书开放平台直传。

#### 文字发送

```bash
openclaw message send --channel feishu --target <open_id> --message "文字内容"
```

#### 语音发送

1. 使用 Edge TTS 生成 mp3
2. 转换为 OPUS
3. 使用 OpenClaw Feishu 通道发送本地媒体

```bash
python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"
ffmpeg -y -loglevel error -i output.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
openclaw message send --channel feishu --target <open_id> --media output.opus
```

## 重要注意事项

### 1. 不要使用 OpenClaw 内置 `tts` 工具生成中文晨报语音
该工具在某些环境下可能默认使用英文语音，导致中文内容被错误读成英文数字。

**推荐方式：**

```bash
python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"
```

### 2. 飞书语音必须使用 OPUS

推荐转换命令：

```bash
ffmpeg -y -loglevel error -i input.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
```

### 3. 本地媒体路径必须在 OpenClaw 允许目录内
如果通过 OpenClaw 发送本地语音文件，媒体路径不能放在任意系统临时目录。

推荐输出目录：

```text
C:\Users\22350\.openclaw\workspace\temp\feishu-voice\
```

否则可能报错：

```text
LocalMediaAccessError: Local media path is not under an allowed directory
```

### 4. 不推荐默认依赖飞书开放平台 App 凭据直传
旧方案依赖：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- tenant_access_token
- 手动上传文件再发消息

这条链路更复杂，也更容易因凭据缺失失败。

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

```json
{
  "voice": "zh-CN-XiaoyiNeural",
  "style": "年轻女管家风格",
  "rate": "-3%",
  "pitch": "+1Hz",
  "description": "自然、温柔、清甜、稳重"
}
```

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

| 触发场景 | 示例请求 |
|---------|---------|
| 用户要求语音回复 | "语音回复告诉我今天天气" |
| 发送飞书语音 | "给飞书发一条语音" |
| 音频格式转换 | "把这个 mp3 转成飞书能用的格式" |
| 中文 TTS 生成 | "把这段文字转成语音" |

## 音频格式支持

| 格式 | MIME 类型 | 说明 |
|------|----------|------|
| opus | audio/opus | **推荐格式** |
| amr | audio/amr | 兼容格式 |
| ogg | audio/ogg | 替代容器 |
| mp3 | - | ❌ 飞书语音不推荐直接发送 |

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

## 脚本工具

### convert_to_opus.py

音频格式转换脚本，位于 `scripts/convert_to_opus.py`

```bash
python convert_to_opus.py input.mp3
python convert_to_opus.py input.mp3 output.opus
```

## 归档

本次飞书晨报链路修复归档见：
- `ARCHIVE-2026-03-27-feishu-brief-fix.md`

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

**仓库地址**：https://github.com/biayunT/feishu-voice

---

**作者**：小云 ☁️  
**默认声音**：zh-CN-XiaoyiNeural（晓伊）

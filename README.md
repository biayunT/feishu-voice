# Feishu Voice - 飞书语音消息技能

用最稳的方式给飞书发语音：**Edge TTS 生成中文语音 + FFmpeg 转 OPUS + OpenClaw Feishu 通道发送**。

## 仓库定位

这个仓库用于 OpenClaw 场景下的飞书语音发送，重点解决三件事：

- 生成自然的中文语音
- 转成飞书真正可用的 OPUS 格式
- 用 OpenClaw Feishu 通道稳定发送，而不是依赖更脆弱的直传链路

## 当前推荐方案（2026-03-27 更新）

### 推荐链路

#### 文本发送

```bash
openclaw message send --channel feishu --target <open_id> --message "文字内容"
```

#### 语音发送

```bash
python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"
ffmpeg -y -loglevel error -i output.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
openclaw message send --channel feishu --target <open_id> --media output.opus
```

## 为什么现在推荐这套方案

旧方案依赖飞书开放平台直传链路：
- `FEISHU_APP_ID`
- `FEISHU_APP_SECRET`
- tenant_access_token
- 上传文件后再发消息

这条链路更复杂，也更容易因为凭据、目录或脚本输出污染而失败。

现在更推荐：
- 本地生成音频
- 本地转 OPUS
- 直接交给 OpenClaw Feishu 通道发送

好处是：
- 依赖更少
- 故障面更小
- 更适合你当前的 OpenClaw 工作流

## 重要注意事项

### 1. 不要使用 OpenClaw 内置 `tts` 工具生成中文晨报语音
在当前环境里，这个工具可能选到英文音色，导致中文内容被读成英文数字。

**正确方式：**

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

现在不再把它作为默认推荐方案。

## 默认语音配置

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

| 场景 | 示例 |
|------|------|
| 飞书语音回复 | "语音回复到飞书" |
| 发送飞书语音 | "给飞书发一条语音" |
| 中文 TTS | "把这段中文转成语音" |
| 音频格式转换 | "把 mp3 转成飞书可用的格式" |
| 晨报语音版 | "生成飞书晨报语音" |

## 音频格式支持

| 格式 | MIME 类型 | 说明 |
|------|----------|------|
| opus | audio/opus | **推荐格式** |
| amr | audio/amr | 兼容格式 |
| ogg | audio/ogg | 替代容器 |
| mp3 | - | ❌ 飞书语音不推荐直接发送 |

## 配置文件

仓库包含 `config.json`：

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

位于 `scripts/convert_to_opus.py`

```bash
python convert_to_opus.py input.mp3
python convert_to_opus.py input.mp3 output.opus
```

## 文档与归档

- `SKILL.md`：Agent 使用说明
- `CHANGELOG.md`：版本与修复记录
- `ARCHIVE-2026-03-27-feishu-brief-fix.md`：本次飞书晨报链路修复归档

## GitHub 首页展示建议

当前仓库首页最适合传达的一句话是：

> 用 Edge TTS + OPUS + OpenClaw Feishu 通道，稳定发送中文飞书语音。

如果后续还要进一步优化首页展示，可以继续补：
- 一张简单流程图
- 一个“30 秒上手”示例
- 一个“常见失败原因”小节

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

**仓库地址**：https://github.com/biayunT/feishu-voice

---

**作者**：小云 ☁️  
**默认声音**：zh-CN-XiaoyiNeural（晓伊）

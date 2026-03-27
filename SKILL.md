---
name: feishu-voice
description: "Generate Chinese voice with Edge TTS, convert audio to OPUS, and send voice messages to Feishu via the OpenClaw Feishu channel. Use when (1) user asks for 飞书语音/语音回复/发送语音到飞书 (2) converting audio for Feishu compatibility (3) generating Chinese TTS with zh-CN-XiaoyiNeural (4) sending local audio files to Feishu through OpenClaw."
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["python", "ffmpeg", "ffprobe"],
      "channels": ["feishu"]
    }
  }
}
---

# Feishu Voice

为 OpenClaw Agent 提供飞书语音消息生成、格式转换和发送能力。

## 当前推荐方案（2026-03-27）

### 推荐链路

1. 使用 `python -m edge_tts` 生成中文 mp3
2. 使用 `ffmpeg` 转换为飞书可接受的 OPUS
3. 使用 OpenClaw Feishu 通道发送本地媒体文件

### 推荐发送方式

**文本：**

```bash
openclaw message send --channel feishu --target <open_id> --message "文字内容"
```

**语音：**

```bash
python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"
ffmpeg -y -loglevel error -i output.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
openclaw message send --channel feishu --target <open_id> --media output.opus
```

## 重要规则

### 1. 中文语音不要使用 OpenClaw 内置 `tts`
在当前环境里，内置 `tts` 工具可能错误选择英文语音，导致中文内容被读成英文数字。

**正确方式：**

```bash
python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"
```

### 2. 飞书语音优先走 OpenClaw 通道
当前稳定方案是：
- 语音本地生成
- 文件转 OPUS
- 通过 OpenClaw Feishu 通道发送

不推荐默认走飞书开放平台直传链路。

### 3. 本地媒体路径必须放在允许目录内
如果通过 OpenClaw 发送本地音频文件，媒体文件必须放在 OpenClaw 允许的目录中。

推荐目录：

```text
C:\Users\22350\.openclaw\workspace\temp\feishu-voice\
```

否则可能报错：

```text
LocalMediaAccessError: Local media path is not under an allowed directory
```

### 4. 飞书语音格式固定为 OPUS
推荐转换命令：

```bash
ffmpeg -y -loglevel error -i input.mp3 -acodec libopus -ac 1 -ar 16000 output.opus
```

## 何时使用

当用户出现以下请求时使用本技能：

- “给飞书发一条语音”
- “语音回复到飞书”
- “把这段中文转成语音发飞书”
- “把 mp3 转成飞书能发的语音格式”
- “生成飞书晨报语音版”

## 推荐执行顺序

1. 确认文本内容
2. 用 `edge_tts` 生成 mp3
3. 转换为 OPUS
4. 确保输出目录在允许范围内
5. 通过 OpenClaw Feishu 通道发送

## 故障排查

### 语音发送失败，但文本发送正常
优先检查：
- 输出文件是否是 OPUS
- 文件路径是否在 OpenClaw 允许目录内
- 是否误用了飞书开放平台凭据直传方案

### `ConvertFrom-Json` 失败
如果脚本模式下使用本技能，注意不要让 `ffmpeg` / `edge_tts` 的控制台输出污染结构化结果。

### 本地媒体被拒绝
如果报：
- `LocalMediaAccessError`

说明文件路径不在允许目录中，改到 workspace 下的 `temp/feishu-voice/` 即可。

## 相关文件

- `README.md`：完整说明
- `CHANGELOG.md`：版本与修复记录
- `ARCHIVE-2026-03-27-feishu-brief-fix.md`：本次飞书晨报链路修复归档
- `scripts/convert_to_opus.py`：音频转换脚本

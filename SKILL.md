---
name: feishu-voice
description: "Generate and send voice messages to Feishu with TTS and audio format conversion. Use when (1) user asks for voice reply/语音回复 (2) sending voice messages to Feishu (3) converting audio for Feishu compatibility (4) generating TTS audio in Chinese (5) other agents need voice message capability. Supports Chinese TTS with zh-CN-XiaoyiNeural voice, converts to opus/amr formats for Feishu compatibility."
---

# Feishu Voice

Generate and send voice messages to Feishu with proper audio format support.

## Quick Start

**Send a voice message:**

```
1. Generate TTS audio using tts tool
2. Convert mp3 to opus format using ffmpeg
3. Send via message tool with mimeType: audio/opus
```

## Workflow

### Step 1: Generate TTS Audio

Use the `tts` tool to generate speech:

```
tts: text="你的语音内容"
```

Output: mp3 file at `\tmp\openclaw\tts-XXXXX\voice-XXXXX.mp3`

**Default Chinese voice settings:**
- Voice: `zh-CN-XiaoyiNeural`
- Style: young female butler, natural and gentle
- Rate: `-3%`, Pitch: `+1Hz`

### Step 2: Convert Audio Format

Feishu voice messages require opus/amr/ogg format (NOT mp3).

**Convert mp3 to opus:**

```bash
ffmpeg -y -i "input.mp3" -c:a libopus -b:a 32k "output.opus"
```

**Alternative formats:**
- AMR: `ffmpeg -y -i input.mp3 -ar 8000 -ab 12.2k output.amr`
- OGG: `ffmpeg -y -i input.mp3 -c:a libopus output.ogg`

### Step 3: Send Voice Message

Use the `message` tool to send:

```json
{
  "action": "send",
  "channel": "feishu",
  "media": "<path-to-opus-file>",
  "mimeType": "audio/opus"
}
```

## Complete Example

**User request:** "语音回复告诉我今天天气"

**Execution:**

```
1. Generate TTS:
   tts: text="今天长沙天气晴朗，最高24度..."

2. Convert format:
   ffmpeg -y -i "\tmp\openclaw\tts-xxx\voice.mp3" -c:a libopus -b:a 32k "\tmp\openclaw\tts-xxx\voice.opus"

3. Send message:
   message: action=send, channel=feishu, media=\tmp\openclaw\tts-xxx\voice.opus, mimeType=audio/opus
```

## Format Reference

| Format | MIME Type | Quality | Notes |
|--------|-----------|---------|-------|
| opus | audio/opus | 32kbps | Recommended, best quality |
| amr | audio/amr | 12.2kbps | Legacy format, lower quality |
| ogg | audio/ogg | 32kbps | Alternative container |

## Important Notes

- **Never send mp3 directly** - Feishu does not recognize mp3 as voice message
- **Always convert to opus/amr** before sending to Feishu
- **Use ffmpeg** for audio conversion (available on this system)
- **After tts tool call**, reply with `NO_REPLY` to avoid duplicate messages

## Resources

### scripts/
- `convert_to_opus.py` - Python script to convert audio to opus format

### references/
- `formats.md` - Detailed format specifications and ffmpeg commands
# Feishu Voice Message Formats

## Supported Formats

Feishu voice messages require specific audio formats. MP3 is NOT supported as a voice message format.

### Recommended: Opus

**Best quality and compatibility for Feishu voice messages.**

```bash
ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k output.opus
```

**Parameters:**
- Codec: `libopus`
- Bitrate: `32k` (good for voice, balances quality and size)
- Sample rate: Auto (preserves original)

**MIME type:** `audio/opus`

### Alternative: AMR

**Legacy format with lower quality, smaller file size.**

```bash
ffmpeg -y -i input.mp3 -ar 8000 -ab 12.2k output.amr
```

**Parameters:**
- Sample rate: `8000` Hz (narrowband)
- Bitrate: `12.2k` (AMR-NB standard)

**MIME type:** `audio/amr`

### Alternative: OGG

**Opus in OGG container.**

```bash
ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k output.ogg
```

**MIME type:** `audio/ogg`

## Format Comparison

| Format | Quality | Size | Compatibility | Notes |
|--------|---------|------|---------------|-------|
| opus | High | Small | Excellent | Recommended |
| amr | Low | Smallest | Good | Legacy format |
| ogg | High | Small | Good | Alternative container |
| mp3 | High | Medium | NOT supported | Do NOT use |

## Voice Quality Settings

### For Speech/TTS

```bash
# Clear voice, optimized for speech
ffmpeg -y -i input.mp3 -c:a libopus -b:a 32k -application voip output.opus
```

### For Music

```bash
# Higher quality for music
ffmpeg -y -i input.mp3 -c:a libopus -b:a 64k -application audio output.opus
```

## Sending to Feishu

After conversion, use the message tool:

```json
{
  "action": "send",
  "channel": "feishu",
  "media": "/path/to/voice.opus",
  "mimeType": "audio/opus"
}
```

## Troubleshooting

### ffmpeg not found

Install ffmpeg or ensure it's in PATH:
```bash
# Windows (with chocolatey)
choco install ffmpeg

# Or download from: https://ffmpeg.org/download.html
```

### Conversion fails

Check input file format:
```bash
ffmpeg -i input.mp3
```

### Voice message not playing

Ensure format is opus/amr/ogg, not mp3.
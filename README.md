# Feishu Voice

Generate and send voice messages to Feishu with TTS and audio format conversion.

## Features

- TTS generation with Chinese voice support
- Audio format conversion (mp3 → opus/amr)
- Send voice messages to Feishu

## Installation

```bash
skillhub install feishu-voice
# or
clawhub install feishu-voice
```

## Usage

Use this skill when:
- User asks for voice reply (语音回复)
- Sending voice messages to Feishu
- Converting audio for Feishu compatibility
- Generating TTS audio in Chinese

### Quick Example

```
1. Generate TTS: tts tool with text
2. Convert format: ffmpeg -i input.mp3 -c:a libopus -b:a 32k output.opus
3. Send: message tool with mimeType: audio/opus
```

## Format Support

| Format | MIME Type | Notes |
|--------|-----------|-------|
| opus | audio/opus | Recommended |
| amr | audio/amr | Legacy format |
| ogg | audio/ogg | Alternative |

## Requirements

- ffmpeg (for audio conversion)
- OpenClaw with TTS support

## License

MIT
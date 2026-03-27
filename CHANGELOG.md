# Changelog

## 2026-03-27

### docs: archive feishu brief voice fix and update recommended flow

- 新增 `ARCHIVE-2026-03-27-feishu-brief-fix.md`，归档本次飞书晨报文字+语音链路修复
- README 更新为当前推荐方案：
  - 文本通过 OpenClaw Feishu 通道发送
  - 中文语音通过 `edge_tts` 生成
  - 音频转换为 OPUS
  - 语音文件通过 OpenClaw Feishu 通道发送
- 明确不再推荐默认走飞书开放平台 App ID / App Secret 直传音频
- 明确本地媒体文件必须放在 OpenClaw 允许目录内

## 2026-03-18

### docs: add TTS warning for Chinese voice generation

- 增加说明：不要使用 OpenClaw 内置 `tts` 工具生成中文语音
- 推荐改用 `python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz"`

## 2026-03-17

### feat: add config and detailed Chinese README

- 添加 `config.json`
- README 改为详细中文版
- 内置小云默认声音配置

## Initial release

- 初始飞书语音消息技能仓库

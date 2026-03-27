# 飞书晨报链路修复归档（2026-03-27）

## 背景

本次排障目标是修复“飞书晨报文字已发送，但语音发送失败”的问题。

最初现象：
- 晨报文字版可以发送到飞书
- 语音发送失败，并提示当前环境缺少飞书语音发送所需凭据

## 根因分析

旧方案中，语音发送脚本依赖飞书开放平台直传链路：
- 读取 `FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- 调用 tenant_access_token 接口
- 上传音频文件
- 再发送 audio 消息

这导致以下问题：
1. 凭据缺失时直接失败
2. 链路复杂，调试成本高
3. 与当前 OpenClaw 已经可用的 Feishu 通道重复建设

## 最终修复方案

改为统一走 **OpenClaw Feishu 通道**。

### 当前稳定链路

#### 文字版
- 使用 OpenClaw CLI 发送：
  - `openclaw message send --channel feishu --target <open_id> --message <text>`

#### 语音版
1. 使用 Edge TTS 生成中文 mp3：
   - `python -m edge_tts --voice zh-CN-XiaoyiNeural --rate="-3%" --pitch="+1Hz" --text "内容" --write-media "output.mp3"`
2. 转换为飞书可接受的 OPUS：
   - `ffmpeg -y -loglevel error -i input.mp3 -acodec libopus -ac 1 -ar 16000 output.opus`
3. 使用 OpenClaw CLI 发送：
   - `openclaw message send --channel feishu --target <open_id> --media <opus_path>`

## 关键实现细节

### 1. 不再依赖飞书开放平台 App 凭据
- 不再要求 `FEISHU_APP_ID`
- 不再要求 `FEISHU_APP_SECRET`
- 不再手动获取 tenant_access_token
- 不再手动上传文件到飞书开放平台

### 2. 输出目录必须在 OpenClaw 允许范围内
语音媒体文件不能放在任意系统临时目录。

最终确认可用目录：
- `C:\Users\22350\.openclaw\workspace\temp\feishu-voice\`

如果输出到不受信任目录，OpenClaw 会报：
- `LocalMediaAccessError: Local media path is not under an allowed directory`

### 3. 语音生成脚本输出必须干净
在脚本中需要压制 `edge_tts` / `ffmpeg` 的控制台噪音，避免污染 JSON 输出。
否则外层脚本解析 `ConvertFrom-Json` 会失败。

## 涉及脚本

实际使用的脚本位于：
- `D:\openclaw-qq-bridge-portable\daily-tech-summary.ps1`
- `D:\openclaw-qq-bridge-portable\daily-tech-summary-feishu.ps1`
- `D:\openclaw-qq-bridge-portable\send-feishu-brief-voice.ps1`

## 验证结果

已验证通过：
- OpenClaw Gateway 正常
- Feishu 文本发送正常
- 语音生成正常
- OPUS 发送正常
- 飞书端可以正常收到晨报语音

## 建议

后续在 feishu-voice 技能说明中，建议明确增加：
1. 中文语音优先使用 `edge_tts`，不要依赖可能选错英文音色的简化路径
2. 飞书语音优先通过 OpenClaw Feishu 通道发送，而不是默认走开放平台直传
3. 本地媒体发送时，输出目录要放在 OpenClaw 允许的路径下
4. 对脚本型输出，尽量保证 stdout 只输出结构化结果

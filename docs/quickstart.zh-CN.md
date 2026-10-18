# Saydelta 中文快速入门

把英文旁白录音和原稿放在一起，生成一个可离线打开的审校页面。点击疑点即可试听附近声音，记录需要重录的位置和备注。它适合检查普通词汇的英文合成旁白，不能保证识别结果正确，也不负责音质和发音评分。

## 先看真实示例

直接用浏览器打开仓库中的 `examples/garden-review-v2.html`，无需安装。示例录音约 47 秒，**人为设置了漏句、one→two、重复一句**，不是自然错误率调查。原始输入是 `examples/garden.wav` 和 `examples/garden.txt`，具体编辑记录在 `examples/edits.json`。

点击 **Listen to context** 试听；**Needs another take** 表示需要重录，**Sounds right** 表示声音正确，**Leave open** 保留待判断。**Save decisions** 导出决定和备注，**Load decisions** 恢复同一份报告的决定。浏览器本地保存不等于备份。

## 用自己的录音

需要 Python 3.10 或更新版本。在下载或克隆的项目目录中执行：

```sh
python -m venv .venv
```

Windows 激活：`.venv\Scripts\activate`；macOS/Linux 激活：`source .venv/bin/activate`。然后：

```sh
python -m pip install -e ".[asr]"
saydelta fetch-model models/small.en
saydelta check examples/garden.wav examples/garden.txt --model models/small.en --offline -o my-review.html
```

如果 PowerShell 不允许激活脚本，无需更改安全策略：使用 `.venv\Scripts\python.exe -m pip install -e ".[asr]"` 安装，把后续命令中的 `saydelta` 换成 `.venv\Scripts\saydelta.exe` 即可。

`fetch-model` 会下载约 484 MB 的识别模型，显示进度，每个文件最多尝试三次；另有 Python 依赖下载。请使用空目录，下载一次后重复使用。默认使用 CPU，不需要显卡、账号、付费 API 或单独安装 ffmpeg。新环境下载时间受网络影响，不计入处理速度。若失败，错误信息会列出已完成文件；检查网络后换一个空目录重试，或者从[官方文件列表](https://huggingface.co/Systran/faster-whisper-small.en/tree/main)下载 `config.json`、`tokenizer.json`、`vocabulary.txt`、`model.bin` 放在同一目录。不会关闭 TLS 证书验证。

把两个输入路径替换成自己的录音和 UTF-8 纯文本原稿即可。支持 WAV、MP3 等解码器能读取的格式。输出文件已存在时会拒绝覆盖，请换一个文件名。文件上限为 512 MB、20 分钟，原稿上限为 100,000 字符；上限不表示所有长度和音频条件都已经验证。

模型已下载在本地时，可完全禁止联网下载：

```sh
saydelta check recording.wav script.txt --model /path/to/small.en --offline -o review.html
```

`--model` 指向完整的 CTranslate2 模型目录。直接使用缓存模型时可只加 `--offline`。如提示模型不可用，先正常运行一次完成下载。CUDA 是可选项；本次 Windows 环境缺少所需 CUDA 库，因此所有验证使用 CPU。

## 结果意味着什么

疑点是“识别结果与原稿不同”，必须试听再决定。模型重新识别后与原稿一致的片段保留在 **Rechecks** 中，并未删除。没有疑点不等于录音完全正确。人名、专业词、口音、噪声和人声有声书容易产生误报；公开人声样本未达到本项目的验证门槛。

HTML 包含完整原稿和压缩的单声道试听音频，原录音不变。分享 HTML 就是在分享这些内容。报告无遥测、不请求网络资源；识别在本地进行。决定 JSON 包含你的备注，不包含音频。

当前已在 Windows / Python 3.12 和 3.14 实测；其他系统尚未实测。独立复现遇到默认模型缓存下载路径的 SSL 中断，因此推荐上述独立下载步骤。受控实验与真实用户采用是不同阶段，项目尚无用户留存或传播证据。

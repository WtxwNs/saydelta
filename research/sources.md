# Selection evidence — retrieved 2026-10-19

No author advertising is counted as independent user adoption. Repo capabilities below are source/README observations unless a local test is named.

## Attention snapshot
GitHub Trending [day](https://github.com/trending), [week](https://github.com/trending?since=weekly), [month](https://github.com/trending?since=monthly). Raw pages and parsed lists saved locally. Day succeeded on retry. Examples (counts change between requests):

| Repository | Window growth displayed | Cumulative stars in same response |
|---|---:|---:|
| debpalash/VoiceStudio | 2,098/day | 74,680 |
| debpalash/VoiceStudio | 40,333/month | 74,668 |
| heygen-com/hyperframes | 5,639/week | 66,540 |
| mksglu/context-mode | 4,438/week | 30,669 |
| storytold/artcraft | 18,479/week | 32,448 |

These show attention to local creation and agent workflows, not retention, quality, or an opportunity by themselves. Extreme leaderboard growth is not independently audited. Full lists include other categories; selection was not confined to research tools.

## Original needs and counterevidence
- [VoxCPM #394](https://github.com/OpenBMB/VoxCPM/issues/394), 2026-09-07 (90-day window): a fine-tuner reports repetition, missing beginning words and inconsistent pronunciation in Persian. An English example illustrates the issue; it is not English failure evidence. An independent model-specific report, not market-size evidence.
- [Silero #335](https://github.com/snakers4/silero-models/issues/335), 2026-10-12 (7-day window): a user reports duplicated initial Russian pronouns. This is an upstream defect, but demonstrates a separate source of output mistakes; no claim our English scope solves it.
- [Qwen #372](https://github.com/QwenLM/Qwen3-TTS/issues/372), 2026-09-20 (30-day window): ROCm fine-tuning dependency failure. Reject as a new product opportunity: upstream portability fix.
- [Qwen #375](https://github.com/QwenLM/Qwen3-TTS/issues/375), 2026-09-30: asks about output training rights. Do not infer legal clearance from an unresolved issue.
- [Higgs #117](https://github.com/boson-ai/higgs-audio/issues/117), 2025-08 (historical): user describes generating speech, unloading TTS, using Whisper to locate missing words, then regenerating failures. Concrete existing workflow; not recent growth evidence.
- [Kokoro-FastAPI #224](https://github.com/remsky/Kokoro-FastAPI/issues/224), 2025-03, closed: skipped text from punctuation handling. Historical problem, not a current unresolved bug.
- [Local TTS experience](https://www.reddit.com/r/LocalLLaMA/comments/1vzyuyv/local_tts_models_not_sure_if_this_is_the_place/), 2026-09: original user reports editing input and unfinished/cut words. Supporting qualitative evidence, not a representative survey.
- [TTS feature discussion](https://www.reddit.com/r/TextToSpeech/comments/1vqikxv/what_features_do_you_think_current_tts_services/), 2026-08: a comment describes per-file checks to avoid replaying thousands of clips. Self-selected qualitative evidence.

General issue searches were noisy (TTS also matches a government organization). Saved raw results are not all relevant and their counts must NOT be presented as demand counts. A fresh query returning few issues is not proof of no demand.

## Strong alternatives that constrain selection
- [TTSProof](https://github.com/Mormolykos/ttsproof): MIT; downloaded release 0.4.0 / commit 4f88adf (2026-09-02). Normalization, structural checks, WER and HTML with playback already exist. Source inspection: ASR returns a whole string, reports are per sample; default max duration is 30 seconds, default WER gate 0.03. A fair long-recording comparison must configure its duration limit and separately report structural flags. Its README evaluation is author-reported, not reproduced here.
- [AudioBook-Maker](https://github.com/DigiJoe79/AudioBook-Maker): local integrated generation, Whisper QA, segmentation and review. Requires desktop plus backend/engines; could already suit users creating books inside it. Not run; cannot claim ours is more accurate.
- [tts-audiobook-tool](https://github.com/zeropointnine/tts-audiobook-tool): local TTS generation with quality control and regeneration. Must not claim local TTS quality review is new.
- [Voiceover QA](https://voiceoverqa.com/): most direct workflow alternative. Offers timestamped audio/script comparison; hosted ASR, upload retention described on website. Not run, no paid account or audio upload. Our potential distinction is local, open, portable review of existing recordings, not invention of voiceover QA.
- [OpenScrub](https://github.com/austinmabry/OpenScrub): local video redaction already has OCR, motion tracking and human review. Reject generic video privacy candidate.
- [HTML PDF Compare](https://github.com/ttomohisa/htmlapps-pdf-compare): already advertises inserted-page alignment and browser comparison. [Stirling #6089](https://github.com/Stirling-Tools/Stirling-PDF/issues/6089) closed with feature PR. Reject generic PDF candidate.
- [Test Weakening Guard](https://github.com/marketplace/actions/test-weakening-guard) and [slopsieve](https://www.npmjs.com/package/slopsieve): deterministic diff checks already offered. Reject generic agent-test review candidate.
- [csv-diff issues](https://github.com/simonw/csv-diff/issues): duplicate and composite key complaints are old; many alternatives already support them. A bugfix is insufficient differentiation.

## Dependencies and names
- [Kokoro ONNX](https://github.com/thewh1teagle/kokoro-onnx): MIT code, Apache-2.0 weights per upstream; used only to create controlled test audio. Release model-files-v1.0; voice archive downloaded from model-files-v1.1 after network retry. Not redistributed as a model.
- [faster-whisper base.en](https://huggingface.co/Systran/faster-whisper-base.en): MIT model conversion; revision 3d3d5dee26484f91867d81cb899cfcf72b96be6c observed. Local inference, no reference script in ASR prompt.
- Name checks: CueProof and Readback have clear existing uses; rejected. Exact searches for Saydelta and Sylladiff returned no matching products in this search (not a trademark clearance). Saydelta is a working name only.

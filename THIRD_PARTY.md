# Third-party sources and distribution

Saydelta's original source code and documentation use the MIT license in `LICENSE`. Python wheels contain Saydelta code and its HTML template, not bundled dependency binaries or model weights. Dependencies are installed separately and retain their own licenses. Do not describe the complete dependency stack as MIT-only.

| Component | Version tested | License / source | Use |
|---|---|---|---|
| faster-whisper | 1.2.1 | [MIT](https://github.com/SYSTRAN/faster-whisper/blob/master/LICENSE) | Local recognition |
| CTranslate2 | 4.8.3 | [MIT](https://github.com/OpenNMT/CTranslate2/blob/master/LICENSE) | Recognition runtime |
| small.en conversion | local Systran model | [MIT model card](https://huggingface.co/Systran/faster-whisper-small.en) | Downloaded separately; not in release |
| RapidFuzz | 3.14.6 | [MIT](https://github.com/rapidfuzz/RapidFuzz/blob/main/LICENSE) | Token alignment |
| num2words | 0.5.14 | [LGPL-2.1](https://github.com/savoirfairelinux/num2words/blob/master/COPYING) | Number normalization; unmodified separate Python dependency |
| whisper-normalizer | 0.1.15 | MIT, installed distribution license | English spelling normalization |
| PyAV | 16.1.0 | [BSD-3-Clause](https://github.com/PyAV-Org/PyAV/blob/v16.1.0/LICENSE.txt) | Audio decoding and MP3 listening copies |
| NumPy | 2.5.4 | BSD-3-Clause and bundled-component notices in its distribution | Audio arrays |

PyAV binary wheels contain FFmpeg components, which have their own licenses and build-dependent obligations. This project does not repackage those wheels or their native libraries. Anyone distributing a standalone bundled executable must separately audit those binary dependencies and corresponding source requirements; this release provides Python source/wheel only. Package metadata and upstream license files were checked on 2026-10-19.

## Example audio

The garden script is original Saydelta material. The voice is synthetic Kokoro `af_heart`, generated locally using [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx) 0.6.1 (MIT code) and [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) model assets (Apache-2.0 per upstream model card). Model files were obtained from the project's official model release; they are not redistributed. The demo's deliberate edits are documented in `examples/edits.json`; synthesis and editing instructions are in `research/make_corpus.py` and `research/make_demo.py`.

The original example script, generated garden recording, report and screenshots are provided under the project MIT license to the extent of the contributors' rights. No claim of endorsement by model authors or real speakers is made. These artifacts contain no recorded private conversation.

## Research-only data

The human stress test uses the [hf-internal-testing/librispeech_asr_dummy](https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy) subset of [LibriSpeech](https://www.openslr.org/12), attributed to Vassil Panayotov, Guoguo Chen, Daniel Povey and Sanjeev Khudanpur, under [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/). Fixed rows and concatenation choices are recorded in `research/human_holdout.py`. Raw dataset/audio is excluded from the source release; scripts retrieve it from the stated source. Included human manifests and finding excerpts contain transformed transcriptions from that dataset and retain CC-BY-4.0 attribution, not the project's MIT license. This stress test failed the claimed review-load gate and is retained as counterevidence.

TTSProof 0.4.0 (MIT) was run as a separately installed comparison tool. No competitor source is copied into the product. Competitor repository clones, downloaded model weights, virtual environments and raw research recordings are excluded from the source release.

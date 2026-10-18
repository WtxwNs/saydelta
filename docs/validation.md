# What was tested, and what was not

2026-10-19, Windows, Python 3.12, faster-whisper 1.2.1, CTranslate2 4.8.3, PyAV 16.1.0, `small.en`, CPU int8, six threads, beam 5. VAD and previous-text conditioning disabled. **The expected script never enters recognition.** Current product uses Indel/LCS word anchors and conservative local rechecks.

## Claim and decision rule

For creators reviewing ordinary-vocabulary synthesized English voiceovers against an exact script, Saydelta turns recognition differences into a portable listening inbox. Compared with a transcript plus text diff, the concrete capability is timestamped audition, retained evidence and review decisions in one file. The cost is model download, local processing and human judgment. It is not an automatic correctness certificate.

The [initial protocol](../research/validation-plan.md) was written before experiments: >=90% planted phrase defects localized, <=1 suspect per clean minute, and <=30% audition duration on sparse-fault clips. Human listening time and user preference were not measured. The original broader English-narration scope failed on public human audiobook speech and was explicitly narrowed before the confirmation corpus.

## Controlled results

All clean and altered variants are included. Each altered clip contains one planted omission, repetition or word/number change. “Clean” means no deliberate edit; synthesized speech can still contain natural errors. Every remaining clean finding is conservatively counted as a false alarm, without claiming the sound was certified correct.

| Set | Planted defects located | Clean findings / clean minutes | Maximum audition fraction |
|---|---:|---:|---:|
| Development: 3 scripts, 2 voices | 18/18 | 0 / 4.988 | 28.18% |
| First holdout: 2 scripts, 2 new voices | 11/12 | 1 / 4.965 | 22.89% |
| Confirmation: 1 new script, 3 new voices | 9/9 | 3 / 6.629 | 18.77% |
| Human audiobook stress test | 3/3 | 20 / 3.875 | 54.43% — **fails** |

Synthetic clips span roughly 40–184 seconds. The 20-minute input limit is a resource bound, not evidence that every 20-minute recording has been tested. All synthesis uses one model family, Kokoro; these results do not establish generalization across TTS engines, languages, accents or natural production errors. Some clean findings such as “helped” versus “help” may be real synthesis differences; they are not discounted.

The first holdout exposed spelling normalization and recheck bugs and informed fixes. It is no longer untouched validation. The confirmation scripts/voices were new after those fixes, but the final alignment change was replayed on all sets, so these are development/confirmation evidence, not a sealed independent benchmark. The nine confirmation defects are a small sample.

Scoring requires time intersection and >=90% ordered target-token coverage. Both fault text and finding text use the product's canonicalization: case and punctuation are ignored; number spellings use num2words 0.5.14; a fixed contraction map expands forms such as cannot/can't; into→in to and onto→on to; Mr/Mrs expand; EnglishSpellingNormalizer from whisper-normalizer 0.1.15 maps spelling variants. Raw source and recognized text remain unchanged in the report. In particular, treating “sign into” and “sign in to” as different lowers two development repetition matches to 89.47%; the declared normalized scorer treats them as equivalent. `research/summarize.py` imports the product tokenizer, so this is executable rather than a manual favorable adjustment.

Early exact string scoring mishandled punctuation and common boundary words; the correction is documented, not credited as improved recognition. A rotated library repetition remains a conservative miss. Windows are merged before calculating audition fraction. The raw findings, recheck evidence and [per-clip results](../research/product-summary.json) remain inspectable. No SHA256 bookkeeping is needed.

A separate **16.6-minute engineering stress run** concatenated all 13 clean synthetic clips with half-second pauses and replaced the first garden clip with its omission variant. The wheel produced a 16.2 MB report in 81.688 seconds of recognition/rechecks, located the planted omission and retained six additional suspects. A clipping warning was shown. This uses repeated scripts and multiple voices, so it is a length/packaging check, not independent natural-production accuracy evidence. [Input composition](../research/long-input.json), [actual findings](../research/long-result.json).

## Counterevidence and changes

- `base.en` did not meet the gate; `small.en` alone still exceeded the audition bound on one clip.
- A second independent crop recognition can show that a first mismatch is not reproduced. Findings remain in the report's Rechecks view. Long insertions and repetitions cannot be downgraded merely because a correct copy is present.
- The public LibriSpeech sample contains names and recognition failures. A larger distil-large-v3.5 trial did not make it suitable for the broad claim. The product does not market itself as general audiobook QA.
- A dense 46.8-second demo with three planted faults exposed bad alignment: cheap substitutions collapsed three distinct edits into a single large block. Indel/LCS anchors now retain the intervening correct words and show three items. All corpora were replayed after this change. The dense demo asks for about 19 seconds of listening; **the 30% sparse-fault result does not apply to it**.

## Fair alternatives

TTSProof 0.4.0 was run on the same 40 development/first-holdout recordings with the **exact same cached first-pass transcript**. Its duration ceiling was raised to 1,200 seconds to accept the task; other structural defaults remained enabled. No runtime comparison is valid because recognition was cached.

At its default WER threshold of .03, nine of ten single-word/number altered clips pass. The remaining altered clip is stopped by clipping checks. At **WER threshold 0, all altered files are flagged**, some by structural gates before ASR. Therefore threshold configuration can solve the narrow “flag this file” problem. Saydelta's reason to exist is the standalone, shareable human listening workflow, not exclusive word-error detection. TTSProof also checks audio properties that Saydelta does not replace.

A normalized text diff of the same transcript contains the same mismatch evidence. Saydelta adds timed navigation, conservative recheck evidence and decisions; no superior recognition accuracy is claimed. Listening end to end remains a useful baseline and may be preferable for short recordings. AudioBook-Maker, tts-audiobook-tool and hosted Voiceover QA were researched but not run; no measured superiority over them is claimed.

## Reproduce

The lightweight product example needs only the package, a recognition model and the files under `examples/`. For the controlled research corpus, install the research dependencies separately (`kokoro-onnx==0.6.1`, `espeakng-loader==0.2.4`, `soundfile==0.14.0`, `ttsproof==0.4.0`, and `pyarrow` for the human subset), and download the disclosed Kokoro assets into `.models/kokoro` and the small.en CTranslate2 model into `.models/small.en`.

```sh
python research/download_models.py
python research/make_corpus.py
python research/make_corpus.py --corpus research/holdout.json --voices bf_emma af_sky --manifest research/holdout-manifest.json
python research/make_corpus.py --corpus research/confirmation.json --voices am_adam af_nicole bm_george --manifest research/confirmation-manifest.json
python research/human_holdout.py
python research/probe.py --model small.en --no-vad --manifest research/audio-manifest.json
python research/probe.py --model small.en --no-vad --manifest research/holdout-manifest.json
python research/probe.py --model small.en --no-vad --manifest research/confirmation-manifest.json
python research/probe.py --model small.en --no-vad --manifest research/human-manifest.json
python research/recheck_product.py
python research/summarize.py --prefix product
python research/baseline.py --wer-threshold 0.03
python research/baseline.py --wer-threshold 0
```

`probe.py` retains an older exploratory alignment; only its independently recognized word cache is used in final product replay. `recheck_product.py` imports current product code and reruns crop recognition. Downloading and regeneration are not deterministic latency guarantees; model/library versions and hardware matter.

`download_models.py` retrieves `kokoro/kokoro-v1.0.onnx`, `kokoro/voices-v1.0.bin` from the official kokoro-onnx model-files-v1.0 release, plus small.en's `config.json`, `tokenizer.json`, `vocabulary.txt`, `model.bin` from the official Systran model repository, all under `.models/`. `human_holdout.py` retrieves the disclosed 9 MB public parquet file if missing. Downloads use verified HTTPS and can fail if the network or model host is unavailable.

## Current evidence boundary

Engineering checks and controlled audio experiments are internal evidence. No public release, real user adoption, repeated use, unsolicited sharing or contribution has yet been observed. No hidden telemetry is installed. Those stages must be reported separately.

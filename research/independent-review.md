# Independent new-user reproduction and skeptical review

Date: 2026-10-19. Reviewer: a separate agent that did not implement Saydelta. This is an independent engineering check within the same workspace, not external user or market validation. Product implementation was not consulted to repair the reproduction.

## Reproduction

Started with README.md only. Created `.independent/venv` using the machine-default Python 3.14.6, then ran the documented editable ASR install. Installation succeeded, including faster-whisper 1.2.1, CTranslate2 4.8.3 and PyAV 16.1.0. Used the environment executables directly instead of shell activation and placed outputs under `.independent`; neither change alters the product invocation.

The documented default command failed during the first model download. The model host reported `SSL: UNEXPECTED_EOF_WHILE_READING`, retried, then the CLI exited 1 with a useful message to check the connection or provide a complete local model folder. No report was produced. This is a network-path failure, not evidence of an inference defect; a clean first-download experience is not verified.

The README explicitly documents an offline local-model option. After consulting linked validation documentation, used the existing `.models/small.en` assets with the same fresh environment:

```powershell
.\.independent\venv\Scripts\saydelta.exe check examples/garden.wav examples/garden.txt --model .models/small.en --offline -o .independent/offline-review.html
```

This succeeded in roughly 9 seconds total; report provenance records 7.28 seconds of recognition and rechecks. No external ffmpeg or GPU was needed. This verifies a fresh dependency environment with existing model assets, not a fully fresh asset download.

## Actual output checks

Inspected both the packaged `examples/garden-review-v2.html` and newly generated `.independent/offline-review.html`, rather than relying on exit status. Each contains the actual script, transcript and three review findings matching the disclosed edits:

- Omission of the sentence about wild flowers and bees; context 15.30–18.82 seconds.
- Replacement `one` with `two`; context 17.24–20.54 seconds.
- Repetition of the planting/soil/wheelchair sentence; context 21.40–35.62 seconds.

Each HTML embeds 562,508 bytes of MP3. Independently decoded that payload with PyAV: mono, 24 kHz, 1,123,200 nonzero audio samples, exactly 46.8 seconds. The HTML creates an Audio object from that data payload. This is substantive evidence of decodable embedded audio, not a human listening certification or browser-playback test. The merged review windows total 19.46 seconds, or 41.6% of the dense demo; the documentation correctly excludes this example from its sparse-fault 30% claim.

Browser verification remains blocked. The available CUA browser rejected the README-directed local `file:///.../garden-review-v2.html` URL under its protocol security policy and explicitly prohibited indirect workarounds. No workaround was attempted. Independent visual layout, click-to-play, seek, decisions export/import and offline browser behavior are therefore unverified here. This limitation belongs to this test environment; it is not evidence that a normal browser cannot open the file.

## Results and comparison audit

Read the linked validation protocol, current validation report, source notes, edit record, raw product result JSON and both TTSProof baseline JSON files. Recomputed clean findings/minutes and merged maximum audition fractions from raw results: all four documented rows agree. Ordered-token/time-intersection checking reproduced holdout 11/12, confirmation 9/9 and human 3/3. A literal token check yields development 16/18 because both backup repetitions say `sign into` versus planted `sign in to` (89.47% literal coverage); treating that reasonable equivalence as normalization yields the stated 18/18. Metric normalization should be specified explicitly enough to reproduce without implementation inspection.

Baseline counts independently agree with the text: at WER .03, 9/10 substitutions pass; at WER 0, all 30 altered clips fail, along with 4/10 clean clips. Those are saved-output audits; I did not independently rerun the complete corpus or competitor.

Checked the current [TTSProof upstream README](https://github.com/Mormolykos/ttsproof): it already offers structural checks, normalized WER/CER, and a self-contained HTML report with waveform/audio playback. Saydelta cannot claim that portable HTML or local word-error detection alone is unique. The narrower candidate distinction is timestamped passage review and decisions for existing recordings. The current README generally respects that boundary; superiority in user effort or usefulness remains unmeasured.

## Concrete issues and evidence limits

1. **First download did not complete.** Keep fresh-download verification pending. The error is actionable, but a direct model download/source link and concrete folder contents would make the documented offline fallback usable for a genuinely new user who does not inherit `.models`.
2. **Research reproduction is less complete than product reproduction.** Validation asks for Kokoro assets in `.models/kokoro` without exact download commands/filenames in that section; third-party documentation gives upstream links. Provide exact asset setup and complete per-manifest commands before describing the corpus as frictionlessly reproducible.
3. **Scoring normalization needs precision.** The `in to`/`into` equivalence changes the reported development hit rate under the 90% rule. Document the canonicalization used by the metric and the distinction from raw word coverage.
4. **Product evidence remains narrow.** All synthetic tests use Kokoro; confirmation includes only one script and nine planted defects. Existing holdout-informed fixes and replay of final alignment make this internal development/confirmation evidence, not an untouched independent accuracy benchmark. The failed human-audiobook result is correctly retained.
5. **Human benefit is still a hypothesis.** Audition-window fraction is not measured completion time, missed-error rate after review, reviewer preference, repeat use or willingness to share. No such adoption or market claim is justified by this review.

Verdict: the local inference-to-portable-audio-report core independently reproduces with existing model assets and identifies all three disclosed demo changes. Fresh network model acquisition and independent browser interaction are unresolved. The benchmark arithmetic and restrained competitive framing are substantially supported, with the reproduction and metric-documentation gaps above.

## Follow-up after downloader and documentation changes

2026-10-19, same independent reviewer. This follow-up preserves the original failed-download observation above.

Re-read the revised README and validation instructions. The recommended path now explicitly prepares a model with `saydelta fetch-model models/small.en`, then runs offline inference. README includes the official source link, all four required filenames, a direct-executable PowerShell alternative that avoids activation-policy changes, and the failure/retry policy. The validation instructions now include the asset-download helper, explicit commands for all four manifests and the canonicalization responsible for the `in to`/`into` metric difference. These revisions address my concrete instruction and scoring-transparency findings.

The implementing agent reports successfully downloading all four files into the fresh `.models/download-check-small.en` directory. **I did not perform or independently observe that network transfer.** I independently inspected that directory: config.json 2,657 bytes; tokenizer.json 2,128,466 bytes; vocabulary.txt 422,309 bytes; model.bin 483,545,366 bytes. I also verified the installed CLI exposes the newly documented fetch-model command. Its HTTPS/retry implementation was not independently audited in this new-user review.

I independently reran the documented offline check using those newly downloaded assets in my original fresh Python 3.14 environment, writing `.independent/fresh-assets-review.html`. It succeeded in roughly 9 seconds total and records 7.359 seconds of recognition/rechecks. I inspected both this independently generated report and the implementing agent's `research/fresh-download-review.html`: each contains the three expected omission/replacement/repetition findings and a 562,508-byte MP3 that decodes to 46.8 seconds of nonzero mono audio. This establishes that the newly acquired asset set is usable independently of the original model directory.

Within the scope exercised, I found **no remaining demonstrated engineering blocker for a clearly labeled Windows pre-release**. This is not comprehensive release certification: my browser interaction remains unverified under the prior CUA restriction, the new downloader's network run is implementer evidence, other platforms and the complete research regeneration were not independently exercised, and no human-usefulness or adoption conclusion follows. The original automatic-download path failure remains real and is now honestly documented as an optional path rather than the recommended quickstart.

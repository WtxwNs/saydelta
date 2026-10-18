# Historical decision log

Recorded during development; see PROJECT_STATUS.md for the current state.

# Project status

Updated: 2026-10-19 (Asia/Shanghai). Goal active; audio proofing candidate in real feasibility testing. Not accepted or released.

## Constraints and environment
- Workspace: `D:/0work/Repo/1019Github`, initially empty. Windows/PowerShell.
- Node 24.18.0, npm 11.16.0, Git 2.55.0, uv 0.11.28, Python 3.12.13 and 3.14.6 available.
- NVIDIA RTX 5090 laptop-class device: 24,463 MiB reported VRAM, ~32 GB RAM. GPU computation not yet exercised.
- npm registry and Python HTTPS to GitHub work. Windows curl certificate revocation check fails; do not disable TLS verification. Web tool sometimes cannot retrieve Trending query pages; direct Python retrieval succeeded for weekly/monthly.
- Free, reasonable dependency/model downloads authorized. No new paid services. No public publishing or outreach authorized yet.
- Maintain simple architecture; no hidden telemetry, fabricated adoption, SHA256 bookkeeping or weak benchmark comparisons.

## Research, first pass
Raw weekly/monthly Trending snapshots and parsed entries are in `research/`. Daily timed out; retry independent of direction selection. Growth is displayed-window growth, not cumulative stars. Not independently audited.

Candidate directions (not commitments):
1. Local audio/script discrepancy review for voiceover and audiobook creators: timestamped suspect passages, click to listen, portable review report. Alternatives: listen end-to-end, ASR + text diff, Voiceover QA, AudioBook-Maker. Critical risk: ASR errors overwhelm true narration defects; existing integrated tools may already suffice. Validation: known clean and altered audio, independent recognition, measure localized defect recall and false alarms, compare to simple ASR diff and current tools. Shareable evidence: real before/after audio review.
2. Video/screen recording privacy redaction: strong visible utility, but OpenScrub already covers local OCR, motion, review, GPU and output. Tentatively reject as insufficient differentiation; claims have not been tested.
3. PDF visual comparison with inserted-page alignment: valuable to document reviewers, but htmlapps-pdf-compare already advertises browser-local alignment and five views. Stirling-PDF #6089 is closed with implementation PR. Tentatively reject; do not sell a known upstream feature as a new product.
4. Agent test-weakening review: obvious developer demand, but Test Weakening Guard, slopsieve and existing supervision tools already cover it. Tentatively reject generic deterministic diff rules without new demonstrated advantage.
5. CSV change review: repeated duplicate-key and composite-key complaints, but many local CLI/browser tools exist. An upstream bug fix alone is not an independent project.

## Current iteration
Question: Is model-independent local audio proofing a meaningful gap, and can targeted review work without excessive ASR false positives?
Action: inspect original user reports, competing implementation and releases, then build only a minimal real audio-to-review experiment if the gap survives.
Evidence: VoiceStudio appears in monthly Trending (+40,333 displayed; 74,668 cumulative in retrieved snapshot). This is attention, not adoption evidence. VoxCPM #394 reports repeated/missing words for Persian; Higgs #117 describes a user's separate Whisper verification workflow. Existing AudioBook-Maker releases advertise word-level quality review, so competitor inspection is mandatory.
## Iteration 2 — real audio feasibility
- `research/sources.md` records primary sources, competition, dates and counterevidence. Daily Trending retrieved on retry; all three windows saved.
- Candidate working name: Saydelta (exact search found no obvious match; CueProof and Readback rejected due collisions).
- `research/validation-plan.md` written before trials: >=90% planted defect recall, <=1 clean suspect/minute, <=30% targeted audition duration. Need truthful ASR uncertainty, no reference prompt, and independent inputs.
- Installed free dependencies in `.venv`, downloaded Kokoro ONNX (~326 MB) and voices (~28 MB), faster-whisper base.en (~145 MB), small.en (~484 MB). Distil-large-v3.5 download ongoing as further quality experiment. ~307 GB disk free at start. CPU inference works; GPU computation not required or yet tested.
- PyAV 19 is incompatible with faster-whisper 1.2.1 (`metadata_errors` removed). Pin tested PyAV 16.1.0. An older download process held a DLL open during replacement; it was stopped, and reinstall worked. Final product clean-env installation must not reuse this experimental environment.
- Windows curl's `--ssl-revoke-best-effort` solved missing revocation-service access while retaining certificate verification. HF Xet stalled; normal HTTP with `HF_HUB_DISABLE_XET=1` or curl succeeded. Do not ship Windows-specific workarounds as a cross-platform requirement.
- Original corpus: three scripts, two Kokoro voices, clean + omitted sentence + repeated sentence + changed word/number = 24 files (~20 min). `make_corpus.py`, source JSON and manifests allow regeneration. These are controlled defects, not a natural error-rate survey.
- Base.en plus normalization detected 18/18 planted defects but had 5 suspect regions/4.988 clean minutes and up to 35.4% audition duration: FAIL, do not round into a pass.
- Small.en reduced clean suspects to 1/4.988 minutes; 18/18 found; maximum audition share 31.18%: still FAIL.
- Repetition locations are inherently ambiguous between identical copies. v2 alignment auditions both copies. Adjacent edits merge; punctuation, number spelling, contractions and spoken-identical into/in to normalize with raw text retained.
- Independent local ASR recheck uses six expected words of context each side only AFTER fresh recognition; expected text is never provided to ASR. A unique contiguous context match marks `not_reproduced`; long insertions/repetitions are never dismissed by this rule. All original findings and recheck evidence retained. On development samples, planted defects remain and four spurious findings are not reproduced. Full aggregate recomputation pending.
- Held-out `holdout.json`: two new scripts, bf_emma/af_sky voices, same defect families = 16 files. Generation complete; small.en transcription/recheck running. Do not tune on held-out results without a new holdout.
- External counterexample: fixed first groups from LibriSpeech dummy subset (CC-BY-4.0), human speaker 1272. Six constructed files (three clean, three omitted utterance). Small.en finds omissions but produces 24 clean suspects/3.875 minutes, including names and an ASR chunk omission: broad human-narration claim FAILS. Local recheck and larger-model checks pending. No hiding this result or claiming universal audiobook QA.
- Evaluation harness initially compared punctuation-bearing truth strings to punctuation-stripped diffs; corrected to normalized whole-word content matching. Original low hit count was an evaluator bug, not a model improvement. All measured windows still checked against ground-truth intervals.

## Iteration 3 — real product path, still pre-release
- Narrowed claim openly: ordinary-vocabulary synthesized English voiceovers; public human audiobook counterexamples remain failures even with a larger recognition model. No universal audiobook claim.
- Original Levenshtein alignment + conservative local recheck summary: development 18/18 planted defects, 0 suspects/4.988 clean minutes, max 28.17% audition; first holdout 11/12 by conservative ordered-content scoring, 1/4.965 clean minutes, max 22.88%; fresh confirmation 9/9, 3/6.629 clean minutes, max 18.77%. Human stress set 3/3 omissions but 24/3.875 clean minutes and max 55.66% audition: FAIL.
- Scoring fixes: punctuation and common boundary words can shift across a minimum-edit alignment. `research/summarize.py` uses >=90% ordered fault-token coverage plus time intersection; it deliberately counts the rotated library repetition as a miss. These are conservative automated labels, not listening-certified error counts or measured human time saved.
- First holdout exposed a dangerous recheck: a long insertion represented as a replacement could be dismissed when a correct copy coexisted. Net token growth >=3 now forbids downgrade, and a regression test covers this.
- Product implemented: bounded local audio decode, independent ASR, timestamp review, embedded mono MP3, offline HTML, decision notes/export/import, helpful input failures, exclusive atomic report publication. Existing output is preserved.
- Fresh `.verify` environment installed package + ASR/dev dependencies successfully. Actual CLI generated `research/clean-env-review.html` from a 40-second recording. Nine focused tests currently pass. Wheel install and independent README reproduction still pending.
- Browser verified actual playback, persistence after reload, decision download and import restoring exact note. Desktop and 390px layouts inspected; no horizontal overflow. Screenshots in `docs/`. Mobile interaction still requires further checking.
- A new multi-fault demo exposed unit-cost substitution alignment hiding three distinct defects in one misleading block. Switched product to Indel/LCS anchors, yielding separate omission/replacement/repetition on the actual 46.8-second `examples/garden.wav`. This changes the core algorithm: prior metrics are NOT automatically product acceptance. Full replay with fresh rechecks is running via `research/recheck_product.py`, saving separate `product-*` results and preserving old evidence. Dense 3-fault demo needs ~19 seconds audition; the 30% sparse-fault gate is not claimed for this dense demo.
- TTSProof paired recognition baseline at stock WER .03 misses some single changes; setting WER threshold to zero flags all altered files (some via clipping gate). Therefore detection is not an exclusive advantage; targeted playback and portable review are the value under test. No runtime comparison because competitor received cached recognition.
- `.models/distil-large-v3.5` downloaded (~1.5 GB) for counterexample investigation. CUDA inference attempted and failed missing `cublas64_12.dll`; all reported inference uses CPU. No GPU performance claim.

## Iteration 4 — release candidate verification
- Product replay completed: synthetic counts and review fractions unchanged from iteration 3. Human stress set still FAILS: 20 clean suspects/3.875 minutes, max 54.43%. `research/product-summary.json` is current; old recheck results preserved.
- Real dense demo: 46.8 seconds, 3 separately shown planted differences. Actual product recognition/recheck time 7.188 seconds (excludes model loading/download, decoding and encoding). The 40-second silent walkthrough uses real captured UI states with explicitly disclosed edited holds, not real-time footage; actual audio remains in the interactive report.
- `docs/validation.md` documents scoring corrections, adapted first holdout, limited one-model-family generalization, failed broad claim, and TTSProof threshold-zero counterevidence. Do not claim a unique detector or measured human time savings.
- Source archive and wheel built successfully. Wheel installed into `.wheelcheck` (separate fresh environment), invoked outside source root, generated 3 findings and a successfully decoded 46.8-second embedded MP3. Archive inspected: no models, virtual environments or vendor clones.
- English README, Chinese quickstart, third-party license/source notes, contribution guide and release notes written. MIT project; separately installed LGPL/BSD/MIT dependencies are not relabeled or bundled. No standalone executable distributed.
- Browser actions verified: note persistence, actual decision JSON download, import restoring the original note, 390px width without horizontal overflow. Captured screenshots are in `docs/`.
- Independent agent `independent_reproduction` launched at user's explicit request, with no implementation history and instructed to start from README. Fresh default Python 3.14 installation is underway. Its file-URL browser access was rejected by policy; it is recording this limitation and inspecting output/audio without bypassing it. Primary's earlier localhost UI verification is separate evidence.
- Community rules researched: HN forbids generated/automated posts, LocalLLaMA excludes primarily generated code/copy, TextToSpeech forbids self-promotion. `docs/release-plan.md` contains the specific GitHub release text and opt-in feedback plan; no prohibited community post is prepared for automatic submission.

Next: address independent reproduction findings, audit edge-case failure and missing release steps, finalize portable release files and concise status. Then request the exact public repository destination/publication authorization with reviewable deliverables. Public release, actual users, reuse/sharing remain unverified. Overall goal remains active, not achieved.

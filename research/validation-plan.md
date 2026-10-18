# Audio review feasibility gate (written before experiments)

Date: 2026-10-19. This is a candidate validation, not a product claim.

Proposed claim: For English voiceover creators reviewing an existing 1–20 minute recording against an exact script, a local, timestamped discrepancy inbox can expose localized omissions/repetitions/substitutions and let them audition the relevant context without moving their project into a new TTS studio. Costs: one ASR model download, local transcription time, and human decisions about ASR mistakes. This does not certify pronunciation, naturalness or complete correctness.

Compared with: (1) listening while reading; (2) faster-whisper transcript plus a plain normalized text diff, with identical recognition; (3) TTSProof, a credible current local QA package; (4) AudioBook-Maker and tts-audiobook-tool as integrated workflows (do not claim measured superiority without running them). Voiceover QA is a cloud alternative; do not upload samples or buy access.

Small gate: generate original clean narration with open Kokoro weights, then generate controlled variants containing a deleted sentence, repeated phrase, changed content word and changed number. Keep clean variants and disclose that faults are planted, not a measured natural TTS failure rate. Use at least three distinct passages, two voices, and a separate held-out passage if proceeding. Also inspect at least one non-planted public sample if licensing permits.

Decision thresholds before formal comparison:
- At least 90% of planted phrase-level defects should have a matching suspect region. Each region's audition window should contain the defect or the neighboring words for an omission (within 2 seconds).
- On clean narration, no more than one false suspect per minute after documented text normalization; inspect both ASR and actual sound before classifying.
- Candidate review windows should occupy at most 30% of the altered audio duration on sparse-defect samples. This is review surface, not a measured human time saving.
- Do not call normalization differences defects. Never silently hide content changes or claim no findings means verified correct.
- Local end-to-end output must include audible, independently checkable context and the original versus recognized text. No model prompt may contain the expected script (avoids recognition simply reproducing reference).
- Compare location usefulness and missed local defects with whole-file WER policies; do not weaken competitors' configured policies or claim detection accuracy improvements over the same ASR without evidence.

If this fails, record failures and revise the core method, or reject. Don't move thresholds to fit results. Long audio, names, numbers and repeated phrases are intentional stress cases. English-only is an explicit initial boundary, not a claim about multilingual reports gathered during research.

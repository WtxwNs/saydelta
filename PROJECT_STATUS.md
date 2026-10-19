# Saydelta project status

Updated 2026-10-19. Public GitHub publication authorized on 2026-10-19; publication in progress. Overall goal not achieved. Windows pre-release engineering path verified; public release and user adoption NOT verified.

## Current product and claim
For creators reviewing ordinary-vocabulary synthesized English voiceovers, Saydelta turns script/recognition differences into timed listening and decisions in one offline HTML file. Costs: a ~484 MB model download, local processing, and human judgment. Detection itself is not exclusive: a transcript diff or TTSProof with WER threshold zero can flag the same words. The distinct workflow is passage audition, retained evidence, notes and portable review of existing recordings.

## Verified evidence
- Actual workspace: Windows, Python 3.12/3.14, Node 24, ~32 GB RAM, RTX 5090 laptop GPU reporting ~24 GB VRAM. CUDA inference failed missing cublas64_12.dll; all reported runs use CPU.
- Current synthetic results: development 18/18; adapted first holdout 11/12; confirmation 9/9 planted defects localized. Clean suspects: 0/4.988, 1/4.965, 3/6.629 minutes. Maximum sparse-fault audition fraction: 28.18%, 22.89%, 18.77%. Predeclared gate: >=90% localized, <=1 clean suspect/minute, <=30% audition. One TTS model family only; no human completion-time claim.
- Broad human-audiobook claim FAILED: 20 suspects/3.875 clean minutes, maximum 54.43% audition. Larger model did not justify a general audiobook claim.
- Dense demo: actual 46.8-second audio, 3 planted faults, 19.46 seconds audition. This is not a sparse-fault 30% example. All edits disclosed.
- Fresh environments installed editable package and built wheel. Wheel ran outside source root. Output contained all 3 expected findings and an independently decoded 46.8-second MP3. 12 focused regression checks and lint pass.
- Default faster-whisper download failed in independent reproduction (SSL EOF). Added explicit fetch-model using verified HTTPS, progress and bounded retries. Primary completed all four files in a new folder; real inference using them succeeded. Independent agent reran with those fresh assets and confirmed the output. No TLS bypass.
- 16.6-minute synthetic concatenation stress run: produced a 16.2 MB HTML, found planted omission, retained 6 extra suspects; 81.688 seconds recognition/rechecks. Length/packaging check, not independent accuracy data.
- Primary browser checks: actual context playback, reload persistence, exported/imported decisions, desktop and 390px layout. Independent browser file-URL access was blocked by tool policy; it did not bypass the restriction. Browser verification and independent data verification remain separate.

## Decisions and failures retained
Use simple Python CLI + static HTML, CPU default, no server/account/telemetry. Reject generic video redaction, PDF comparison, test-weakening and CSV diff candidates due existing alternatives. Keep all ASR evidence; never put the reference script into recognition. Fixes to normalization, long-insertion rechecks and multi-fault alignment required replaying all corpora. See research/decision-log.md, research/sources.md and docs/validation.md for evidence and limitations.

## Delivery and next action
Source, English README, Chinese quickstart, real example, edited 40-second silent walkthrough, MIT license, third-party notices, source/wheel packages and specific release text are prepared. Independent review and its follow-up found no demonstrated engineering blocker for a labeled Windows pre-release within tested scope. Final artifacts are under dist/: wheel plus source tar.gz/zip, about 3.4 MB for the complete source/example bundle. Final build, source inspection and local Git snapshot completed before requesting publication authorization.

Public GitHub account verified as WtxwNs; WtxwNs/saydelta was not found. Neither repository creation/publication nor outreach is authorized yet. Ask once for permission to create that public repository and publish this reviewed release; keep community posts separate. HN forbids generated/automated posts, LocalLLaMA excludes primarily generated copy/code, TextToSpeech prohibits self-promotion. Do not post there automatically.

No external user trial, repeat use, sharing or contribution observed. Next useful evidence after authorized release: voluntary installation outcomes, completed review of a user's own recording, usefulness of findings, and a second real task. No monitoring automation or outreach is authorized. Do not mark the overall goal complete based on internal acceptance.

## Authorization-wait audit
Previous goal turn made substantive progress: completed release preparation and requested publication authorization. This continuation found and reproduced an uncaught HTTP IncompleteRead download failure, fixed bounded retries/partial cleanup, and passed the added regression. No publication reply or outreach authorization received. Public release and actual-user evidence remain the same external dependency; the goal is not complete.

Final blocked audit: the same missing publication authorization has persisted across the release-preparation turn and two automatic continuations. The previous continuation made progress by fixing the download failure. This continuation confirmed a clean Git state, current release artifacts, no public repository at the proposed destination, and a completed independent reviewer with no demonstrated engineering blocker within tested scope. No human authorization arrived. There is no pending engineering job whose completion can supply real-user evidence. Further publication or outreach requires user input; do not treat automatic goal continuations as consent. Mark the goal blocked pending that authorization, not complete.

## Authorization received
On 2026-10-19 the human user explicitly approved the previously proposed public WtxwNs/saydelta repository and first release. Repository/release publication is now authorized. This does not authorize private messages, community posts, or fabricated adoption. The prior authorization blocker is resolved.

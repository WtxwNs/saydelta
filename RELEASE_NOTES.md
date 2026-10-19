# 0.1.0 — public preview, 2026-10-19

First local release candidate: compare an English script with an existing recording, review timed discrepancies in a portable HTML file, listen to embedded audio and save decisions with notes.

CPU recognition is the default. The recommended `fetch-model` step downloads small.en with visible progress and bounded retries; processing then runs with `--offline`. Source recordings stay unchanged. Reports contain the script and a compressed listening copy; sharing a report shares that content.

Known limits: recognition suggestions require listening; human audiobooks and names perform poorly in the disclosed stress test; only Windows/Python 3.12 and 3.14 have been exercised locally; no real user retention or adoption evidence. Published at https://github.com/WtxwNs/saydelta/releases/tag/v0.1.0 after explicit authorization.

The downloader also handles truncated chunked HTTP responses with bounded retries and removes incomplete files. A regression test reproduces this failure; no recognition or alignment behavior changed.

# Release and first-user plan

Publication completed on 2026-10-19: [public repository](https://github.com/WtxwNs/saydelta), [v0.1.0 preview with eight assets](https://github.com/WtxwNs/saydelta/releases/tag/v0.1.0). Public example download verified. No community outreach or real-user adoption claimed.

## Destinations checked on 2026-10-19

1. **A public GitHub repository and release**, authorized by the human user on 2026-10-19 for WtxwNs/saydelta. Primary audience: local TTS users who already have recordings and need an auditable review file. Include runnable inputs, offline example, wheel/source archive, the 40-second edited walkthrough and the failed human-audiobook result. No paid hosting is needed.
2. **Hacker News / Show HN** is potentially relevant to local tools, but its [general rules](https://news.ycombinator.com/newsguidelines.html) prohibit generated text and automated posting. [Show HN rules](https://news.ycombinator.com/showhn.html) also ask for personal involvement, something usable and no vote solicitation. Do not post this agent's generated copy there. If the human maintainer chooses to participate after personally trying the product, they must write their own submission and be available to discuss it. No submission is prepared for automated use.
3. **r/LocalLLaMA** was researched as a TTS discussion source, but its [rules](https://www.reddit.com/r/LocalLLaMA/about/rules.json) disallow primarily generated code/copy and require relevance. It is not a release destination for this agent-built project under those rules.
4. **r/TextToSpeech** is directly relevant, but its [rules](https://www.reddit.com/r/TextToSpeech/about/rules.json) prohibit self-promotion. Exclude it. A guessed LocalTTS rules endpoint returned 404; do not infer permission from missing rules.

Do not circumvent community restrictions with disguised third-party recommendations, unsolicited issue advertisements, private messages or mass cross-posting. No outreach is authorized yet.

## GitHub release text, ready for human review

**Saydelta 0.1.0: an offline listening inbox for script/recording differences**

Saydelta compares an existing English voiceover with its script and creates one HTML file you can open offline. Choose a suspect passage, listen to its context, mark whether it needs another take, and save pickup notes. The report includes a listening copy, so a collaborator can inspect the same evidence without running a server.

Start by downloading `garden-review-v2.html` from the release and opening it in a browser. The 47-second synthetic example deliberately contains a missing sentence, a changed number and a repeated sentence. Its audio, script and edit record are included, along with a 40-second silent walkthrough made from actual browser captures. To process your own audio, install the source/wheel with the ASR extra; first use downloads about 484 MB for small.en. CPU works; no account or paid API is required.

This is a human review tool, not an error certificate. Recognition can be wrong. The controlled ordinary-vocabulary synthetic samples met the stated gate, while public human audiobook samples did not. Names, accents and noisy recordings can produce too many findings. Other tools can flag the same word differences; the focus here is timed listening and a portable decision record. Only Windows/Python 3.12 and 3.14 have been tested locally so far.

The project was developed with an AI coding agent, including implementation and internal evaluation. Internal tests are not user adoption evidence. If you try it, the most useful feedback is whether you completed a review of your own recording, which flags were useful or misleading, and whether you would use it for a second recording. Share audio only if you have permission and are comfortable making it public.

At publication attach the built source archive, wheel, `examples/garden-review-v2.html`, example input files and `docs/walkthrough.mp4`. The repository README links these relative files; no nonexistent public URL should be advertised before publication.

## Observe behavior without telemetry

Use an opt-in GitHub issue/discussion template after publication. Ask for: installation success or exact blocker; whether a real review was completed; which findings were correct or misleading; whether the user tried a second recording; what manual work remained. Audio upload is optional. Distinguish volunteered anecdotes from counts of all users.

Repository traffic, if available to the authorized owner, indicates exposure only. Stars do not establish reuse. If no target users see the project, revise discoverability and value explanation. If installation fails, fix that first. If users finish a review but do not return, investigate whether the workflow is useful before adding features. Do not schedule monitoring or contact people until those actions are specifically authorized.

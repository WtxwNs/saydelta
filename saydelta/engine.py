"""Local recognition and conservative rechecks. Reference text never enters ASR."""

import time
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path

from .alignment import align, tokenize
from .audio import RATE, decode


def recheck_allowed(finding):
    return (
        finding["kind"] != "repetition"
        and len(tokenize(finding["heard"])) - len(tokenize(finding["expected"])) < 3
    )


def load_model(name, device, offline):
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise ValueError('Install speech recognition first: pip install -e ".[asr]"') from exc
    try:
        return WhisperModel(
            name,
            device=device,
            compute_type="int8" if device == "cpu" else "float16",
            cpu_threads=6,
            local_files_only=offline,
        )
    except Exception as exc:
        hint = (
            "Use --device cpu, or install the CUDA libraries required by faster-whisper."
            if device == "cuda"
            else "Try: saydelta fetch-model models/small.en; then pass --model models/small.en --offline. Or use another complete local model folder."
        )
        if offline:
            hint = "The model is not available locally. Download it first or pass --model PATH."
        raise ValueError(f"Could not load speech recognition. {hint}") from exc


def recognize(model, audio, timestamps=True):
    # No initial_prompt, hotwords, prefix or reference-conditioned recognition.
    segments, _ = model.transcribe(
        audio,
        language="en",
        beam_size=5,
        word_timestamps=timestamps,
        vad_filter=False,
        condition_on_previous_text=False,
    )
    return list(segments)


def recheck(model, audio, script, findings, progress=lambda text: None):
    tokens = tokenize(script)
    reference = [t.value for t in tokens]
    duration = len(audio) / RATE
    for number, finding in enumerate(findings, 1):
        finding["status"] = "review"
        if not recheck_allowed(finding):
            continue
        a = next(
            (i for i, t in enumerate(tokens) if t.begin >= finding["script_start"]), len(tokens)
        )
        b = next((i for i, t in enumerate(tokens) if t.begin >= finding["script_end"]), len(tokens))
        expected = reference[max(0, a - 6) : min(len(reference), b + 6)]
        joined = " ".join(expected)
        # A unique anchor is necessary; an identical correct passage elsewhere
        # cannot be used to dismiss a real error here.
        if len(expected) < 8 or (" " + " ".join(reference) + " ").count(" " + joined + " ") != 1:
            continue
        start = max(0, finding["start"] - 5)
        end = min(duration, finding["end"] + 5)
        progress(f"Rechecking passage {number}/{len(findings)}…")
        began = time.monotonic()
        segments = recognize(model, audio[int(start * RATE) : int(end * RATE)], timestamps=False)
        heard = " ".join(s.text for s in segments)
        actual = " ".join(t.value for t in tokenize(heard))
        finding["recheck"] = {
            "start": start,
            "end": end,
            "expected_context": joined,
            "heard": heard,
            "seconds": round(time.monotonic() - began, 3),
        }
        if (" " + joined + " ") in (" " + actual + " "):
            finding["status"] = "not_reproduced"
    return findings


def review(
    audio_path,
    script,
    model_name="small.en",
    device="cpu",
    offline=False,
    progress=lambda text: None,
):
    if not script.strip() or not tokenize(script):
        raise ValueError("The script is empty. Supply the words expected in this recording.")
    if len(script) > 100_000:
        raise ValueError("Script exceeds 100,000 characters. Split it into chapters first.")
    progress("Reading the local recording…")
    audio = decode(audio_path)
    progress(
        "Loading local speech recognition…"
        if offline
        else "Loading speech recognition (an uncached model may download)…"
    )
    model = load_model(model_name, device, offline)
    progress("Recognizing speech without showing the model your script…")
    began = time.monotonic()
    try:
        segments = recognize(model, audio)
        words = [asdict(word) for segment in segments for word in (segment.words or [])]
        if not words:
            raise ValueError(
                "No speech was recognized. Check the audio and its language; English is supported."
            )
        duration = len(audio) / RATE
        findings = align(script, words, duration)
        recheck(model, audio, script, findings, progress)
    except RuntimeError as exc:
        raise ValueError(
            "Recognition failed. Try --device cpu and check the model installation."
        ) from exc
    transcript = " ".join(segment.text.strip() for segment in segments)
    from rapidfuzz.distance import Levenshtein

    expected = [t.value for t in tokenize(script)]
    actual = [t.value for t in tokenize(transcript)]
    match = 1 - Levenshtein.normalized_distance(expected, actual)
    warnings = []
    if match < 0.5:
        warnings.append(
            "Low text match: check that the script belongs to this audio. Names, noise or unsupported speech may also cause this."
        )
    if float(abs(audio).max()) >= 0.999:
        warnings.append(
            "Audio reaches full scale and may contain clipping. This review checks words, not sound quality."
        )
    return {
        "format": "saydelta-review-v1",
        "script": script,
        "duration": duration,
        "transcript": transcript,
        "words": words,
        "findings": findings,
        "warnings": warnings,
        "provenance": {
            "model": Path(model_name).name,
            "device": device,
            "language": "en",
            "faster_whisper": version("faster-whisper"),
            "beam_size": 5,
            "reference_prompt": False,
            "recheck": "unique-context-v1",
            "processing_seconds": round(time.monotonic() - began, 3),
            "timing_scope": "Recognition and rechecks only; excludes decoding, model loading/download and report encoding.",
            "note": "Recognition differences are suggestions for human review, not verified errors.",
        },
    }

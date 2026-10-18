"""Bounded local decoding; no external ffmpeg executable or network input."""

from pathlib import Path

import av
import numpy as np

RATE = 16000
MAX_SECONDS = 1200
MAX_BYTES = 512 * 1024 * 1024


def decode(path):
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"Audio file not found: {path}")
    if path.stat().st_size > MAX_BYTES:
        raise ValueError("Audio exceeds 512 MB. Export a shorter or compressed recording first.")
    parts = []
    count = 0
    try:
        with av.open(str(path)) as source:
            if not source.streams.audio:
                raise ValueError("This file has no audio track. Export a recording with speech.")
            resampler = av.AudioResampler(format="fltp", layout="mono", rate=RATE)
            for frame in source.decode(audio=0):
                for converted in resampler.resample(frame):
                    values = converted.to_ndarray().reshape(-1)
                    count += len(values)
                    if count > RATE * MAX_SECONDS:
                        raise ValueError(
                            "Recording exceeds 20 minutes. Split it into chapters first."
                        )
                    parts.append(values)
            for converted in resampler.resample(None):
                values = converted.to_ndarray().reshape(-1)
                count += len(values)
                if count > RATE * MAX_SECONDS:
                    raise ValueError("Recording exceeds 20 minutes. Split it into chapters first.")
                parts.append(values)
    except (av.FFmpegError, OSError) as exc:
        raise ValueError("Could not decode the audio. Try exporting it as WAV or MP3.") from exc
    if count < RATE // 2:
        raise ValueError("Recording is empty or shorter than half a second.")
    audio = np.concatenate(parts).astype(np.float32, copy=False)
    if not np.isfinite(audio).all():
        raise ValueError("Audio contains invalid samples. Re-export it as PCM WAV.")
    if float(np.max(np.abs(audio))) < 0.00001:
        raise ValueError("Recording is silent. Check the microphone or selected audio track.")
    return audio

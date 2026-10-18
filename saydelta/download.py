"""Explicit, bounded model retrieval via verified HTTPS, without credentials."""

import http.client
import json
import time
import urllib.error
import urllib.request
from pathlib import Path

MODEL_FILES = ("config.json", "tokenizer.json", "vocabulary.txt", "model.bin")
MODEL_URL = "https://huggingface.co/Systran/faster-whisper-small.en/resolve/main/"


def fetch_model(destination, progress=print):
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    if any(destination.iterdir()):
        raise ValueError(
            "Model folder is not empty. Choose a new empty folder; existing files are preserved."
        )
    completed = []
    for name in MODEL_FILES:
        target = destination / name
        partial = destination / (name + ".download")
        failure = None
        for attempt in range(3):
            progress(f"Downloading {name} (attempt {attempt + 1}/3)...")
            count = 0
            try:
                request = urllib.request.Request(
                    MODEL_URL + name + "?download=true", headers={"User-Agent": "Saydelta/0.1"}
                )
                with (
                    urllib.request.urlopen(request, timeout=60) as source,
                    partial.open("xb") as out,
                ):
                    expected = source.headers.get("Content-Length")
                    checkpoint = 0
                    while chunk := source.read(1024 * 1024):
                        out.write(chunk)
                        count += len(chunk)
                        if count - checkpoint >= 32 * 1024 * 1024:
                            progress(f"  {name}: {count // (1024 * 1024)} MiB received")
                            checkpoint = count
                if expected and count != int(expected):
                    raise OSError("The model host ended the transfer before the expected length.")
                if not count:
                    raise OSError("The model host returned an empty file.")
                if name.endswith(".json"):
                    json.loads(partial.read_text(encoding="utf-8"))
                partial.rename(target)
                completed.append(name)
                failure = None
                break
            except (OSError, ValueError, http.client.HTTPException) as exc:
                failure = exc
                partial.unlink(missing_ok=True)
                if attempt < 2:
                    time.sleep(1)
        if failure:
            # Keep complete downloads for inspection, but explain the exact state.
            raise ValueError(
                f"Download failed for {name} after 3 attempts: {failure}. "
                f"Completed files: {', '.join(completed) or 'none'}. "
                "Check your network connection. Use a new empty folder to retry, or obtain the "
                "four model files from https://huggingface.co/Systran/faster-whisper-small.en/tree/main."
            ) from failure
    progress(f"Model ready: {destination.resolve()}")
    return destination

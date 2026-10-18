"""Produce an offline, portable review file. No third-party scripts or requests."""

import base64
import io
import json
import os
import tempfile
import uuid
from importlib.resources import files
from pathlib import Path


def review_audio(path):
    """Encode a compact listening copy; original source is never modified."""
    import av

    output = io.BytesIO()
    with av.open(str(path)) as source, av.open(output, "w", format="mp3") as target:
        stream = target.add_stream("libmp3lame", rate=24000)
        stream.bit_rate = 96000
        stream.layout = "mono"
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=24000)
        for frame in source.decode(audio=0):
            for converted in resampler.resample(frame):
                for packet in stream.encode(converted):
                    target.mux(packet)
        for converted in resampler.resample(None):
            for packet in stream.encode(converted):
                target.mux(packet)
        for packet in stream.encode(None):
            target.mux(packet)
    return base64.b64encode(output.getvalue()).decode("ascii")


def write_report(data, audio_path, destination):
    destination = Path(destination)
    if destination.exists():
        raise ValueError("Output already exists. Choose another filename.")
    payload = {**data, "id": data.get("id", str(uuid.uuid4())), "audio": review_audio(audio_path)}
    encoded = (
        json.dumps(payload, ensure_ascii=True)
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )
    template = files("saydelta").joinpath("review.html").read_text(encoding="utf-8")
    html = template.replace("/*__REPORT_DATA__*/", encoded)
    # Exclusive creation protects an existing report, even if another process
    # creates it during recognition. Remove partial output on write failure.
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=destination.parent, suffix=".tmp", delete=False
    ) as temporary:
        staging = Path(temporary.name)
        temporary.write(html)
    try:
        # Hard-link publication is atomic and refuses to overwrite on supported
        # local filesystems. Both paths are on the same volume.
        os.link(staging, destination)
    except OSError as exc:
        raise ValueError(
            "Could not save the report. Use a writable local folder and a new filename."
        ) from exc
    finally:
        staging.unlink(missing_ok=True)

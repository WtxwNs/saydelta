"""Build a transparent three-edit demo from the original controlled garden corpus."""
import json
from pathlib import Path

import numpy as np
import soundfile as sf

root = Path("examples")
root.mkdir(exist_ok=True)
passage = json.loads(Path("research/corpus.json").read_text())[0]
manifest = json.loads(Path("research/audio-manifest.json").read_text())
changed = next(r for r in manifest if r["id"] == "garden-af_heart-substitution")
audio, rate = sf.read(changed["audio"], dtype="float32")
parts = []
for i in range(8):
    samples, sr = sf.read(f"research/audio/garden-af_heart-sentence-{i}.wav", dtype="float32")
    assert sr == rate
    parts.append(np.concatenate([samples, np.zeros(round(rate * .25))]))
fault = changed["fault"]
parts[4] = audio[round(fault["start"] * rate):round(fault["end"] * rate)]
order = [0, 1, 2, 4, 5, 5, 6, 7]
sf.write(root / "garden.wav", np.concatenate([parts[i] for i in order]), rate, subtype="PCM_16")
(root / "garden.txt").write_text(" ".join(passage["sentences"]) + "\n", encoding="utf-8")
(root / "edits.json").write_text(json.dumps({"method": "Controlled edits, not natural TTS failures",
    "voice": "Kokoro af_heart", "sentence_order_zero_based": order,
    "omitted": passage["sentences"][3], "repeated": passage["sentences"][5],
    "replaced": {"expected": "one", "heard": "two", "sentence": 4}}, indent=2), encoding="utf-8")
print("Wrote examples/garden.wav and garden.txt; all planted edits disclosed in edits.json")

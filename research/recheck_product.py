"""Replay cached independent ASR through the current product and fresh rechecks."""
import json
from pathlib import Path

from saydelta.alignment import align
from saydelta.audio import decode
from saydelta.engine import load_model, recheck

model = load_model(".models/small.en", "cpu", True)
for corpus in ["audio", "holdout", "confirmation", "human"]:
    rows = json.loads(Path(f"research/{corpus}-manifest.json").read_text())
    results = []
    for row in rows:
        raw = json.loads(Path(f"research/audio/{row['id']}.small.en-no-vad.asr.json").read_text())
        findings = align(row["script"], raw["words"], row["duration"])
        recheck(model, decode(row["audio"]), row["script"], findings)
        results.append({key: row[key] for key in ["id", "duration", "kind", "fault"]} | {"findings": findings})
        print(row["id"], sum(f["status"] == "review" for f in findings), flush=True)
    Path(f"research/product-{corpus}-manifest-small.en.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

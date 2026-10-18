"""Aggregate saved rechecks; do not run recognition or change any findings.

Conservative content check: >=90% ordered reference fault tokens plus time
intersection. This scorer misses a rotated repetition in the first holdout;
keep it as a miss rather than manually granting a favorable result.
"""
from difflib import SequenceMatcher
import json
from pathlib import Path
import argparse

from saydelta.alignment import tokenize


def values(text):
    return [token.value for token in tokenize(text)]


results = []
parser = argparse.ArgumentParser()
parser.add_argument("--prefix", default="recheck", choices=["recheck", "product"])
args = parser.parse_args()
for corpus in ["audio", "holdout", "confirmation", "human"]:
    rows = json.loads(Path(f"research/{args.prefix}-{corpus}-manifest-small.en.json").read_text())
    clean = [row for row in rows if row["kind"] == "clean"]
    altered = [row for row in rows if row["kind"] != "clean"]
    details = []
    for row in altered:
        active = [f for f in row["findings"] if f["status"] == "review"]
        fault = row["fault"]
        target = values(fault["expected"] or fault["heard"])
        hit = False
        for finding in active:
            actual = values(finding["expected"] if fault["expected"] else finding["heard"])
            coverage = sum(b.size for b in SequenceMatcher(None, target, actual, autojunk=False).get_matching_blocks()) / len(target)
            hit |= coverage >= .9 and finding["start"] <= fault["end"] and finding["end"] >= fault["start"]
        intervals = []
        for finding in sorted(active, key=lambda f: f["start"]):
            if intervals and finding["start"] <= intervals[-1][1]:
                intervals[-1][1] = max(intervals[-1][1], finding["end"])
            else:
                intervals.append([finding["start"], finding["end"]])
        details.append({"id": row["id"], "hit": hit,
                        "review_fraction": sum(e-s for s,e in intervals)/row["duration"]})
    results.append({"corpus": corpus, "hits": sum(r["hit"] for r in details),
                    "planted_defects": len(altered),
                    "clean_suspects": sum(f["status"] == "review" for r in clean for f in r["findings"]),
                    "clean_minutes": sum(r["duration"] for r in clean)/60,
                    "max_review_fraction": max(r["review_fraction"] for r in details), "details": details})
Path(f"research/{args.prefix}-summary.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
for result in results:
    print({k: v for k, v in result.items() if k != "details"})

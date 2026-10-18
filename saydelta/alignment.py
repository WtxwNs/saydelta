"""Feasibility alignment: normalized tokens keep source offsets and audio times."""

import re
from dataclasses import dataclass

from num2words import num2words
from rapidfuzz.distance import Indel
from whisper_normalizer.english import EnglishSpellingNormalizer

SPELLING = EnglishSpellingNormalizer()


@dataclass
class Token:
    value: str
    begin: int
    end: int
    start: float = 0
    stop: float = 0


PATTERN = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?|[^\W\d_]+(?:['’][^\W\d_]+)*|[$€£%]", re.UNICODE)
CONTRACTIONS = {
    "can't": "can not",
    "cannot": "can not",
    "won't": "will not",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "isn't": "is not",
    "aren't": "are not",
    "wasn't": "was not",
    "weren't": "were not",
    "it's": "it is",
    "i'm": "i am",
    "we're": "we are",
    "you're": "you are",
    "they're": "they are",
    "into": "in to",
    "onto": "on to",
    "mr": "mister",
    "mrs": "missus",
}


def tokenize(text, start=0, stop=0):
    output = []
    for match in PATTERN.finditer(text):
        value = match[0].lower().replace("’", "'")
        if value[0].isdigit() and len(value) < 16:
            value = num2words(value.replace(",", ""))
        value = SPELLING(CONTRACTIONS.get(value, value))
        for part in re.findall(r"[^\W_]+(?:'[^\W_]+)*|[$€£%]", value):
            output.append(Token(part, match.start(), match.end(), start, stop))
    return output


def align(script, words, duration):
    expected = tokenize(script)
    transcript = ""
    observed = []
    for word in words:
        text = word["word"].strip()
        offset = len(transcript)
        transcript += text + " "
        for token in tokenize(text, word["start"], word["end"]):
            token.begin += offset
            token.end += offset
            observed.append(token)
    a = [t.value for t in expected]
    b = [t.value for t in observed]
    changes = []
    # Merge tiny equal islands between differences, preserving their full text.
    # Preserve matching words as anchors. Unit-cost substitutions can turn a
    # missing sentence plus a repeated sentence into one misleading replacement.
    for op in Indel.opcodes(a, b):
        tag, i, j, k, l = op
        if tag == "equal":
            continue
        if changes and i - changes[-1][1] <= 2 and k - changes[-1][3] <= 2:
            changes[-1][1] = j
            changes[-1][3] = l
        else:
            changes.append([i, j, k, l])
    findings = []
    for i, j, k, l in changes:
        source_begin = expected[i].begin if i < len(expected) else len(script)
        source_end = expected[j - 1].end if j > i else source_begin
        heard_begin = observed[k].begin if k < len(observed) else len(transcript)
        heard_end = observed[l - 1].end if l > k else heard_begin
        start = observed[k].start if k < len(observed) else duration
        stop = observed[l - 1].stop if l > k else start
        kind = "replacement" if j > i and l > k else ("omission" if j > i else "insertion")
        if l == k:
            start = observed[k - 1].stop if k else 0
        # Either identical copy could be called the insertion. Play both copies
        # instead of pretending the minimum edit alignment identifies intent.
        if i == j and l - k >= 3:
            count = l - k
            if k >= count and b[k - count : k] == b[k:l]:
                start = observed[k - count].start
                kind = "repetition"
            elif b[l : l + count] == b[k:l]:
                stop = observed[l + count - 1].stop
                kind = "repetition"
        findings.append(
            {
                "kind": kind,
                "expected": script[source_begin:source_end],
                "heard": transcript[heard_begin:heard_end],
                "script_start": source_begin,
                "script_end": source_end,
                "start": max(0, start - 1.5),
                "end": min(duration, max(start + 0.2, stop) + 1.5),
            }
        )
    return findings

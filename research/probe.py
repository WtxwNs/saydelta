"""Small real ASR-to-timed-diff probe. No reference prompt is sent to ASR."""
import json
import re
import time
import argparse
from pathlib import Path
from difflib import SequenceMatcher
from faster_whisper import WhisperModel
from rapidfuzz.distance import Levenshtein
from num2words import num2words

def tokens(text):
    text = re.sub(r'\b\d+\b', lambda m: num2words(int(m[0])), text.lower())
    text = re.sub(r'\bin to\b', 'into', text)
    return re.findall(r"[a-z0-9]+(?:'[a-z]+)?", text.replace('\u2019', "'"))

def compare(reference, words, duration):
    expected = tokens(reference)
    observed = []
    timed = []
    for word in words:
        for token in tokens(word['word']):
            observed.append(token)
            timed.append(word)
    findings = []
    for tag, a, b, c, d in Levenshtein.opcodes(expected, observed):
        if tag == 'equal':
            continue
        start = timed[c]['start'] if c < len(timed) else duration
        end = timed[d-1]['end'] if d > c else start
        if tag == 'delete':
            start = timed[c-1]['end'] if c > 0 else 0
        findings.append({'kind': tag, 'expected': ' '.join(expected[a:b]), 'heard': ' '.join(observed[c:d]),
            'start': max(0, start-1.5), 'end': min(duration, max(start+.2,end)+1.5)})
    return findings

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='base.en')
    parser.add_argument('--no-vad', action='store_true')
    parser.add_argument('--manifest', default='research/audio-manifest.json')
    args = parser.parse_args()
    model = WhisperModel('.models/'+args.model, device='cpu', compute_type='int8', cpu_threads=6)
    rows = json.loads(Path(args.manifest).read_text())
    results = []
    for row in rows:
        suffix = args.model + ('-no-vad' if args.no_vad else '')
        path = Path('research/audio', row['id'] + '.' + suffix + '.asr.json')
        start = time.monotonic()
        if path.exists():
            recognition = json.loads(path.read_text())
        else:
            segments, info = model.transcribe(row['audio'], language='en', beam_size=5,
                word_timestamps=True, vad_filter=not args.no_vad, condition_on_previous_text=False)
            segments = list(segments)
            recognition = {'words': [w._asdict() for s in segments for w in (s.words or [])],
                'text': ' '.join(s.text for s in segments), 'seconds': time.monotonic()-start}
            path.write_text(json.dumps(recognition, indent=2), encoding='utf-8')
        findings = compare(row['script'], recognition['words'], row['duration'])
        result = {'id': row['id'], 'duration': row['duration'], 'asr_seconds': recognition['seconds'],
            'findings': findings, 'fault': row['fault']}
        results.append(result)
        print(json.dumps(result), flush=True)
    Path('research/probe-results-'+suffix+'.json').write_text(json.dumps(results, indent=2), encoding='utf-8')

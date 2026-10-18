"""Original scripts, Kokoro synthesis, controlled edits with known audio intervals.

This is a controlled audio experiment, NOT a sample of naturally occurring errors.
"""
import argparse
import json
from pathlib import Path

import espeakng_loader
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro
from kokoro_onnx.config import EspeakConfig

parser = argparse.ArgumentParser()
parser.add_argument('--limit', type=int, default=3)
parser.add_argument('--voices', nargs='+', default=['af_heart', 'am_michael'])
parser.add_argument('--corpus', default='research/corpus.json')
parser.add_argument('--manifest', default='research/audio-manifest.json')
args = parser.parse_args()
root = Path('research/audio')
root.mkdir(exist_ok=True)
model = Kokoro('.models/kokoro/kokoro-v1.0.onnx', '.models/kokoro/voices-v1.0.bin',
    espeak_config=EspeakConfig(lib_path=espeakng_loader.get_library_path(), data_path=espeakng_loader.get_data_path()))
corpus = json.loads(Path(args.corpus).read_text())[:args.limit]
manifest = []
for passage in corpus:
    for voice in args.voices:
        pieces = []
        for i, sentence in enumerate(passage['sentences']):
            cached = root / f"{passage['id']}-{voice}-sentence-{i}.wav"
            if cached.exists():
                samples, sr = sf.read(cached, dtype='float32')
            else:
                samples, sr = model.create(sentence, voice=voice, speed=1.0, lang='en-us')
                sf.write(cached, samples, sr, subtype='PCM_16')
            pieces.append(np.concatenate([samples, np.zeros(int(sr * .25), dtype=np.float32)]))
        for kind in ['clean', 'omission', 'repetition', 'substitution']:
            chunks = list(pieces)
            spoken = list(passage['sentences'])
            fault = None
            if kind == 'omission':
                pos = sum(len(c) for c in chunks[:3]) / sr
                fault = {'start': pos, 'end': pos, 'expected': spoken[3], 'heard': ''}
                del chunks[3]
                del spoken[3]
            elif kind == 'repetition':
                pos = sum(len(c) for c in chunks[:6]) / sr
                fault = {'start': pos, 'end': pos + len(chunks[5])/sr, 'expected': '', 'heard': spoken[5]}
                chunks.insert(6, chunks[5])
                spoken.insert(6, spoken[5])
            elif kind == 'substitution':
                change = passage['change']; i = change['sentence']
                spoken[i] = spoken[i].replace(change['old'], change['new'])
                samples, sr = model.create(spoken[i], voice=voice, speed=1.0, lang='en-us')
                chunks[i] = np.concatenate([samples, np.zeros(int(sr * .25), dtype=np.float32)])
                pos = sum(len(c) for c in chunks[:i]) / sr
                fault = {'start': pos, 'end': pos + len(chunks[i])/sr, 'expected': change['old'], 'heard': change['new']}
            name = f"{passage['id']}-{voice}-{kind}"
            sf.write(root / (name + '.wav'), np.concatenate(chunks), sr, subtype='PCM_16')
            reference = ' '.join(passage['sentences'])
            (root / (name + '.txt')).write_text(reference, encoding='utf-8')
            manifest.append({'id': name, 'audio': str(root / (name+'.wav')), 'script': reference,
                'spoken': ' '.join(spoken), 'kind': kind, 'fault': fault, 'voice': voice,
                'duration': sum(len(c) for c in chunks)/sr})
            print(name, round(manifest[-1]['duration'], 1), flush=True)
Path(args.manifest).write_text(json.dumps(manifest, indent=2), encoding='utf-8')

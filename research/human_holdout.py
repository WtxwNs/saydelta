"""A fixed, external spoken-audio check; do not tune on its results.

LibriSpeech dev-clean speaker 1272, via HF's dummy subset. CC-BY-4.0.
Concatenation and one-utterance omission are disclosed transformations.
"""
import io
import json
from pathlib import Path
import numpy as np
import pyarrow.parquet as pq
import soundfile as sf
import urllib.request

dataset = Path('research/librispeech.parquet')
if not dataset.exists():
    url = 'https://huggingface.co/datasets/hf-internal-testing/librispeech_asr_dummy/resolve/main/clean/validation-00000-of-00001.parquet'
    with urllib.request.urlopen(url, timeout=60) as source:
        dataset.write_bytes(source.read())
Path('research/audio').mkdir(exist_ok=True)
data=pq.read_table('research/librispeech.parquet').to_pylist()
manifest=[]
for group,indices in enumerate([range(0,10),range(15,25),range(30,40)]):
    records=[data[i] for i in indices]
    audio=[]
    for item in records:
        samples,sr=sf.read(io.BytesIO(item['audio']['bytes']),dtype='float32')
        audio.append(np.concatenate([samples,np.zeros(int(.25*sr),dtype=np.float32)]))
    script=' '.join(item['text']+'.' for item in records)
    for kind in ['clean','omission']:
        chunks=list(audio);fault=None
        if kind=='omission':
            pos=sum(len(c) for c in chunks[:4])/sr
            fault={'start':pos,'end':pos,'expected':records[4]['text'],'heard':''}
            del chunks[4]
        name=f'human-{group}-{kind}'
        dest=Path('research/audio',name+'.wav')
        sf.write(dest,np.concatenate(chunks),sr,subtype='PCM_16')
        manifest.append({'id':name,'audio':str(dest),'script':script,'kind':kind,'fault':fault,
            'duration':sum(len(c) for c in chunks)/sr,'source_ids':[r['id'] for r in records]})
Path('research/human-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print([(r['id'],round(r['duration'],1)) for r in manifest])

"""Independent local re-recognition of suspect regions, without a script prompt.

Before running: only resolve when a UNIQUE expected context (six words each
side) reappears contiguously in fresh ASR. Never resolve repetitions or long
insertions this way: a correct copy could coexist with an extra copy.
Keep all first-pass findings and fresh evidence, not just remaining findings.
"""
import argparse
import json
import time
from pathlib import Path
from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from alignment_v2 import align,tokenize

parser=argparse.ArgumentParser()
parser.add_argument('--model',default='small.en')
parser.add_argument('--manifest',default='research/audio-manifest.json')
args=parser.parse_args()
model=WhisperModel('.models/'+args.model,device='cpu',compute_type='int8',cpu_threads=6)
rows=json.loads(Path(args.manifest).read_text());results=[]
for row in rows:
    recognition=json.loads(Path('research/audio',row['id']+'.'+args.model+'-no-vad.asr.json').read_text())
    findings=align(row['script'],recognition['words'],row['duration'])
    tokens=tokenize(row['script']); reference=[t.value for t in tokens]
    audio=None
    for finding in findings:
        finding['status']='review'
        # Minimum-edit alignment can leave a common word on the reference side
        # of a long insertion. Treat net word growth as insertion too.
        if finding['kind']=='repetition' or len(tokenize(finding['heard']))-len(tokenize(finding['expected']))>=3:
            continue
        a=next((i for i,t in enumerate(tokens) if t.begin>=finding['script_start']),len(tokens))
        b=next((i for i,t in enumerate(tokens) if t.begin>=finding['script_end']),len(tokens))
        expected=reference[max(0,a-6):min(len(reference),b+6)]
        joined=' '.join(expected)
        if len(expected)<8 or (' '.join(reference)).count(joined)!=1:
            continue
        if audio is None:audio=decode_audio(row['audio'])
        start=max(0,finding['start']-5);end=min(row['duration'],finding['end']+5)
        begin=time.monotonic()
        segments,_=model.transcribe(audio[int(start*16000):int(end*16000)],language='en',
            beam_size=5,vad_filter=False,condition_on_previous_text=False)
        heard=' '.join(s.text for s in segments)
        actual=' '.join(t.value for t in tokenize(heard))
        # Word-delimited matching, not arbitrary substring matching.
        reproduced=(' '+joined+' ') in (' '+actual+' ')
        finding['recheck']={'start':start,'end':end,'expected_context':joined,'heard':heard,
            'seconds':time.monotonic()-begin}
        if reproduced:finding['status']='not_reproduced'
    result={'id':row['id'],'duration':row['duration'],'kind':row['kind'],'fault':row['fault'],'findings':findings}
    results.append(result)
    print(row['id'],[(f['expected'],f['heard'],f['status']) for f in findings],flush=True)
Path('research/recheck-'+Path(args.manifest).stem+'-'+args.model+'.json').write_text(json.dumps(results,indent=2),encoding='utf-8')

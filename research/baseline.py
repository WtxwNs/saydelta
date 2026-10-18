"""Run TTSProof on the same audio and exact cached first-pass transcript.

No speed comparison: cached ASR deliberately makes this a paired output test.
Raise duration limit for the longer task; retain other stock checks and WER gate.
"""
import json
import argparse
from pathlib import Path
from ttsproof.runner import qa_sample
from ttsproof.config import Config

class CachedASR:
    def __init__(self,text):self.text=text
    def transcribe(self,*args):return self.text

parser=argparse.ArgumentParser()
parser.add_argument('--wer-threshold',type=float,default=.03)
args=parser.parse_args()
results=[]
for manifest in ['audio','holdout']:
    for row in json.loads(Path('research/'+manifest+'-manifest.json').read_text()):
        recognized=json.loads(Path('research/audio',row['id']+'.small.en-no-vad.asr.json').read_text())
        result=qa_sample(row['script'],row['audio'],sample_id=row['id'],
            asr=CachedASR(recognized['text']),config=Config(max_general_sec=1200,wer_threshold=args.wer_threshold))
        results.append({'kind':row['kind'],**result})
Path(f'research/ttsproof-baseline-{args.wer_threshold}.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
for row in results:
    print(row['id'],row['verdict'],'WER:',row['wer'],row['error_reason'])

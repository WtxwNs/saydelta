"""Evaluate known defects; report all clean findings conservatively as false alarms."""
import argparse
import json
from pathlib import Path
from alignment_v2 import align, tokenize

def canonical(text):
    return ' '.join(t.value for t in tokenize(text))

parser=argparse.ArgumentParser()
parser.add_argument('--model',default='base.en-no-vad')
parser.add_argument('--manifest',default='research/audio-manifest.json')
args=parser.parse_args()
rows=json.loads(Path(args.manifest).read_text())
results=[]
for row in rows:
    path=Path('research/audio',row['id']+'.'+args.model+'.asr.json')
    if not path.exists():
        raise SystemExit('Missing recognition: '+str(path))
    recognition=json.loads(path.read_text())
    findings=align(row['script'],recognition['words'],row['duration'])
    fault=row['fault']
    hit=None
    if fault:
        # Time intersection alone cannot establish a hit: content must match too.
        hit=any(f['start']<=fault['end'] and f['end']>=fault['start'] and
            (canonical(fault['expected']) in canonical(f['expected']) if fault['expected'] else
             canonical(fault['heard']) in canonical(f['heard'])) for f in findings)
    intervals=[]
    for f in sorted(findings,key=lambda f:f['start']):
        if intervals and f['start']<=intervals[-1][1]:intervals[-1][1]=max(intervals[-1][1],f['end'])
        else:intervals.append([f['start'],f['end']])
    reviewed=sum(end-start for start,end in intervals)
    results.append({'id':row['id'],'kind':row['kind'],'hit':hit,'duration':row['duration'],
        'review_fraction':reviewed/row['duration'],'findings':findings,'seconds':recognition['seconds']})
clean=[r for r in results if r['kind']=='clean']; altered=[r for r in results if r['kind']!='clean']
summary={'model':args.model,'defects_found':sum(bool(r['hit']) for r in altered),'defects_total':len(altered),
    'clean_suspects':sum(len(r['findings']) for r in clean),'clean_minutes':sum(r['duration'] for r in clean)/60,
    'max_review_fraction':max(r['review_fraction'] for r in altered),'results':results}
Path('research/evaluation-'+Path(args.manifest).stem+'-'+args.model+'.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in summary.items() if k!='results'},indent=2))
for r in results:print(r['id'],r['hit'],round(r['review_fraction'],3),[(f['expected'],f['heard']) for f in r['findings']])

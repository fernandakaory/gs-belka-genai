import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = [json.loads(line) for line in (ROOT / 'base/trechos.jsonl').read_text(encoding='utf8').splitlines() if line.strip()]
SOURCES = {s['id']: s for s in json.loads((ROOT / 'base/fontes.json').read_text(encoding='utf8'))}
STOP = {'sao','paulo','amanha','minuto','exato','exata','pessoal','prefeito','vizinho','casa','numero','endereco','rua','a','as','o','os','de','da','do','dos','das','em','no','na','um','uma','e','ou','para','por','com','que','se','qual','como','eu','me','minha','meu','tem','sobre','ao','aos','mais','pode','onde','nos','nas','essa','esse','ser','estou'}
def tokenize(s):
    s = ''.join(c for c in unicodedata.normalize('NFKD',s.lower()) if not unicodedata.combining(c))
    tokens=[]
    for t in re.findall(r'[a-z0-9]+',s):
        if t in STOP or len(t)<=2: continue
        for root, normalized in [('alag','alagamento'),('enchent','enchente'),('inund','inundacao'),('desliz','deslizamento'),('prepar','preparacao'),('prev','previsao'),('chuv','chuva'),('ri','risco')]:
            if t.startswith(root) and (root != 'ri' or t.startswith('risco')):
                t=normalized;break
        tokens.append(t)
    return tokens

CORPUS=[Counter(tokenize(c['topicos']+' '+c['texto'])) for c in CHUNKS]
DOC_FREQ=Counter(t for bag in CORPUS for t in bag)

def search(question, k=3, threshold=0.20):
    query=Counter(tokenize(question))
    if not query:
        return []
    scores=[]
    for chunk, bag in zip(CHUNKS,CORPUS):
        score=0.0
        for term,n in query.items():
            idf=math.log(1+(len(CHUNKS)-DOC_FREQ.get(term,0)+0.5)/(DOC_FREQ.get(term,0)+0.5))
            score+=idf * (bag.get(term,0)*2.2/(bag.get(term,0)+1.2)) * n
        score/=math.sqrt(max(len(query),1))
        if score>=threshold:
            scores.append({**chunk,'score':round(score,3),'fonte_url':SOURCES[chunk['fonte_id']]['url']})
    return sorted(scores,key=lambda x:(-x['score'],x['id']))[:k]

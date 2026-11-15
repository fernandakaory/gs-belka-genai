import json
from pathlib import Path
from app.knowledge import search
ROOT=Path(__file__).resolve().parents[1]

# Compara os trechos encontrados com o gabarito e conta buscas sem resposta.
def evaluate(threshold=0.20):
    cases=json.loads((ROOT/'avaliacao/casos_teste.json').read_text(encoding='utf8'))
    positives=[c for c in cases if c['respondivel']]
    counts={1:0,3:0}; false_positives=0
    for c in cases:
        hits=search(c['pergunta'],k=3,threshold=threshold)
        found=[h['id'] for h in hits]
        if c['respondivel']:
            for k in counts:
                if any(x in found[:k] for x in c['gabarito_trechos']):counts[k]+=1
        elif hits:false_positives+=1
    return {'limiar':threshold,'casos_respondiveis':len(positives),'casos_nao_consta':len(cases)-len(positives),
            'recall_at_1':round(counts[1]/len(positives),3),'recall_at_3':round(counts[3]/len(positives),3),
            'falsos_positivos_nao_consta':false_positives}

# Mostra os resultados para diferentes limites de pontuação.
if __name__=='__main__':
    print(json.dumps([evaluate(t) for t in (0.2,0.5,1.0,1.5,2.0)],indent=2,ensure_ascii=False))

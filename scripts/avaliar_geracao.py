"""Avalia respostas REAIS. Não usa demo; separa falhas por modelo.
Uso: python -m scripts.avaliar_geracao --modes baseline rag rag_lora agent agent_lora
"""
import argparse,asyncio,csv,json,time
from pathlib import Path
from app.service import answer
from app.knowledge import search
ROOT=Path(__file__).resolve().parents[1]

async def run(args):
    cases=json.loads((ROOT/'avaliacao/casos_teste.json').read_text(encoding='utf8'))
    if args.limit:cases=cases[:args.limit]
    rows=[]
    for mode in args.modes:
        for case in cases:
            row={'id':case['id'],'modo':mode,'respondivel':case['respondivel']}
            try:
                t=time.perf_counter()
                response=await answer(case['pergunta'],mode=mode,demo=False,enable_weather=args.weather)
                row.update({'json_valido':response['json_valido_modelo'],'citacoes_autorizadas':all(c in {h['id'] for h in search(case['pergunta'])}|{'WEATHER'} for c in response['citacoes']),
                  'tem_citacao':bool(response['citacoes']),'recusa':'não consta' in response['resposta'].lower(),
                  'recusa_correta':not case['respondivel'] and 'não consta' in response['resposta'].lower(),
                  'trecho_gabarito_encontrado':bool(set(case['gabarito_trechos']) & set(response['citacoes'])),
                  'resposta':response['resposta'],'citacoes':';'.join(response['citacoes']),'segundos':round(time.perf_counter()-t,2),
                  'ferramentas':';'.join(response['ferramentas']),'erro':''})
            except Exception as e:row.update({'erro':type(e).__name__+': '+str(e)})
            rows.append(row)
            print(mode,case['id'],'ERRO' if row.get('erro') else 'OK')
    out=ROOT/'avaliacao';out.mkdir(exist_ok=True)
    (out/'resultados_comparacao_reais.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
    columns=['id','modo','respondivel','json_valido','citacoes_autorizadas','tem_citacao','recusa','recusa_correta','trecho_gabarito_encontrado','resposta','citacoes','segundos','ferramentas','erro']
    with (out/'resultados_comparacao_reais.csv').open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=columns);w.writeheader();w.writerows(rows)
    summaries={}
    for mode in args.modes:
        sub=[x for x in rows if x['modo']==mode];valid=[x for x in sub if not x.get('erro')]
        summaries[mode]={'casos':len(sub),'executados':len(valid),'falhas_execucao':len(sub)-len(valid),'json_valido_taxa':round(sum(bool(x['json_valido']) for x in valid)/len(valid),3) if valid else None,'recusas_corretas':sum(bool(x['recusa_correta']) for x in valid),'gabarito_citado':sum(bool(x['trecho_gabarito_encontrado']) for x in valid),'nota':'citação não prova correção semântica; revisar manualmente'}
    (out/'placar_comparacao_reais.json').write_text(json.dumps(summaries,ensure_ascii=False,indent=2))
    print(json.dumps(summaries,indent=2,ensure_ascii=False))
    print('REVISÃO MANUAL: avaliar correção, apoio em fontes, alucinação e documentar cinco erros reais.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--limit',type=int);p.add_argument('--weather',action='store_true',help='permite consulta meteorológica em tempo real; desativada por padrão para comparações reproduzíveis')
    p.add_argument('--modes',nargs='+',choices=['baseline','rag','rag_lora','agent','agent_lora'],default=['baseline','rag','rag_lora','agent','agent_lora'])
    asyncio.run(run(p.parse_args()))

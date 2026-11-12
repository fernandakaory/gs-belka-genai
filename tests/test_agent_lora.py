import json
from pathlib import Path
from app.tools import select_tools,city_from_text
from app.service import decode, REFUSAL
ROOT=Path(__file__).resolve().parents[1]

def test_agent_chooses_weather_when_city_and_forecast():
    assert 'weather_forecast' in select_tools('Vai chover amanhã em São Paulo?')

def test_agent_avoids_weather_without_location():
    assert 'weather_forecast' not in select_tools('Vai chover amanhã?')

def test_cities_not_invented():
    assert city_from_text('Minha rua') == (None,None)

def test_invalid_citation_refused():
    r=decode(json.dumps({'resposta':'Tudo bem','citacoes':['K999']}),{'K01'},'agent',[],None,[])
    assert r['resposta']==REFUSAL and not r['json_valido_modelo']

def test_valid_agent_citation():
    r=decode(json.dumps({'resposta':'Evite alagamentos','citacoes':['K01']}),{'K01'},'agent',[],None,[])
    assert r['fundamentada']

def test_dataset_split_and_integrity():
    all_ids=[]
    for split in ('train','val','test'):
        samples=[json.loads(x) for x in (ROOT/f'treinamento/{split}.jsonl').read_text().splitlines()]
        assert len(samples)>=20
        all_ids += [x['id'] for x in samples]
        for sample in samples:
            output=json.loads(sample['mensagens'][-1]['content'])
            assert isinstance(output['citacoes'],list)
            assert all(c.startswith('K') for c in output['citacoes'])
    assert len(set(all_ids))==len(all_ids)

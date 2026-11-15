from fastapi.testclient import TestClient
from app.main import app
from app.knowledge import search

client=TestClient(app)
# Confere as rotas básicas, as respostas de demonstração e a busca.
def test_health():assert client.get('/health').status_code==200
def test_sources():assert client.get('/api/fontes').json()['quantidade_trechos']>=10
def test_refusal_unknown():
    r=client.post('/api/perguntar',json={'pergunta':'Qual o telefone pessoal do prefeito?','configuracao':'agent','demo':True})
    assert r.status_code==200
    assert 'não consta' in r.json()['resposta'].lower()
def test_demo_source():
    r=client.post('/api/perguntar',json={'pergunta':'Como me proteger de incêndio florestal?','demo':True})
    assert r.status_code==200
    assert r.json()['citacoes']
def test_validation():assert client.post('/api/perguntar',json={'pergunta':'oi'}).status_code==422
def test_search():assert search('onda de calor hidratação')
def test_no_hallucinated_reference():
    result=client.post('/api/perguntar',json={'pergunta':'Como agir durante enchente?','demo':True}).json()
    assert all(x in {h['id'] for h in search('Como agir durante enchente?')} for x in result['citacoes'])

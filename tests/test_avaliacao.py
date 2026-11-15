from unittest.mock import patch

from scripts.avaliar_geracao import citacoes_autorizadas


# Garante que o quarto trecho do agente seja aceito pelo avaliador.
def test_quarto_trecho_do_agente_e_permitido():
    hits = [{'id': f'K0{i}'} for i in range(1, 5)]
    with patch('scripts.avaliar_geracao.search', side_effect=lambda q, k: hits[:k]):
        response = {'citacoes': ['K04'], 'meteorologia': None}
        assert citacoes_autorizadas('pergunta', 'agent', response)
        assert citacoes_autorizadas('pergunta', 'agent_lora', response)
        assert not citacoes_autorizadas('pergunta', 'rag', response)
        assert not citacoes_autorizadas('pergunta', 'rag_lora', response)
        assert not citacoes_autorizadas('pergunta', 'baseline', response)


def test_fonte_meteorologica_exige_dados_da_consulta():
    with patch('scripts.avaliar_geracao.search', return_value=[]):
        response = {'citacoes': ['WEATHER'], 'meteorologia': None}
        assert not citacoes_autorizadas('pergunta', 'agent', response)
        response['meteorologia'] = {'fonte': 'Open-Meteo'}
        assert citacoes_autorizadas('pergunta', 'agent', response)

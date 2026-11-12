# Belka AI · Gen AI for Engineering — FIAP GS 2026.2

> **Protótipo acadêmico de orientação ambiental.** Não prevê desastres, não emite alertas oficiais e não substitui a Defesa Civil.

**Olhar longe. Proteger perto.**

## O que faz

- Busca de conhecimento rastreável com IDs K01–K24 e fontes S01–S09.
- Chat via FastAPI com **cinco configurações comparáveis**: baseline, RAG, RAG+LoRA, agente, agente+LoRA.
- LLM **local** via Ollama, com modelo padrão `qwen2.5:1.5b` (baixado pela pessoa que executa).
- Interface web navegável; consulta real ao Open-Meteo para precipitação prevista 24/72h e temperatura 72h.
- **Modo demonstração** sem LLM para testar o encadeamento (não deve ser contabilizado como avaliação de IA).
- Conjunto de teste com perguntas respondíveis e "não consta", avaliação de recall@1/recall@3 e avaliação comparativa da LLM.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
ollama pull qwen2.5:1.5b       # requer Ollama instalado; veja https://ollama.com
ollama serve                    # se não estiver em execução (outro terminal)
uvicorn app.main:app --reload
```

Abrir http://127.0.0.1:8000 ; documentação da API http://127.0.0.1:8000/docs . Para experimentar sem Ollama, marcar **Modo demonstração**. **O modo demo não realiza inferência por LLM.**

Para avaliar:

```bash
python -m pytest -q
python -m scripts.avaliar_busca
python -m scripts.avaliar_geracao      # executa LLM local: demora conforme hardware
# opcional ensaio de 3 casos: python -m scripts.avaliar_geracao --limit 3
```

Arquivos de saída de avaliação da LLM ficam em `avaliacao/resultados_comparacao_reais.{csv,json}` (ignorados pelo Git até revisão). Registre manualmente 5 erros reais, versões e métricas no relatório.

## Estrutura

```text
app/             FastAPI, busca, integração Open-Meteo, Ollama, site
base/            trechos JSONL, fontes com URL, condição de reutilização
avaliacao/       casos gabaritados e saídas reais geradas localmente
scripts/         recall@1, recall@3, confronto de cinco configurações
notebooks/       guia Jupyter para experimentos com saídas salvas
checks: tests/   testes automatizados da API e recuperação
docs/            arquitetura, ficha, relatório e pendências
```

## Mapa da rubrica FIAP

| Critério | Onde |
|---|---|
| Problema e casos "não consta" | `docs/ficha_tecnica.md`, `avaliacao/casos_teste.json` |
| Conhecimento em trechos com fonte | `base/trechos.jsonl`, `base/fontes.json` |
| Recall@1/@3 e limiar | `scripts/avaliar_busca.py` + execução documentada |
| JSON, citação e recusa | `app/service.py`, `tests/` |
| Agente comparado a RAG | `app/service.py`, `scripts/avaliar_geracao.py` |
| Placar de 3 configurações mínimas e 2 adicionais | `avaliacao/resultados_comparacao_reais.csv` após execução |
| Cinco erros reais | `docs/relatorio.md` após revisão |
| Reprodutibilidade | README, `requirements.txt`, testes, notebooks |

## Limites importantes

- O **agente** usa ferramenta de busca e Open-Meteo via roteamento determinístico, sem planejamento autônomo; `agent_lora` também usa adapter PEFT (após treino).
- Seleção lexical pode devolver resultados irrelevantes; validação de citação não comprova adequação da frase.
- Dados do Open-Meteo são previsões de modelos e **não** fornecem por si uma probabilidade de enchente/deslizamento/incêndio.
- Mensagens de orientação e citações precisam de revisão antes de um uso público.
- Interface e backend não estão publicados: publicação e validação em ambiente acessível são pendências.
- **Ver** `docs/pendencias_usuario.md` para tudo que depende da equipe.

## Referências

- Manual Belka v1.0 fornecido pela equipe (orientação, não especificação imutável).
- Desafio FIAP CitizenTech 2026.2, pp. 29–31, Gen AI for Engineering.
- Defesa Civil: https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/saiba-como-agir
- Open-Meteo: https://open-meteo.com/en/docs
- Flood API: https://open-meteo.com/en/docs/flood-api
- Ollama: https://github.com/ollama/ollama/blob/main/docs/api.md

## Integrantes (confirmar)

| Integrante | RM |
|---|---|
| Fernanda Kaory Saito | 551104 |
| João Pedro Borsato | 550294 |
| Maria Fernanda Camargo | 97956 |
| Pedro Lucas Nunes | 550366 |
| Vinícius Bernardino | 97888 |

---
## Extensão GS: LoRA + RAG + agente (09/11/2026)

Esta versão inclui **script para treinamento LoRA real (ainda não executado), dataset sintético supervisionado e suíte comparativa**, além de nove fontes catalogadas e 24 trechos curtos. O arquivo `docs/fontes_ampliadas.md` discrimina URLs e limites. O arquivo `docs/pendencias_usuario.md` é o checklist atualizado.

### Preparação
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-lora.txt
ollama pull qwen2.5:1.5b
```

### Treinamento local
```bash
python -m treinamento.treinar_lora --epochs 2 --rank 8
```
Treino em CPU é lento. A configuração sugerida utiliza Qwen2.5-1.5B-Instruct, PEFT LoRA, Grad Accum 8, comprimento 768 e salva o **adapter** em `outputs/belka-lora`. GPU Mac MPS poderá funcionar se houver memória suficiente; reduza `--max-length` se necessário, com cuidado para não cortar as respostas. Arquivo `requirements-lora.txt` tem dependências específicas (não instaladas no ambiente mínimo). **Nenhum checkpoint treinado foi incluído:** é necessário executar o treino real.

### Comparações e API
```bash
uvicorn app.main:app --reload
python -m scripts.avaliar_busca
python -m scripts.avaliar_geracao --modes baseline rag rag_lora agent agent_lora
pytest -q
```
Ollama é usado para os modos `baseline`, `rag`, `agent`. Adapter PEFT carregado via Transformers para `rag_lora`, `agent_lora`. Não afirma que o Ollama esteja rodando o adapter. A escolha de ferramentas do agente é um roteamento determinístico auditável (ver `docs/experimento_lora_agente.md`), com Open-Meteo somente se houver pedido de previsão e cidade reconhecida. A consulta de clima requer acesso à rede.

**Importante:** o dataset ensina JSON, orientação, citação e recusa. Não é um dataset de eventos rotulados; não permite prometer precisão de previsão de desastres. Sem dados de localização, hidrologia e vulnerabilidade não há risco local confiável. Nunca use a interface como sistema oficial de proteção civil.

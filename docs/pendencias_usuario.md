# Pendências para concluir a GS — Belka Gen AI

## Obrigatórias para evidências e nota
- [ ] **Rodar LoRA** com ambiente `requirements-lora.txt`: conferir RAM, espaço livre e tempo de treino; salvar `outputs/belka-lora` e `training_run.json` (não commitar checkpoints grandes nem dados pessoais).
- [ ] **Rodar Ollama** com `qwen2.5:1.5b` e a API; verificar sua versão de macOS e recursos do equipamento.
- [ ] **Executar comparativo real** `python -m scripts.avaliar_geracao` com as cinco configurações e incluir CSV/JSON de resultados interpretados no relatório.
- [ ] **Analisar cinco erros reais** do experimento (pergunta, resposta incorreta, causa provável, mudança sugerida e novo teste); não criar erros fictícios.
- [ ] **Revisar dataset e fontes** com a equipe e, idealmente, pessoa com conhecimento de Defesa Civil: respostas sintéticas podem simplificar informação demais.
- [ ] **Validar qualidade**: mínimo 1 conjunto de questões independente do treino, JSON real, recusa, fundamentação e métricas; testes automatizados não substituem revisão humana.
- [ ] **Preparar notebooks com saídas salvas** e capturas da execução real de LoRA, RAG, agente e comparação.
- [ ] **Revisar README e relatório** com métricas medidas e limitações reais da máquina.
- [ ] **Publicar repositório público no GitHub**, conferir clone limpo, link público, execução e anexar no Teams até **19/11/2026, 23h55**; somente um integrante da equipe faz o envio.

## Integração com o produto
- [ ] Confirmar contrato da API e conectar ao MVP Belka (frontend real e, se desejar, indicadores Gold do Big Data).
- [ ] Decidir se a primeira versão trabalha com cidades pré-cadastradas ou geocodificação com consentimento; não permitir que LLM invente localização.
- [ ] Validar disponibilidade e licença do Open-Meteo para o cenário da apresentação e da futura operação comercial.
- [ ] Publicar demonstração ou vídeo conforme exigências da disciplina e do MVP; evitar apresentar indicadores como alertas oficiais.

## Risco de escopo
- [ ] Confirmar com professor se LoRA + agente satisfaz a interpretação de treinamento local (ambos são oferecidos neste projeto, mas precisam de evidências reais).
- [ ] Antes de uso público, fazer revisão de conteúdo, conformidade/LGPD, disponibilidade, monitoramento e gestão de emergências com especialistas.

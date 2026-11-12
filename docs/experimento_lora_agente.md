# Protocolo experimental: LoRA + RAG + agente

## Hipótese
O LoRA melhora conformidade com JSON/citação/recusa e o agente melhora a recuperação de evidências atualizadas, comparado à LLM sem ferramentas. Não presumir ganho: medir.

## Condições
1. `baseline` Qwen puro via Ollama.
2. `rag` Qwen + busca local de trechos.
3. `rag_lora` Qwen ajustado por adapter PEFT + RAG.
4. `agent` Qwen + ferramentas selecionadas por regras + RAG + validação.
5. `agent_lora` Qwen LoRA + mesmas ferramentas + validação.

**Transparência:** o orquestrador de ferramenta desta versão é **roteamento determinístico de intenção**, não planejamento autônomo por LLM. Demonstra uso efetivo de ferramentas; caso o professor exija decisão autônoma do modelo, implementar e avaliar tool calling com controle de argumentos. Evitar chamar isso de agente autônomo pleno.

## Entradas e avaliação
- 17 casos na suíte original `avaliacao/casos_teste.json`, incluindo 5 não respondíveis. Amplie com perguntas independentes feitas pelos colegas.
- Dataset LoRA sintético: 138 train, 36 val, 36 test, criado com enunciados para ensinar resposta formatada; mesma evidência pode aparecer entre conjuntos.
- `scripts/avaliar_geracao.py` registra JSON válido, citação autorizada, recusa adequada, gabarito citado, latência, erros de execução.
- Revisar manualmente: acerto semântico, alucinações e **cinco erros reais**; citações permitidas não provam factualidade.
- `--weather` ativa API meteorológica. Deixar desligado no experimento controlado de conhecimento, pois clima muda e dificulta repetibilidade.
- Logar modelo, versão, hardware, dependências, data, latência e prompt. A inferência PEFT e a base Ollama usam motores diferentes; a comparação é aplicada, não isolação causal perfeita da LoRA.

## Segurança
- Não habilitar acesso a dados privados; cidades reconhecidas por allowlist; sem geolocalização automática.
- Em falha do Open-Meteo, não substituir por dados inventados ou antigos.
- Não derivar risco oficial de um limiar simplista de precipitação.

# Análise de cinco erros reais — Belka Gen AI

## Metodologia

Foram executadas 85 inferências reais, distribuídas entre 17 casos de teste e cinco configurações: baseline, RAG, RAG + LoRA, RAG + agente e RAG + LoRA + agente.

A análise abaixo identifica cinco ocorrências de falha observadas nas respostas, considerando adequação ao pedido, formato JSON e fundamentação nas evidências.

### Erro 1 — T03 / Baseline

**Problema:** a pergunta sobre sinais de deslizamento recebeu a resposta "Não consta na base consultada.", embora a base contenha orientações relevantes no trecho K03.

**Correção proposta:** utilizar recuperação de conhecimento e fornecer contexto pertinente antes da geração, com validação de saída estruturada.

### Erro 2 — T02 / RAG

**Problema:** a configuração RAG respondeu "Não consta na base consultada." a uma pergunta classificada como respondível. A avaliação também identificou JSON inválido.

**Correção proposta:** investigar a recuperação dos trechos e validar a saída da LLM antes de retorná-la.

### Erro 3 — T12 / RAG

**Problema:** a resposta afirmou corretamente que chuva prevista não garante enchentes, mas citou apenas K02. Esse trecho contém orientações preventivas e não sustenta integralmente a conclusão apresentada.

**Correção proposta:** priorizar K12, que aborda diretamente as limitações da previsão de chuva na determinação de enchentes.

### Erro 4 — T17 / RAG + LoRA + agente

**Problema:** ao receber uma pergunta sobre o minuto exato de um deslizamento, o modelo apresentou orientações gerais sem comunicar explicitamente que não é possível determinar esse horário com as evidências disponíveis.

**Correção proposta:** reforçar as instruções sobre incerteza e ausência de evidências suficientes, utilizando testes de recusa específicos.

### Erro 5 — T12 / RAG + LoRA + agente

**Problema:** o modelo explicou que chuva prevista não garante enchentes, mas citou K02 e K07 em vez do trecho K12. Também acrescentou uma orientação sobre áreas suscetíveis a deslizamentos, não solicitada diretamente na pergunta.

**Correção proposta:** melhorar a seleção das evidências e reduzir informações adicionais que não sejam necessárias para responder à pergunta.

## Limitações da avaliação

- JSON válido não garante qualidade semântica.
- Uma citação existente não garante fundamentação factual suficiente.
- A detecção automática de recusa depende de expressões predefinidas.
- As cinco ocorrências representam quatro perguntas distintas.
- As correções propostas não foram implementadas nem validadas experimentalmente.

## Conclusão

A comparação mostrou ganhos de conformidade estrutural com RAG, LoRA e agente. Entretanto, a combinação de todos os componentes não apresentou desempenho superior em todas as métricas.

Os resultados reforçam a necessidade de avaliar separadamente formato, recuperação, fundamentação e adequação das respostas, especialmente em uma aplicação que oferece orientações relacionadas à segurança da população.
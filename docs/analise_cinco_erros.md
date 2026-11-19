# Análise de cinco erros reais — Belka Gen AI

## Metodologia

Há 85 registros de avaliação, distribuídos entre 17 casos de teste e cinco configurações: baseline, RAG, RAG + LoRA, RAG + agente e RAG + LoRA + agente. Recusas sem evidência podem ser produzidas pelo serviço sem chamar o modelo.

A análise abaixo identifica cinco ocorrências de falha observadas nas respostas, considerando adequação ao pedido, formato JSON e fundamentação nas evidências.

### Erro 1 — T03 / Baseline

**Problema:** a pergunta sobre sinais de deslizamento recebeu a resposta "Não consta na base consultada.", embora a base contenha orientações relevantes no trecho K03.

**Causa observável:** o baseline não recebe K03 nem outros trechos. O registro também marca JSON inválido, situação em que o serviço substitui a saída por uma recusa. Como o texto bruto não foi salvo nesse arquivo, não é possível atribuir a recusa ao modelo ou identificar o erro exato de formato.

**Correção proposta:** utilizar recuperação de conhecimento e fornecer contexto relevante antes da geração, com validação de saída estruturada.

### Erro 2 — T02 / RAG

**Problema:** a configuração RAG respondeu "Não consta na base consultada." a uma pergunta classificada como respondível. A avaliação também identificou JSON inválido.

**Causa provável:** a saída foi rejeitada pela verificação de formato ou citações e substituída pela recusa padrão. O registro não preserva o texto bruto; por isso não confirma se a falha ocorreu na escrita do JSON, no formato dos campos ou nas citações.

**Correção proposta:** investigar a recuperação dos trechos e validar a saída da LLM antes de retorná-la.

### Erro 3 — T12 / RAG

**Problema:** a resposta afirmou corretamente que chuva prevista não garante enchentes, mas citou apenas K02. Esse trecho contém orientações preventivas e não apoia por completo a conclusão apresentada.

**Causa observável:** a verificação aceita um ID recuperado, mas não confere se o conteúdo desse trecho apoia cada afirmação. A citação K02 passa pela checagem de ID sem substituir a evidência mais direta de K12.

**Correção proposta:** priorizar K12, que aborda diretamente as limitações da previsão de chuva na determinação de enchentes.

### Erro 4 — T17 / RAG + LoRA + agente

**Problema:** ao receber uma pergunta sobre o minuto exato de um deslizamento, o modelo apresentou orientações gerais sem comunicar explicitamente que não é possível determinar esse horário com as evidências disponíveis.

**Causa provável:** a busca encontra trechos relacionados a deslizamentos e o modelo responde ao tema geral, ignorando a exigência de horário exato. A regra de validação do agente não detecta essa diferença entre a pergunta e o conteúdo respondido.

**Cuidado com a métrica:** esse registro marca K03 como não autorizado, mas o avaliador antigo conferia três trechos enquanto o agente usava quatro. A marcação precisa ser reavaliada antes de ser tratada como invenção de fonte.

**Correção proposta:** reforçar as instruções sobre incerteza e ausência de evidências suficientes, utilizando testes de recusa específicos.

### Erro 5 — T12 / RAG + LoRA + agente

**Problema:** o modelo explicou que chuva prevista não garante enchentes, mas citou K02 e K07 em vez do trecho K12. Também acrescentou uma orientação sobre áreas com risco de deslizamentos, não solicitada diretamente na pergunta.

**Causa provável:** o modelo combina recomendações dos trechos recuperados sem limitar a resposta ao pedido. A validação atual verifica os IDs, mas não o foco da resposta ou o apoio de cada frase na fonte citada.

**Correção proposta:** melhorar a seleção das evidências e reduzir informações adicionais que não sejam necessárias para responder à pergunta.

## Limitações da avaliação

- JSON válido não garante qualidade do conteúdo.
- Uma citação existente não garante fundamentação factual suficiente.
- A detecção automática de recusa depende de expressões predefinidas.
- As cinco ocorrências representam quatro perguntas distintas.
- As correções propostas não foram implementadas nem validadas experimentalmente.

## Conclusão

As configurações com RAG produziram mais respostas em JSON válido do que o baseline. Entre os modos avaliados, RAG + LoRA citou o gabarito em mais casos respondíveis (11 de 12) do que RAG + LoRA + agente (10 de 12).

Os resultados reforçam a necessidade de avaliar separadamente formato, recuperação, fundamentação e adequação das respostas, especialmente em uma aplicação que oferece orientações relacionadas à segurança da população.

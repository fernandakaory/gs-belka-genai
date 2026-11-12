# Dataset Belka LoRA (sintético, supervisionado)

- Objetivo: **seguir instruções, emitir JSON válido, citar trechos autorizados e recusar inferências sem base**. **NÃO** treina previsão de enchentes, deslizamentos ou alertas reais.
- Proveniência: exemplos autorais construídos a partir de paráfrases curtas dos trechos em `base/trechos.jsonl`, com fontes em `base/fontes.json`. Os registros de recusa e os enunciados são sintéticos. Não são notícias reais, ocorrências verificadas ou dados de indivíduos.
- Divisão: conjuntos `train`, `val`, `test` separados por famílias de prefixos de perguntas; os **temas e trechos de evidência se repetem** entre conjuntos. Portanto há generalização limitada e **não se deve chamar o test de avaliação independente de conhecimento factual**. O teste principal de eficácia usa `avaliacao/casos_teste.json` e revisão humana.
- Campos: id, familia, origem, trecho_referencia, mensagens(system,user,assistant).
- Cuidado: respostas de treino são sínteses autorais com fontes, não transcrições; especialistas devem revisar conteúdo antes de uso público.
- Para medir generalização verdadeira: criar holdout com fontes/temas não usados no treino e perguntas feitas por avaliadores independentes.

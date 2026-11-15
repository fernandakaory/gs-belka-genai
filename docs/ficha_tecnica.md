# Ficha técnica — Belka AI

**Problema:** pessoas expostas a eventos climáticos necessitam de explicações claras de orientações de prevenção, com fontes e sem invenção de alertas ou abrigos.

**Tarefa da IA:** responder perguntas educativas sobre enchentes, deslizamentos, incêndios e ondas de calor; buscar trechos com fonte, explicar limites das previsões e recusar perguntas sem suporte.

**Domínio acadêmico:** segurança comunitária / CitizenTech; integração com app Belka.

**Usuários:** cidadãos, lideranças comunitárias, agentes de apoio; linguagem simples e acessível.

**Entrada:** perguntas em PT-BR, opcional consulta manual de coordenadas para previsão meteorológica.

**Saída:** JSON com `resposta`, `citacoes`, `configuracao`, `fundamentada`, `aviso`.

**Modelo:** Qwen2.5 1.5B via Ollama nos modos originais e via Transformers/PEFT nos modos com LoRA. O ajuste LoRA já foi treinado; o agente escolhe ferramentas por regras da pergunta.

**Comparação:** baseline, RAG simples, RAG + LoRA, agente + RAG e agente + RAG + LoRA. São 17 perguntas por modo. O modelo base tem o mesmo nome, mas Ollama e PEFT usam programas diferentes para gerar respostas.

**Pontos que NÃO estão validados:** eficácia de prevenção, veracidade de todas as respostas, previsão probabilística de eventos, adequação jurídica para operação pública.

**ODS:** meta 11.5, pelo apoio informativo à prevenção de desastres; meta 13.3, pela educação sobre riscos climáticos. Não foi medida redução de danos ou melhora de compreensão pelos usuários.

**Impacto a medir:** compreensão das orientações e facilidade de encontrar informação com fonte, em testes futuros com usuários.

**Repositório:** https://github.com/fernandakaory/gs-belka-genai — acesso público ainda precisa ser confirmado.

**Vídeo:** [demonstração da Belka Gen AI no YouTube](https://youtu.be/IN0QhtyyTC8).

**MVP público:** URL ainda pendente.

**Integrantes:** Fernanda Kaory Saito — RM 551104; João Pedro Borsato — RM 550294; Maria Fernanda Camargo — RM 97956; Pedro Lucas Nunes — RM 550366; Vinícius Bernardino — RM 97888. Confirmar a composição antes da entrega.

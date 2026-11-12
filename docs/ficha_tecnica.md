# Ficha técnica — Belka AI

**Problema:** pessoas expostas a eventos climáticos necessitam de explicações claras de orientações de prevenção, com fontes e sem invenção de alertas ou abrigos.

**Tarefa da IA:** responder perguntas educativas sobre enchentes, deslizamentos, incêndios e ondas de calor; buscar trechos com fonte, explicar limites das previsões e recusar perguntas sem suporte.

**Domínio acadêmico:** segurança comunitária / CitizenTech; integração com app Belka.

**Usuários:** cidadãos, lideranças comunitárias, agentes de apoio; linguagem simples e acessível.

**Entrada:** perguntas em PT-BR, opcional consulta manual de coordenadas para previsão meteorológica.

**Saída:** JSON com `resposta`, `citacoes`, `configuracao`, `fundamentada`, `aviso`.

**Modelo:** Qwen2.5 1.5B via Ollama, configurável; inferência local, não treinamento de pesos. A especialização adotada é um agente com validação determinística pós-geração.

**Comparação:** (A) baseline sem contexto, (B) RAG lexical simples, (C) agente com RAG + guardrails. Mesma LLM e mesmas perguntas nas três modalidades.

**Pontos que NÃO estão validados:** eficácia de prevenção, veracidade de todas as respostas, previsão probabilística de eventos, adequação jurídica para operação pública.

**ODS:** ODS 11 e 13 são conexões propostas; avaliação de impacto ainda é futura.

**Integrantes:** Fernanda Kaory Saito — RM 551104; João Pedro Borsato — RM 550294; Maria Fernanda Camargo — RM 97956; Pedro Lucas Nunes — RM 550366; Vinícius Bernardino — RM 97888. Confirmar a composição antes da entrega.

# Ficha técnica — Belka AI

**Problema:** pessoas expostas a eventos climáticos necessitam de explicações claras de orientações de prevenção, com fontes e sem invenção de alertas ou abrigos.

**Tarefa da IA:** responder perguntas educativas sobre enchentes, deslizamentos, incêndios e ondas de calor; buscar trechos com fonte, explicar limites das previsões e recusar perguntas sem suporte.

**Domínio acadêmico:** segurança comunitária / CitizenTech;

**Usuários:** cidadãos, lideranças comunitárias, agentes de apoio; linguagem simples e acessível.

**Entrada:** perguntas em português, opcional consulta manual de coordenadas para previsão meteorológica.

**Saída:** JSON com `resposta`, `citacoes`, `configuracao`, `fundamentada`, `aviso`.

**Modelo:** Qwen2.5 1.5B via Ollama nos modos originais e via Transformers/PEFT nos modos com LoRA. O ajuste LoRA já foi treinado; o agente escolhe ferramentas por regras da pergunta.

**Comparação:** baseline, RAG simples, RAG + LoRA, agente + RAG e agente + RAG + LoRA. São 17 perguntas por modo. O modelo base tem o mesmo nome, mas Ollama e PEFT usam programas diferentes para gerar respostas.

**Pontos que NÃO estão validados:** eficácia de prevenção, veracidade de todas as respostas, previsão probabilística de eventos, adequação jurídica para operação pública.

**ODS:** meta 11.5, pelo apoio informativo à prevenção de desastres; meta 13.3, pela educação sobre riscos climáticos.

**Repositório:** https://github.com/fernandakaory/gs-belka-genai

**Vídeo:** [demonstração da Belka Gen AI no YouTube](https://youtu.be/IN0QhtyyTC8).

**MVP público:** [acessar a Belka AI](https://belka-api.salmonisland-04dfa6a6.brazilsouth.azurecontainerapps.io/).

**Disponibilidade do MVP:** a aplicação é hospedada na Azure e sua disponibilidade pelo link depende da disponibilidade de créditos da assinatura Azure for Students (Azure Student). Caso os créditos se esgotem, a aplicação poderá ficar indisponível.

**Integrantes:**   
Fernanda Kaory Saito — RM 551104  
João Pedro Borsato — RM 550294  
Maria Fernanda Camargo — RM 97956  
Pedro Lucas Nunes — RM 550366

# Pesquisa de fontes — 09/11/2026

Fontes verificadas na web. `base/fontes.json` contém a URL rastreável, e `base/trechos.jsonl` contém **paráfrases autorais curtas**, não reprodução integral de artigos.

| Fonte | Trechos novos | Utilidade | Limitação |
|---|---|---|---|
| [Defesa Civil Nacional](https://www.gov.br/mdr/pt-br/assuntos/protecao-e-defesa-civil/saiba-como-agir) | K24 | Cuidados diante de eventos | Recomendações gerais, não alertas atuais |
| [Ministério da Saúde — Ondas de Calor](https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/o/ondas-de-calor) | K13-K15 | Saúde, prevenção, grupos vulneráveis | Não define risco local via temperatura isolada |
| [Cemaden — Portais oficiais](https://www.gov.br/cemaden/pt-br/assuntos/briefing-cemaden-cenad/06-11-2026-briefing-cemaden-cenad) | K16-K18 | Painel, Georisk, REINDESC | Catálogo; não foi feita ingestão automática do conteúdo dos portais |
| [Cemaden Educação — prevenção](https://educacao.cemaden.gov.br/wp-content/uploads/cemaden-educacao/Campanha-Prevencao-Riscos-de-Desastres_SECLIMA-1.pdf) | K21 | Sinais e prevenção de deslizamento | Fonte educativa, não diagnóstico geotécnico |
| [Open-Meteo Forecast](https://open-meteo.com/en/docs) | K23 | Variáveis de previsão | Modelos de escala regional |
| [Open-Meteo Flood](https://open-meteo.com/en/docs/flood-api) | K22 | Vazão simulada e resolução de 5 km | Não representa alagamentos de rua |
| [Open-Meteo Historical Weather](https://open-meteo.com/en/docs/historical-weather-api) | K19 | Reanálise histórica | Não é histórico de previsão emitida |
| [Open-Meteo Historical Forecast](https://open-meteo.com/en/docs/historical-forecast-api) | K20 | Previsões arquivadas para avaliação | Cobertura deve ser verificada |

**Critério de inclusão:** domínio institucional, conexão com um dos quatro riscos, conteúdo verificável e limites explícitos. Não foram adicionados limiares de perigo arbitrários nem exemplos de alertas falsamente atribuídos à Defesa Civil.

**Para ampliar de verdade em escala:** integrar downloads oficiais autorizados, registrar data da versão, hash do documento, licença, trecho, URL e origem; testar recuperação antes de usar em público. O REINDESC e o Georisk são fontes futuras, não datasets já baixados.

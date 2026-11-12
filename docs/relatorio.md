# Relatório técnico — Belka Gen AI — preenchimento após experimentos

## 1. Objetivo e arquitetura
Especializar Qwen2.5 1.5B local em orientação ambiental com LoRA, RAG e ferramentas supervisionadas. O serviço **não prevê desastres** e não emite alertas oficiais. Ver `docs/experimento_lora_agente.md`.

## 2. Fontes e base
9 fontes catalogadas e 24 trechos em paráfrases com URL. Veja `docs/fontes_ampliadas.md`. Dataset LoRA sintético: 138 treino / 36 validação / 36 teste; ensina formato, citação e recusa, não classificação de risco real.

## 3. Recuperação já executada (após ampliação)
| Limiar | Recall@1 | Recall@3 | Falsos positivos em 5 negativas |
|---:|---:|---:|---:|
| 0.2 | 0.667 | 1.000 | 1 |
| 0.5 | 0.667 | 1.000 | 1 |
| 1.0 | 0.667 | 1.000 | 1 |
| 1.5 | 0.667 | 0.917 | 0 |
| 2.0 | 0.500 | 0.667 | 0 |

**Limiar exploratório:** 1,5 é conservador no teste atual (0 falsos positivos, Recall@3 0,917), mas implica perda de recuperação e requer avaliação independente. O padrão do protótipo permanece 0,2 para observação; não é seguro inferir riscos a partir dessa busca.

## 4. Condições de comparação
`baseline`, `rag`, `rag_lora`, `agent`, `agent_lora`. Comparar as três exigidas e apresentar também as duas adicionais; sem resultados de geração local ainda. O agente usa roteamento determinístico auditável; não é autônomo.

## 5. Placar a preencher após execução real
| Métrica | Baseline | RAG | RAG+LoRA | Agente | Agente+LoRA |
|---|---|---|---|---|---|
| JSON válido | Pendente | Pendente | Pendente | Pendente | Pendente |
| Recusa adequada | Pendente | Pendente | Pendente | Pendente | Pendente |
| Gabarito citado | Pendente | Pendente | Pendente | Pendente | Pendente |
| Factualidade (revisão) | Pendente | Pendente | Pendente | Pendente | Pendente |
| Latência | Pendente | Pendente | Pendente | Pendente | Pendente |

Salvar `avaliacao/resultados_comparacao_reais.csv` e `avaliacao/placar_comparacao_reais.json` e anexar evidência.

## 6. Cinco erros reais — preencher
| Caso | Pergunta | Resposta | Falha | Causa provável | Correção | Reavaliação |
|---|---|---|---|---|---|---|
| 1 | Pendente | Pendente | Pendente | Pendente | Pendente | Pendente |
| 2 | Pendente | Pendente | Pendente | Pendente | Pendente | Pendente |
| 3 | Pendente | Pendente | Pendente | Pendente | Pendente | Pendente |
| 4 | Pendente | Pendente | Pendente | Pendente | Pendente | Pendente |
| 5 | Pendente | Pendente | Pendente | Pendente | Pendente | Pendente |

## 7. Limites e evidências
Sem treinamento LoRA executado neste ambiente, sem checkpoint, sem resultados reais de inferência. O benchmark de recuperação é pequeno e relacionado à base; os testes automatizados não substituem validação semântica e revisão humana. GitHub, notebook com saídas e vídeo pendentes.

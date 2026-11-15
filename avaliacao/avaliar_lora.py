"""Avalia Qwen base e Qwen+LoRA no mesmo test.jsonl, sem treinar."""
import json
import time
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[1]
TEST_PATH = ROOT / "treinamento" / "test.jsonl"
ADAPTER_PATH = ROOT / "outputs" / "belka-lora"
OUTPUT_PATH = ROOT / "avaliacao" / "resultados_lora.json"
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"
MAX_NEW_TOKENS = 220
RECUSA = "Não consta na base consultada."


# Carrega os casos reservados para teste.
def ler_testes():
    with TEST_PATH.open(encoding="utf-8") as arquivo:
        casos = [json.loads(linha) for linha in arquivo if linha.strip()]
    if not casos:
        raise ValueError("O conjunto de teste está vazio.")
    return casos


# Confere o JSON, as citações e a decisão de recusar em relação ao gabarito.
def avaliar_resposta(texto, referencia):
    try:
        objeto = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        objeto = None
    valido = (
        isinstance(objeto, dict)
        and set(objeto) == {"resposta", "citacoes"}
        and isinstance(objeto["resposta"], str)
        and isinstance(objeto["citacoes"], list)
        and all(isinstance(item, str) for item in objeto["citacoes"])
    )
    citacoes = objeto["citacoes"] if valido else []
    resposta = objeto["resposta"] if valido else ""
    gabarito_recusa = referencia["resposta"] == RECUSA
    recusou = resposta.strip() == RECUSA
    return {
        "json_valido": valido,
        "recusa_esperada": gabarito_recusa,
        "recusou": recusou,
        "recusa_correta": recusou == gabarito_recusa,
        "citacoes_exatas": valido and set(citacoes) == set(referencia["citacoes"]),
        "citacoes_sem_inventar_ids": valido and set(citacoes).issubset(set(referencia["citacoes"])),
    }


# Gera uma resposta e mede o tempo gasto pelo modelo.
def gerar(modelo, tokenizer, mensagens, device):
    texto = tokenizer.apply_chat_template(
        mensagens, tokenize=False, add_generation_prompt=True
    )
    entrada = tokenizer(texto, return_tensors="pt", add_special_tokens=False).to(device)
    if entrada["input_ids"].shape[1] + MAX_NEW_TOKENS > modelo.config.max_position_embeddings:
        raise ValueError("A entrada excede o contexto suportado pelo modelo.")
    if device.type == "cuda":
        torch.cuda.synchronize()
    inicio = time.perf_counter()
    with torch.inference_mode():
        gerado = modelo.generate(
            **entrada,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
        )
    if device.type == "cuda":
        torch.cuda.synchronize()
    segundos = time.perf_counter() - inicio
    tokens = gerado[0, entrada["input_ids"].shape[1]:]
    return tokenizer.decode(tokens, skip_special_tokens=True).strip(), segundos


# Avalia todos os casos e reúne as medidas da configuração.
def executar_configuracao(nome, modelo, tokenizer, casos, device):
    saidas = []
    modelo.eval()
    for indice, caso in enumerate(casos, start=1):
        mensagens = caso["mensagens"]
        referencia = json.loads(mensagens[2]["content"])
        texto, segundos = gerar(modelo, tokenizer, mensagens[:2], device)
        medidas = avaliar_resposta(texto, referencia)
        saidas.append({
            "id": caso["id"],
            "familia": caso.get("familia"),
            "resposta_modelo": texto,
            "gabarito": referencia,
            "tempo_segundos": round(segundos, 4),
            **medidas,
        })
        print(f"{nome}: {indice}/{len(casos)} | {segundos:.2f}s | JSON={'OK' if medidas['json_valido'] else 'ERRO'}", flush=True)
    
    total = len(saidas)
    casos_recusa = [x for x in saidas if x["recusa_esperada"]]

    resumo = {
        "total": total,
        "json_valido": sum(x["json_valido"] for x in saidas),
        "decisao_recusa_correta": sum(
            x["json_valido"] and x["recusa_correta"]
            for x in saidas
        ),
        "recusas_esperadas": len(casos_recusa),
        "recusas_corretas": sum(
            x["json_valido"] and x["recusou"]
            for x in casos_recusa
        ),
        "citacoes_exatas": sum(x["citacoes_exatas"] for x in saidas),
        "citacoes_sem_inventar_ids": sum(
            x["citacoes_sem_inventar_ids"] for x in saidas
        ),
        "tempo_medio_segundos": round(
            sum(x["tempo_segundos"] for x in saidas) / total, 4
        ),
    }

    return {"resumo": resumo, "casos": saidas}


# Compara o modelo original e o modelo com LoRA usando os mesmos casos.
def main():
    casos = ler_testes()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    if device.type != "cuda":
        raise RuntimeError("CUDA não disponível. Não iniciar avaliação lenta na CPU.")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    modelo = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME, dtype=torch.float16
    ).to(device)
    modelo.generation_config.do_sample = False

    resultados = {
        "metodologia": {
            "modelo_base": MODEL_NAME,
            "adapter": str(ADAPTER_PATH.relative_to(ROOT)),
            "dataset": str(TEST_PATH.relative_to(ROOT)),
            "max_new_tokens": MAX_NEW_TOKENS,
            "do_sample": False,
            "observacao": "Métricas automáticas de formato e referência; não medem correção semântica ou alucinação.",
        }
    }
    resultados["qwen_original"] = executar_configuracao(
        "Qwen original", modelo, tokenizer, casos, device
    )
    modelo = PeftModel.from_pretrained(modelo, ADAPTER_PATH)
    resultados["qwen_lora"] = executar_configuracao(
        "Qwen + LoRA", modelo, tokenizer, casos, device
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(resultados, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nResultados salvos em:", OUTPUT_PATH)
    for nome in ("qwen_original", "qwen_lora"):
        print(nome, resultados[nome]["resumo"])


if __name__ == "__main__":
    main()

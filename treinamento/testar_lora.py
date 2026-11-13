
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
from app.service import SYSTEM

# Configurações
BASE_MODEL = "Qwen/Qwen2.5-1.5B-Instruct"
ADAPTER_PATH = Path(__file__).resolve().parents[1] / "outputs" / "belka-lora"

# Carrega o tokenizer e o modelo original
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)

modelo_base = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    dtype=torch.float16,
    device_map="cuda"
)

# Aplica o adapter LoRA treinado
modelo = PeftModel.from_pretrained(modelo_base, ADAPTER_PATH)
modelo.eval()

# Pergunta de demonstração

pergunta = (
    "Pergunta: Uma chuva forte significa que haverá um deslizamento de terra? "
    "Explique em até três frases, usando linguagem simples.\n"
    "Evidências: [K12] A previsão de chuva, isoladamente, não confirma "
    "a ocorrência de enchentes ou deslizamentos. É necessário considerar "
    "condições locais e acompanhar alertas oficiais."
)

mensagens = [
    {"role": "system", "content": SYSTEM},
    {"role": "user", "content": pergunta}
]

texto = tokenizer.apply_chat_template(
    mensagens,
    tokenize=False,
    add_generation_prompt=True
)

entradas = tokenizer(
    texto,
    return_tensors="pt",
    add_special_tokens=False
).to("cuda")


with torch.no_grad():
    saida = modelo.generate(
    **entradas,
    max_new_tokens=220,
    do_sample=False,
    pad_token_id=tokenizer.eos_token_id
)

resposta = tokenizer.decode(
    saida[0][entradas["input_ids"].shape[-1]:],
    skip_special_tokens=True
)

print("\n=== RESPOSTA QWEN + LORA ===")
print(resposta)

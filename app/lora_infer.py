"""Gera respostas com o modelo e o ajuste LoRA treinado."""
import asyncio, os
from functools import lru_cache

# Mantém o modelo carregado para reutilizá-lo nas próximas perguntas.
@lru_cache(maxsize=1)
def load():
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    adapter=os.getenv('BELKA_LORA_ADAPTER','outputs/belka-lora')
    base=os.getenv('BELKA_BASE_MODEL','Qwen/Qwen2.5-1.5B-Instruct')
    device='cuda' if torch.cuda.is_available() else ('mps' if getattr(torch.backends,'mps',None) and torch.backends.mps.is_available() else 'cpu')
    tok=AutoTokenizer.from_pretrained(base)
    model=AutoModelForCausalLM.from_pretrained(base,torch_dtype=torch.float16 if device=='cuda' else torch.float32)
    model=PeftModel.from_pretrained(model,adapter).to(device).eval()
    return model,tok,device

# Prepara a conversa e retorna somente a resposta nova do modelo.
def _generate(system,user):
    import torch
    model,tok,device=load()
    prompt=tok.apply_chat_template([{'role':'system','content':system},{'role':'user','content':user}],tokenize=False,add_generation_prompt=True)
    inputs=tok(prompt,return_tensors='pt').to(device)
    with torch.no_grad():output=model.generate(**inputs,max_new_tokens=300,do_sample=False,pad_token_id=tok.eos_token_id)
    return tok.decode(output[0][inputs['input_ids'].shape[-1]:],skip_special_tokens=True)

# Executa a geração sem bloquear as outras tarefas da API.
async def lora_generate(system,user):
    return await asyncio.to_thread(_generate,system,user)

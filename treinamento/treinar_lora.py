"""Fine-tuning supervisionado LoRA: Qwen2.5-1.5B-Instruct, sem carregar test."""
import argparse, json, os, random
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def read(split):
    return [json.loads(s) for s in (ROOT/f'treinamento/{split}.jsonl').read_text(encoding='utf8').splitlines() if s]

def train(args):
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import LoraConfig, get_peft_model
    random.seed(args.seed);torch.manual_seed(args.seed)
    model_name=args.model
    tokenizer=AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token_id is None:tokenizer.pad_token=tokenizer.eos_token
    device='cuda' if torch.cuda.is_available() else ('mps' if getattr(torch.backends,'mps',None) and torch.backends.mps.is_available() else 'cpu')
    dtype=torch.float16 if device=='cuda' else torch.float32
    model=AutoModelForCausalLM.from_pretrained(model_name,torch_dtype=dtype)
    model.to(device)
    model.config.use_cache=False
    model=get_peft_model(model,LoraConfig(r=args.rank,lora_alpha=args.rank*2,lora_dropout=0.05,bias='none',task_type='CAUSAL_LM',target_modules=['q_proj','v_proj']))
    model.train();model.print_trainable_parameters()

    def enc(example):
        msgs=example['mensagens'];prefix=tokenizer.apply_chat_template(msgs[:2],tokenize=False,add_generation_prompt=True)
        full=tokenizer.apply_chat_template(msgs,tokenize=False,add_generation_prompt=False)
        a=tokenizer(prefix,add_special_tokens=False)['input_ids'];b=tokenizer(full,add_special_tokens=False)['input_ids'][:args.max_length]
        labels=[-100]*min(len(a),len(b))+b[min(len(a),len(b)):]
        return {'ids':b,'labels':labels}
    data = [enc(x) for x in read('train')]
    val_data = [enc(x) for x in read('val')]

    if not any(any(i != -100 for i in x['labels']) for x in data):
        raise ValueError('max_length demasiado pequeno para incluir respostas')

    if not all(any(i != -100 for i in x['labels']) for x in val_data):
        raise ValueError('Existem exemplos de validacao sem tokens de resposta')
    optimizer=torch.optim.AdamW(model.parameters(),lr=args.lr)
    steps=0; losses=[]
    for ep in range(args.epochs):
        random.shuffle(data); optimizer.zero_grad()
        for n,item in enumerate(data):
            ids=torch.tensor([item['ids']],dtype=torch.long,device=device)
            labels=torch.tensor([item['labels']],dtype=torch.long,device=device)
            loss=model(input_ids=ids,labels=labels).loss/args.grad_accum
            loss.backward();losses.append(float(loss.detach().cpu())*args.grad_accum)
            if (n+1)%args.grad_accum==0 or n==len(data)-1:
                torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
                optimizer.step();optimizer.zero_grad();steps+=1
        train_loss = sum(losses[-len(data):]) / len(data)

        model.eval()
        val_losses = []

        with torch.no_grad():
            for item in val_data:
                ids = torch.tensor(
                    [item['ids']], dtype=torch.long, device=device
                )
                labels = torch.tensor(
                    [item['labels']], dtype=torch.long, device=device
                )

                loss = model(input_ids=ids, labels=labels).loss
                val_losses.append(float(loss.detach().cpu()))

        val_loss = sum(val_losses) / len(val_losses)

        print(
            f'epoca={ep+1} '
            f'loss_treino_medio={train_loss:.4f} '
            f'loss_validacao={val_loss:.4f}'
        )

        model.train()
        
    out=ROOT/args.output;out.mkdir(parents=True,exist_ok=True)
    model.save_pretrained(out);tokenizer.save_pretrained(out)
    info={'base_model':model_name,'device':device,'epochs':args.epochs,'rank':args.rank,'lr':args.lr,'grad_accum':args.grad_accum,'steps':steps,'seed':args.seed,'max_length':args.max_length,'loss_treino_final':sum(losses[-len(data):])/len(data),'nota':'Treinamento realizado. Medir qualidade no conjunto de teste separadamente.'}
    (out/'training_run.json').write_text(json.dumps(info,indent=2,ensure_ascii=False))
    print('Adapter salvo em',out)

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--model',default='Qwen/Qwen2.5-1.5B-Instruct');p.add_argument('--output',default='outputs/belka-lora')
    p.add_argument('--epochs',type=int,default=2);p.add_argument('--rank',type=int,default=8);p.add_argument('--lr',type=float,default=1e-4)
    p.add_argument('--grad-accum',type=int,default=8);p.add_argument('--max-length',type=int,default=768);p.add_argument('--seed',type=int,default=42)
    a=p.parse_args();train(a)

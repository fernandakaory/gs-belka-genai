import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
import httpx
from .knowledge import search, SOURCES, CHUNKS
from .service import answer
from .weather import forecast

# Configura a API e a pasta da interface.
app=FastAPI(title='Belka AI — Protótipo acadêmico',version='0.1.0',description='Assistente de orientação; não emite alertas oficiais.')
STATIC=Path(__file__).parent/'static'

# Define os campos aceitos ao enviar uma pergunta.
class Ask(BaseModel):
    pergunta:str=Field(min_length=3,max_length=500)
    configuracao:str=Field(default='agent',pattern='^(baseline|rag|rag_lora|agent|agent_lora)$')
    demo:bool=False
    limiar:float=Field(default=0.20,ge=0,le=10)

# Disponibiliza a interface, o estado da API e a consulta à base.
@app.get('/')
def homepage():return FileResponse(STATIC/'index.html')

@app.get('/health')
def health(): return {'status':'ok','versao':'0.1.0','llm':'Ollama local (configurável)','modo_demo_disponivel':True}

@app.get('/api/fontes')
def fontes():return {'fontes':list(SOURCES.values()),'quantidade_trechos':len(CHUNKS)}

@app.get('/api/busca')
def busca(pergunta:str,limiar:float=0.20):return {'resultados':search(pergunta,threshold=limiar)}

# Processa perguntas e informa quando o modelo local está indisponível.
@app.post('/api/perguntar')
async def perguntar(req:Ask):
    try: return await answer(req.pergunta,req.configuracao,req.demo,req.limiar)
    except httpx.HTTPError as e: raise HTTPException(503,detail='LLM local indisponível. Inicie Ollama e baixe o modelo, ou escolha modo demo.') from e

# Consulta a previsão e informa erros de coordenadas ou do serviço externo.
@app.get('/api/clima')
async def clima(latitude:float=-23.55,longitude:float=-46.63):
    try:return await forecast(latitude,longitude)
    except ValueError as e:raise HTTPException(422,detail=str(e)) from e
    except (httpx.HTTPError,KeyError,TypeError) as e:raise HTTPException(503,detail='Previsão meteorológica indisponível no momento; não exibir valores antigos como atuais.') from e

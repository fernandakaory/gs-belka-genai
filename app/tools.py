"""Usa apenas ferramentas permitidas, sem executar código criado pelo modelo."""
import re, unicodedata
from .knowledge import search
from .weather import forecast

# Usa coordenadas conhecidas para as cidades aceitas pela consulta.
CITIES={'sao paulo':(-23.5505,-46.6333),'rio de janeiro':(-22.9068,-43.1729),'curitiba':(-25.4284,-49.2733),'porto alegre':(-30.0346,-51.2177),'recife':(-8.0476,-34.8770),'belo horizonte':(-19.9167,-43.9345)}

# Remove diferenças de maiúsculas e acentos ao identificar a cidade.
def normalize(text):return ''.join(c for c in unicodedata.normalize('NFKD',text.lower()) if not unicodedata.combining(c))

def city_from_text(text):
    t=normalize(text)
    for name,coord in CITIES.items():
        if re.search(r'(?<!\w)'+re.escape(name)+r'(?!\w)',t):return name,coord
    return None,None

def select_tools(question):
    """Escolhe as ferramentas por palavras da pergunta e pela cidade informada."""
    q=normalize(question)
    meteorology=any(x in q for x in ['amanha','hoje','proxim','previsao','vai chover','tempo em','temperatura em','clima em'])
    city,coords=city_from_text(q)
    return ['rag_search']+(['weather_forecast'] if meteorology and coords else [])

# Busca os trechos e, quando permitido, consulta a previsão da cidade.
async def execute(question, threshold=.20, enable_weather=True):
    tools=select_tools(question)
    evidence={'trechos':search(question,k=4,threshold=threshold),'meteorologia':None,'erros':[]}
    if 'weather_forecast' in tools and enable_weather:
        city,coords=city_from_text(question)
        try:
            w=await forecast(*coords)
            evidence['meteorologia']={k:v for k,v in w.items() if k in ('fonte','url','obtido_em_utc','timezone','latitude_consultada','longitude_consultada','chuva_prevista_24h_mm','chuva_prevista_72h_mm','temperatura_maxima_72h_c','aviso')}
            evidence['meteorologia']['localidade_consultada']=city
        except Exception:
            evidence['erros'].append('Open-Meteo indisponível; sem previsão atual')
    return tools,evidence

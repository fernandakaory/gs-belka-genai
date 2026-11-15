from datetime import datetime, timezone
import httpx

URL='https://api.open-meteo.com/v1/forecast'

# Valida as coordenadas e consulta as próximas 72 horas no Open-Meteo.
async def forecast(latitude:float, longitude:float):
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        raise ValueError('Coordenadas inválidas')
    params={'latitude':latitude,'longitude':longitude,'hourly':'precipitation,temperature_2m,relative_humidity_2m',
            'forecast_hours':72,'timezone':'auto'}
    async with httpx.AsyncClient(timeout=12) as client:
        resp=await client.get(URL,params=params)
        resp.raise_for_status()
        data=resp.json()

    # Resume chuva e temperatura e mantém a origem e o horário da consulta.
    h=data['hourly']; rainfall=h['precipitation']; temp=h['temperature_2m']
    return {'fonte':'Open-Meteo Forecast API','url':URL, 'obtido_em_utc':datetime.now(timezone.utc).isoformat(),
            'timezone':data.get('timezone'),'latitude_consultada':latitude,'longitude_consultada':longitude,
            'chuva_prevista_24h_mm':round(sum(x or 0 for x in rainfall[:24]),1),
            'chuva_prevista_72h_mm':round(sum(x or 0 for x in rainfall),1),
            'temperatura_maxima_72h_c':round(max(x for x in temp if x is not None),1),
            'temperaturas_horarias_c':temp,'horarios':h['time'],
            'aviso':'Previsões meteorológicas não são alertas oficiais nem probabilidades de desastre.'}

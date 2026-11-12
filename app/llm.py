
import os
import httpx


RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "resposta": {
            "type": "string"
        },
        "citacoes": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 3
        }
    },
    "required": ["resposta", "citacoes"],
    "additionalProperties": False
}


async def ollama_generate(system: str, user: str):
    url = os.getenv(
        "OLLAMA_URL", "http://localhost:11434"
    ).rstrip("/") + "/api/chat"

    model = os.getenv("OLLAMA_MODEL", "qwen2.5:1.5b")

    payload = {
        "model": model,
        "stream": False,
        "format": RESPONSE_SCHEMA,
        "options": {
            "temperature": 0,
            "num_predict": 220
        },
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }

    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()

        data = response.json()
        return data["message"]["content"]



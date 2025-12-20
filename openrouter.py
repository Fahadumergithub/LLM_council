import httpx
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://streamlit.io",
    "X-Title": "LLM Council Prototype"
}


async def query_model(model: str, messages: list, timeout: float = 60.0):
    """
    Query a single model via OpenRouter.
    """

    if not OPENROUTER_API_KEY:
        return None

    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7
    }

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=HEADERS,
                json=payload
            )

        if response.status_code != 200:
            return None

        data = response.json()

        return {
            "content": data["choices"][0]["message"]["content"]
        }

    except Exception:
        return None

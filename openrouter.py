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
        print("❌ API key is missing!")
        return {"error": "API key not configured"}

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

        print(f"📡 Status Code: {response.status_code}")
        print(f"📡 Response: {response.text[:500]}")  # First 500 chars
        
        if response.status_code != 200:
            error_msg = response.text
            print(f"❌ Error Response: {error_msg}")
            return {"error": f"API returned status {response.status_code}: {error_msg}"}

        data = response.json()

        return {
            "content": data["choices"][0]["message"]["content"]
        }

    except httpx.TimeoutException:
        print("❌ Request timed out")
        return {"error": "Request timed out after 60 seconds"}
    except Exception as e:
        print(f"❌ Exception occurred: {type(e).__name__}: {str(e)}")
        return {"error": f"Exception: {str(e)}"}

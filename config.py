# config.py

# Your OpenRouter API Key
OPENROUTER_API_KEY = "your_api_key_here"

# The Council: These models provide the initial diverse perspectives
# Using the latest late-2025 free releases
COUNCIL_MODELS = {
    "Gemma 3 27B": "google/gemma-3-27b:free",
    "DeepSeek R1 Chimera": "tngtech/deepseek-r1t2-chimera:free",
    "Mistral Devstral 2": "mistralai/devstral-2-2512:free"
}

# The Judge: Specifically using Kimmy K (Kimi K2) from Moonshot
PRIMARY_JUDGE = "moonshotai/kimi-k2:free"

# Fallback Judges: Used only if Kimmy K is down. 
# These are kept separate from the council to ensure a "fresh set of eyes."
FALLBACK_JUDGES = [
    "meta-llama/llama-4-maverick:free",
    "xiaomi/mimo-v2-flash:free"
]

# UI Settings
APP_TITLE = "The LLM Council"
APP_ICON = "⚖️"

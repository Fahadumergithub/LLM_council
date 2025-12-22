import streamlit as st

# OpenRouter configuration
def get_api_key():
    try:
        return st.secrets["OPENROUTER_API_KEY"]
    except Exception:
        return None

OPENROUTER_API_KEY = None
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Members (4 verified free models with diversity)
COUNCIL_MODELS = [
    "xiaomi/mimo-v2-flash:free",                # #1 Reasoning + General (309B params, beats Claude!)
    "meta-llama/llama-3.3-70b-instruct:free",   # Strong multilingual + reasoning
    "google/gemma-3-27b-it:free",               # Multimodal (vision!) + 128K context
    "nvidia/nemotron-nano-12b-v2-vl:free"       # Multimodal (vision!) + OCR/charts
]

# Chairman Model (most powerful free model)
CHAIRMAN_MODEL = "xiaomi/mimo-v2-flash:free"  # 309B params, top performer

# Model display names for UI
MODEL_NAMES = {
    "xiaomi/mimo-v2-flash:free": "🏆 MiMo Flash (309B)",
    "meta-llama/llama-3.3-70b-instruct:free": "🦙 Llama 3.3 (70B)",
    "google/gemma-3-27b-it:free": "🎨 Gemma Vision (27B)",
    "nvidia/nemotron-nano-12b-v2-vl:free": "👁️ Nemotron Vision (12B)"
}

CHAIRMAN_NAME = "👑 MiMo Supreme Judge"

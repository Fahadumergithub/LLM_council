import streamlit as st

# OpenRouter configuration
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Council Members (4 diverse models)
COUNCIL_MODELS = [
    "qwen/qwen2.5-vl-7b-instruct:free",      # Multimodal vision specialist
    "google/gemma-3-12b:free",               # Reasoning + Math specialist
    "moonshotai/kimi-k2-0711:free",          # Coding + Agent specialist
    "google/gemma-3-4b:free"                 # Fast general-purpose
]

# Chairman Model (final decision maker)
CHAIRMAN_MODEL = "moonshotai/kimi-k2-0711:free"

# Model display names for UI
MODEL_NAMES = {
    "qwen/qwen2.5-vl-7b-instruct:free": "🎨 Qwen Vision Expert",
    "google/gemma-3-12b:free": "🧠 Gemma Reasoning Master",
    "moonshotai/kimi-k2-0711:free": "💻 Kimi Coding Specialist",
    "google/gemma-3-4b:free": "⚡ Gemma Quick Thinker"
}

CHAIRMAN_NAME = "👑 Kimi Supreme Judge"

import streamlit as st

# OpenRouter configuration (Streamlit-native secrets)
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Models (kept for future council expansion)
COUNCIL_MODELS = [
    "google/gemini-2.5-flash"
]

CHAIRMAN_MODEL = "google/gemini-2.5-flash"


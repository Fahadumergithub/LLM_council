import streamlit as st

# OpenRouter configuration (Streamlit-native secrets)
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Free model for testing
COUNCIL_MODELS = [
    "nex-agi/deepseek-v3.1-nex-n1:free"
]

CHAIRMAN_MODEL = "nex-agi/deepseek-v3.1-nex-n1:free"

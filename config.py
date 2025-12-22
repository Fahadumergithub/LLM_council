import streamlit as st

# API Key (Pulling from Streamlit Secrets)
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING"

# --- THE COUNCIL ---
# Replaced Devstral with Llama 3.3 70B
COUNCIL_MODELS = {
    "Gemma 3 (Google)": "google/gemma-3-27b-it:free",
    "Llama 3.3 (Meta)": "meta-llama/llama-3.3-70b-instruct:free",
    "R1 Chimera (DeepSeek)": "tngtech/deepseek-r1t2-chimera:free",
    "MiMo V2 (Xiaomi)": "xiaomi/mimo-v2-flash:free"
}

# --- THE JUDGE ---
PRIMARY_JUDGE = "moonshotai/kimi-k2-thinking" 

# Fallback models if Kimmy K is down
FALLBACK_JUDGES = [
    "meta-llama/llama-4-scout:free",
    "google/gemini-2.0-flash-exp:free"
]

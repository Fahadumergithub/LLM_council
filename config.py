import streamlit as st

# 1. API KEY (Set this in Streamlit Cloud Secrets)
# If running locally, this pulls from .streamlit/secrets.toml
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "PASTE_YOUR_KEY_HERE_FOR_LOCAL_TESTING"

# 2. THE COUNCIL (High IQ + Multimodal)
COUNCIL_MODELS = {
    "Gemma 3 (Google)": "google/gemma-3-27b-it:free",
    "Devstral 2 (Mistral)": "mistralai/devstral-2-2512:free",
    "R1 Chimera (DeepSeek)": "tngtech/deepseek-r1t2-chimera:free",
    "MiMo V2 (Xiaomi)": "xiaomi/mimo-v2-flash:free"
}

# 3. THE JUDGE (Moonshot Kimi)
PRIMARY_JUDGE = "moonshotai/kimi-k2-thinking" # High-reasoning expert

# 4. FALLBACKS (If Kimi is overloaded, use another Reasoning model)
FALLBACK_JUDGES = [
    "xiaomi/mimo-v2-flash:free",
    "google/gemini-2.0-flash-exp:free"
]

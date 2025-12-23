import streamlit as st

# API Key
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "PASTE_YOUR_KEY_HERE"

# --- THE COUNCIL (Verified Free Dec 2025) ---
COUNCIL_MODELS = {
    "Gemma 3 (Google)": "google/gemma-3-27b-it:free",
    "Llama 3.3 (Meta)": "meta-llama/llama-3.3-70b-instruct:free",
    "R1 Chimera (DeepSeek)": "tngtech/deepseek-r1t2-chimera:free",
    "MiMo V2 (Xiaomi)": "xiaomi/mimo-v2-flash:free"
}

# --- THE JUDGE ---
# This is the "General" Kimi K2 free endpoint
PRIMARY_JUDGE = "moonshotai/kimi-k2:free" 

# High-uptime fallbacks if Kimi is overloaded
FALLBACK_JUDGES = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free"
]

import streamlit as st

# API Key
try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except:
    OPENROUTER_API_KEY = "PASTE_YOUR_KEY_HERE"

# --- THE AVENGERS GROUPS ---
# Multimodal Specialists (Images/Vision)
VISION_HEROES = {
    "Iron Man (Gemma 3)": "google/gemma-3-27b-it:free",
    "Vision (Kimi VL)": "moonshotai/kimi-vl-a3b-thinking:free"
}

# Reasoning Specialists (Complex Text/PDFs)
LOGIC_HEROES = {
    "Captain (Llama 3.3)": "meta-llama/llama-3.3-70b-instruct:free",
    "Hulk (DeepSeek R1)": "tngtech/deepseek-r1t2-chimera:free"
}

# --- THE JUDGES ---
PRIMARY_JUDGE = "moonshotai/kimi-k2:free" 
FALLBACK_JUDGES = [
    "google/gemma-3-27b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free"
]

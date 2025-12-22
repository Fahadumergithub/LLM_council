import streamlit as st
import requests
import time

# API Settings
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# THE POWER COUNCIL - Current Top Tier Free Models (late 2025)
COUNCIL_MEMBERS = [
    # 1. Multimodal / Ultra Fast
    {"name": "Gemini 2.0 Flash", "id": "google/gemini-2.0-flash-exp:free"},
    # 2. Brand New / Multimodal (Google's latest open model)
    {"name": "Gemma 3 27B", "id": "google/gemma-3-27b:free"},
    # 3. High IQ / Reasoning (Comparable to Claude 3.5 Sonnet)
    {"name": "MiMo V2 Flash", "id": "xiaomi/mimo-v2-flash:free"},
    # 4. Expert Reasoning (DeepSeek architecture)
    {"name": "DeepSeek Chimera", "id": "tngtech/deepseek-r1t2-chimera:free"}
]

# The Judge (Reliable & Intelligent)
JUDGE_MODEL = "google/gemini-2.0-flash-exp:free"

def call_llm(model_id, prompt, system_prompt="You are a helpful assistant."):
    """Robust caller with increased timeouts and retries for free tier."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://github.com/Fahadumergithub/LLM_council",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    # Free tier can be flaky, so we try 3 times with longer waits
    for attempt in range(3):
        try:
            # Increased timeout to 45 seconds to prevent 'silent' errors
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=45)
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result:
                    return result['choices'][0]['message']['content']
                return f"⚠️ Error: No content returned from {model_id}"
            
            elif response.status_code == 429:
                time.sleep(5) # Wait 5 seconds if rate limited
                continue
            elif response.status_code == 404:
                return f"⚠️ 404: {model_id} is currently offline."
            else:
                return f"⚠️ Status {response.status_code}: {response.text}"
                
        except Exception as e:
            time.sleep(2)
            if attempt == 2:
                return f"❌ Connection Error: {str(e)}"
            
    return "❌ All retry attempts failed (The model is likely overloaded)."

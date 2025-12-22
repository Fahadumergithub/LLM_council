import time
import requests
import streamlit as st

# --- API CONFIG ---
# This pulls from your Streamlit Secrets
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- THE LLM COUNCIL ---
# We use a dictionary to keep track of model IDs and their "Display Names"
COUNCIL_MEMBERS = [
    {"name": "Llama 3.1", "id": "meta-llama/llama-3.1-8b-instruct:free"},
    {"name": "Mistral", "id": "mistralai/mistral-7b-instruct:free"},
    {"name": "Qwen", "id": "qwen/qwen-2.5-72b-instruct:free"},
    {"name": "Gemma", "id": "google/gemma-2-9b-it:free"}
]

JUDGE_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

def call_openrouter(model_id, prompt):
    """
    Standard function to call OpenRouter with built-in 
    'vibe-protection' (retries and delays).
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Fahadumergithub/LLM_council", # Optional
        "X-Title": "LLM Council", # Optional
    }
    
    data = {
        "model": model_id,
        "messages": [{"role": "user", "content": prompt}]
    }

    # Try up to 3 times if it fails (rate limits)
    for attempt in range(3):
        try:
            response = requests.post(BASE_URL, headers=headers, json=data)
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                # If rate limited, wait longer each time (2s, 4s, 8s)
                time.sleep(2 * (attempt + 1))
                continue
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Connection Failed: {str(e)}"
            
    return "Failed after multiple retries."

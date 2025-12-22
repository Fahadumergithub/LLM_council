import streamlit as st
import requests
import time

# API Settings
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# THE LLM COUNCIL - Updated for late 2024/2025 availability
# Note: I removed the 3.1 and Qwen 72b tags as they are causing your 404s.
COUNCIL_MEMBERS = [
    {"name": "Gemini Flash", "id": "google/gemini-2.0-flash-exp:free"},
    {"name": "Llama 3.2", "id": "meta-llama/llama-3.2-3b-instruct:free"},
    {"name": "Mistral 7B", "id": "mistralai/mistral-7b-instruct:free"},
    {"name": "Phi-3 Mini", "id": "microsoft/phi-3-mini-128k-instruct:free"}
]

# The Judge (Using the most reliable model for synthesis)
JUDGE_MODEL = "google/gemini-2.0-flash-exp:free"

def call_llm(model_id, prompt, system_prompt="You are a helpful assistant."):
    """Enhanced caller with error catching for 'vibe coding' stability."""
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

    for attempt in range(2): # Quick retry
        try:
            response = requests.post(BASE_URL, headers=headers, json=payload, timeout=30)
            result = response.json()
            
            if response.status_code == 200:
                # OpenRouter sometimes returns an error inside a 200 response
                if 'choices' in result:
                    return result['choices'][0]['message']['content']
                else:
                    return f"API logic error: {result.get('error', {}).get('message', 'Unknown error')}"
            
            elif response.status_code == 404:
                return "⚠️ Model Offline: This free model was recently removed from OpenRouter."
            elif response.status_code == 429:
                time.sleep(2) # Rate limit wait
                continue
            else:
                return f"Error {response.status_code}: {response.text}"
                
        except Exception as e:
            return f"Connection issues: {str(e)}"
            
    return "Council member is silent (timeout)."

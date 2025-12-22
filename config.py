import streamlit as st
import requests
import time

# API Settings
OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# The Council Members (Free Models)
COUNCIL_MEMBERS = [
    {"name": "Llama 3.1", "id": "meta-llama/llama-3.1-8b-instruct:free"},
    {"name": "Mistral 7B", "id": "mistralai/mistral-7b-instruct:free"},
    {"name": "Qwen 2.5", "id": "qwen/qwen-2.5-72b-instruct:free"},
    {"name": "Gemma 2", "id": "google/gemma-2-9b-it:free"}
]

# The Judge (Usually a smart model to synthesize information)
JUDGE_MODEL = "meta-llama/llama-3.1-8b-instruct:free"

def call_llm(model_id, prompt, system_prompt="You are a helpful assistant."):
    """Helper function to call OpenRouter with retries for free tier stability."""
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

    for attempt in range(3):  # Try 3 times
        try:
            response = requests.post(BASE_URL, headers=headers, json=payload)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            elif response.status_code == 429:
                time.sleep(3)  # Wait 3 seconds if rate limited
            else:
                return f"Error {response.status_code}: {response.text}"
        except Exception as e:
            time.sleep(2)
            continue
            
    return "The model is currently busy. Please try again in a moment."

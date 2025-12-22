import streamlit as st
import requests
import time
from config import OPENROUTER_API_KEY, COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="LLM Council", layout="wide")

# Persistent Debug Log
if "debug_log" not in st.session_state:
    st.session_state.debug_log = []

def call_llm(model_id, prompt, system_prompt="You are a helpful assistant."):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://llm-council.streamlit.app"
    }
    data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                 headers=headers, json=data, timeout=50)
        
        log_entry = f"Model: {model_id} | Code: {response.status_code}"
        st.session_state.debug_log.append(log_entry)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            st.session_state.debug_log.append(f"ERR: {response.text[:100]}")
            return None
    except Exception as e:
        st.session_state.debug_log.append(f"BOOM: {str(e)}")
        return None

st.title("⚖️ The LLM Council")

user_query = st.text_input("Ask the Council:", placeholder="Who discovered DNA?")

if st.button("Summon Council"):
    if user_query:
        st.session_state.debug_log = [] # Reset logs
        
        # 1. Council Phase
        council_responses = {}
        cols = st.columns(4)
        for i, (name, m_id) in enumerate(COUNCIL_MODELS.items()):
            with cols[i]:
                st.write(f"**{name}**")
                res = call_llm(m_id, user_query + " (Answer in exactly 2 lines)")
                if res:
                    st.info(res)
                    council_responses[name] = res
                else:
                    st.error("Model Offline")
            time.sleep(1) # Safety gap

        # 2. Judge Phase
        st.divider()
        st.subheader("👨‍⚖️ Kimmy K's Verdict")
        
        combined_text = "Analyze these anonymous replies:\n\n"
        for i, (name, resp) in enumerate(council_responses.items()):
            combined_text += f"Member {chr(65+i)}: {resp}\n\n"

        judges_to_try = [PRIMARY_JUDGE] + FALLBACK_JUDGES
        verdict = None

        with st.status("Judge is deliberating...") as status:
            for j_id in judges_to_try:
                status.write(f"Trying {j_id}...")
                verdict = call_llm(j_id, combined_text, "You are a lead judge. Provide a final summary.")
                if verdict:
                    status.update(label="Verdict Ready!", state="complete")
                    break
                else:
                    time.sleep(2)

        if verdict:
            st.success(verdict)
        else:
            st.error("The Judge is unavailable. Check the Debug Sidebar.")

# 🔍 Sidebar Debugging
with st.sidebar:
    st.header("🔍 System Logs")
    if st.button("Clear Debug"):
        st.session_state.debug_log = []
    for entry in reversed(st.session_state.debug_log):
        st.text(entry)

import streamlit as st
import requests
import json
import time
from config import OPENROUTER_API_KEY, COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="LLM Council", page_icon="⚖️", layout="wide")

# Custom Styling for that "Clean Previous Version" Look
st.markdown("""
    <style>
    .council-card {
        padding: 20px;
        border-radius: 12px;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        height: 100%;
    }
    .verdict-box {
        background-color: #fff9f0;
        padding: 30px;
        border-left: 8px solid #ffa94d;
        border-radius: 15px;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

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
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=80)
        return response.json()['choices'][0]['message']['content']
    except:
        return None

st.title("⚖️ The LLM Council")
st.write("Expert insights from the council, synthesized by **Kimmy K**.")

user_query = st.text_area("What is your question for the council?", placeholder="Ask anything...", height=100)

if st.button("Summon Council"):
    if not user_query:
        st.warning("Please enter a question.")
    else:
        # Phase 1: The Council Deliberation (Visible to User)
        st.subheader("🏛️ Council Deliberations")
        council_data = {}
        
        # Grid setup (2 rows, 2 columns)
        rows = [st.columns(2), st.columns(2)]
        cols = rows[0] + rows[1]
        
        for i, (name, m_id) in enumerate(COUNCIL_MODELS.items()):
            with cols[i]:
                st.markdown(f"### {name}")
                with st.status(f"{name} is responding...", expanded=True):
                    answer = call_llm(m_id, user_query)
                    if answer:
                        st.write(answer)
                        council_data[name] = answer
                    else:
                        st.error("Model failed to respond.")
            time.sleep(1) # Slight pause to help OpenRouter stability

        # Phase 2: Anonymize for the Judge
        # We strip the real names and replace them with Member Letters
        judge_payload = f"QUERY: {user_query}\n\n"
        for i, (name, resp) in enumerate(council_data.items()):
            letter = chr(65 + i) # A, B, C...
            judge_payload += f"--- RESPONSE FROM COUNCIL MEMBER {letter} ---\n{resp}\n\n"

        # Phase 3: The Verdict (Kimmy K)
        st.divider()
        st.subheader("👨‍⚖️ Final Verdict: Kimmy K (Moonshot)")
        
        with st.spinner("Kimmy K is analyzing anonymous testimonies..."):
            judge_sys = "You are Kimmy K, the lead judge. Review the following anonymous responses (Member A, B, etc.) and provide the final definitive answer."
            verdict = call_llm(PRIMARY_JUDGE, judge_payload, judge_sys)
            
            # Fallback Logic
            if not verdict:
                st.info("Primary judge is busy. Reaching out to a backup...")
                for fallback in FALLBACK_JUDGES:
                    verdict = call_llm(fallback, judge_payload, judge_sys)
                    if verdict: break

        if verdict:
            st.markdown(f'<div class="verdict-box">{verdict}</div>', unsafe_allow_html=True)
        else:
            st.error("Could not reach the judge. Please try again in a moment.")

st.sidebar.markdown("""
### Status
- **Council:** 4 Active Members
- **Judge:** Moonshot Kimi K2
- **Anonymity:** Active ✅
""")

import streamlit as st
import requests
import time
from config import OPENROUTER_API_KEY, COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="Avengers Council", page_icon="💥", layout="wide")

# --- AVENGERS THEME CSS ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #050A0E;
        color: #E7E7E7;
    }
    
    /* Global Titles */
    h1 {
        color: #F0131E !important; /* Marvel Red */
        font-family: 'Arial Black', sans-serif;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 2px 2px #000;
        text-align: center;
    }
    
    /* Council Cards */
    .hero-card {
        background: linear-gradient(145deg, #1e2639, #0b0930);
        border: 2px solid #4D8AB5;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 0 15px rgba(77, 138, 181, 0.3);
        height: 100%;
        margin-bottom: 15px;
    }
    
    /* Assemble Button */
    div.stButton > button {
        background-color: #F0131E !important;
        color: white !important;
        font-weight: bold !important;
        width: 100%;
        border-radius: 5px;
        border: 2px solid #C72523;
        font-size: 24px !important;
        padding: 10px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #ffffff !important;
        color: #F0131E !important;
        box-shadow: 0 0 20px #F0131E;
        transform: scale(1.02);
    }
    
    /* Verdict Shield Box */
    .verdict-shield {
        background: rgba(11, 9, 48, 0.9);
        border: 3px solid #F0131E;
        border-radius: 15px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 0 30px rgba(240, 19, 30, 0.4);
    }
    
    /* Model Status Colors */
    .stInfo { background-color: rgba(30, 38, 57, 0.8) !important; color: #fff !important; border-left: 5px solid #4D8AB5 !important; }
    </style>
""", unsafe_allow_html=True)

def call_llm(model_id, prompt, system_prompt="You are a hero assistant."):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://avengers-council.streamlit.app"
    }
    data = {
        "model": model_id,
        "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=50)
        return response.json()['choices'][0]['message']['content'] if response.status_code == 200 else None
    except:
        return None

# --- UI LAYOUT ---
st.markdown("<h1>💥 The Avengers Council 💥</h1>")
st.markdown("<p style='text-align: center; font-style: italic; color: #4D8AB5;'>Earth's Mightiest LLMs... Assemble.</p>", unsafe_allow_html=True)

user_query = st.text_input("GIVE THE COMMAND:", placeholder="Ex: How do we stop Thanos?")

if st.button("COUNCIL: ASSEMBLE!"):
    if user_query:
        # 1. Deliberation Phase
        council_responses = {}
        cols = st.columns(4)
        
        for i, (name, m_id) in enumerate(COUNCIL_MODELS.items()):
            with cols[i]:
                st.markdown(f"<div class='hero-card'><h3>{name}</h3>", unsafe_allow_html=True)
                with st.spinner("Analyzing..."):
                    res = call_llm(m_id, user_query + " (Respond in 2 lines like a tactical advisor)")
                    if res:
                        st.info(res)
                        council_responses[name] = res
                    else:
                        st.error("COMMS DOWN")
                st.markdown("</div>", unsafe_allow_html=True)
            time.sleep(1)

        # 2. Final Verdict Phase
        st.markdown("<br><hr style='border: 1px solid #4D8AB5;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: #E7E7E7;'>🛡️ STRATEGIC VERDICT: KIMMY K</h2>", unsafe_allow_html=True)
        
        combined_text = "Tactical Briefing:\n\n"
        for i, (name, resp) in enumerate(council_responses.items()):
            combined_text += f"Hero {chr(65+i)}: {resp}\n\n"

        verdict = None
        with st.status("Synthesizing Strategy...", expanded=True) as status:
            for j_id in [PRIMARY_JUDGE] + FALLBACK_JUDGES:
                verdict = call_llm(j_id, combined_text, "You are Kimmy K, lead tactical officer. Provide the final plan.")
                if verdict:
                    status.update(label="STRATEGY ACQUIRED", state="complete")
                    break
                time.sleep(1)

        if verdict:
            st.markdown(f"<div class='verdict-shield'>{verdict}</div>", unsafe_allow_html=True)
            st.balloons()

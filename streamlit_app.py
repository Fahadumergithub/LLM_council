import streamlit as st
import requests
import time
import base64
from config import OPENROUTER_API_KEY, VISION_HEROES, LOGIC_HEROES, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="Avengers Tactical Council", page_icon="💥", layout="wide")

# Avengers Theme CSS
st.markdown("""
    <style>
    .stApp { background-color: #050A0E; color: #E7E7E7; }
    h1 { color: #F0131E !important; font-family: 'Arial Black', sans-serif; text-transform: uppercase; text-align: center; }
    .hero-card { background: linear-gradient(145deg, #1e2639, #0b0930); border: 2px solid #4D8AB5; border-radius: 10px; padding: 15px; margin-bottom: 10px; min-height: 200px; }
    .verdict-shield { background: rgba(11, 9, 48, 0.9); border: 3px solid #F0131E; border-radius: 15px; padding: 20px; box-shadow: 0 0 20px rgba(240, 19, 30, 0.4); }
    </style>
""", unsafe_allow_html=True)

def encode_file(uploaded_file):
    if uploaded_file:
        b64 = base64.b64encode(uploaded_file.read()).decode('utf-8')
        return f"data:{uploaded_file.type};base64,{b64}"
    return None

def call_llm(model_id, content, system_prompt="Tactical Advisor."):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model_id, "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": content}]}
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=60)
        return r.json()['choices'][0]['message']['content'] if r.status_code == 200 else None
    except: return None

st.markdown("<h1>💥 AVENGERS TACTICAL COUNCIL 💥</h1>")

with st.container():
    col_in, col_at = st.columns([3, 1])
    user_query = col_in.text_input("GIVE THE COMMAND:", placeholder="Identify threat or analyze PDF...")
    uploaded_file = col_at.file_uploader("📂 ATTACHMENT", type=["png", "jpg", "pdf"])

if st.button("COUNCIL: ASSEMBLE!"):
    if user_query:
        # Step 1: Smart Model Selection
        is_image = uploaded_file and "image" in uploaded_file.type
        # If it's an image, use Vision heroes + top Logic heroes. If text/PDF, use all.
        active_council = {**VISION_HEROES, **LOGIC_HEROES}
        
        # Step 2: Prepare Payload
        file_url = encode_file(uploaded_file)
        content_payload = [{"type": "text", "text": f"{user_query} (Brief 2-line response)"}]
        
        if uploaded_file:
            if is_image:
                content_payload.append({"type": "image_url", "image_url": {"url": file_url}})
            else: # PDF
                content_payload.append({"type": "file", "file": {"name": uploaded_file.name, "data": file_url}})

        # Step 3: Execution
        results = {}
        cols = st.columns(len(active_council))
        for i, (name, m_id) in enumerate(active_council.items()):
            with cols[i]:
                st.markdown(f"<div class='hero-card'><h4>{name}</h4>", unsafe_allow_html=True)
                with st.spinner("Analyzing..."):
                    res = call_llm(m_id, content_payload)
                    if res:
                        st.info(res)
                        results[name] = res
                    else: st.error("OFFLINE")
                st.markdown("</div>", unsafe_allow_html=True)
            time.sleep(1)

        # Step 4: Final Verdict
        st.divider()
        judge_prompt = "Compare these hero reports and give the final tactical plan:\n\n" + "\n".join([f"{k}: {v}" for k,v in results.items()])
        
        with st.status("Judge Kimmy K is deliberating...") as status:
            final = None
            for j_id in [PRIMARY_JUDGE] + FALLBACK_JUDGES:
                final = call_llm(j_id, [{"type": "text", "text": judge_prompt}])
                if final: break
            
            if final:
                st.markdown(f"<div class='verdict-shield'><h3>👨‍⚖️ THE VERDICT</h3>{final}</div>", unsafe_allow_html=True)
                st.balloons()

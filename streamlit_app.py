import streamlit as st
import requests
import time
import base64
from config import OPENROUTER_API_KEY, VISION_HEROES, LOGIC_HEROES, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="Avengers Tactical Council", page_icon="💥", layout="wide")

# --- AVENGERS THEME CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050A0E; color: #E7E7E7; }
    h1 { color: #F0131E !important; font-family: 'Arial Black', sans-serif; text-transform: uppercase; text-align: center; text-shadow: 2px 2px #000; }
    .hero-card { background: linear-gradient(145deg, #1e2639, #0b0930); border: 2px solid #4D8AB5; border-radius: 10px; padding: 15px; margin-bottom: 10px; min-height: 250px;}
    div.stButton > button { background-color: #F0131E !important; color: white !important; font-weight: bold !important; width: 100%; font-size: 20px !important; border-radius: 5px; }
    .verdict-shield { background: rgba(11, 9, 48, 0.9); border: 3px solid #F0131E; border-radius: 15px; padding: 25px; box-shadow: 0 0 30px rgba(240, 19, 30, 0.4); }
    </style>
""", unsafe_allow_html=True)

# --- HELPER: FILE PROCESSING ---
def encode_file(uploaded_file):
    if uploaded_file is not None:
        file_bytes = uploaded_file.read()
        b64_string = base64.b64encode(file_bytes).decode('utf-8')
        return f"data:{uploaded_file.type};base64,{b64_string}"
    return None

def call_llm(model_id, content_list, system_prompt="You are a tactical advisor."):
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content_list}
        ]
    }
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        return None
    except:
        return None

# --- UI LAYOUT ---
st.markdown("<h1>💥 AVENGERS TACTICAL COUNCIL 💥</h1>")

with st.container():
    col_input, col_file = st.columns([3, 1])
    user_query = col_input.text_input("GIVE THE COMMAND:", placeholder="Analyze this X-ray or mission brief...")
    uploaded_file = col_file.file_uploader("📂 ATTACHMENT", type=["png", "jpg", "jpeg", "pdf"])

if st.button("COUNCIL: ASSEMBLE!"):
    if user_query:
        # 1. Smart Routing: Determine which heroes to call
        is_image = uploaded_file and "image" in uploaded_file.type
        
        # If image, we MUST include Vision heroes. 
        # For general text/PDFs, OpenRouter extracts text, so all heroes can participate.
        active_council = {**VISION_HEROES, **LOGIC_HEROES}
        
        # 2. Prepare Payload
        file_url = encode_file(uploaded_file)
        content_payload = [{"type": "text", "text": f"{user_query} (Answer in 2 lines like a tactical report)"}]
        
        if uploaded_file:
            if is_image:
                content_payload.append({"type": "image_url", "image_url": {"url": file_url}})
            else: # PDF
                content_payload.append({"type": "file", "file": {"name": uploaded_file.name, "data": file_url}})

        # 3. Council Deliberation
        council_results = {}
        cols = st.columns(len(active_council))
        
        for i, (name, m_id) in enumerate(active_council.items()):
            with cols[i]:
                icon = "👁️" if name in VISION_HEROES else "📄"
                st.markdown(f"<div class='hero-card'><h4>{name} {icon}</h4>", unsafe_allow_html=True)
                with st.spinner("Analyzing..."):
                    res = call_llm(m_id, content_payload)
                    if res:
                        st.info(res)
                        council_results[name] = res
                    else:
                        st.error("COMMS DOWN")
                st.markdown("</div>", unsafe_allow_html=True)
            time.sleep(1)

        # 4. Final Strategic Verdict
        st.divider()
        st.markdown("<h2 style='text-align: center;'>🛡️ STRATEGIC VERDICT</h2>", unsafe_allow_html=True)
        
        combined_brief = "Analyze these conflicting hero reports and provide the final directive:\n\n"
        for name, resp in council_results.items():
            combined_brief += f"{name}: {resp}\n\n"

        verdict = None
        with st.status("Judge Kimmy K is finalizing strategy...") as status:
            for j_id in [PRIMARY_JUDGE] + FALLBACK_JUDGES:
                verdict = call_llm(j_id, [{"type": "text", "text": combined_brief}], "You are the Supreme Commander.")
                if verdict:
                    status.update(label="STRATEGY ACQUIRED", state="complete")
                    break
                time.sleep(2)

        if verdict:
            st.markdown(f"<div class='verdict-shield'>{verdict}</div>", unsafe_allow_html=True)
            st.balloons()

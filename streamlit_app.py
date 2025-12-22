import streamlit as st
import requests
import json
from config import OPENROUTER_API_KEY, COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="LLM Council", layout="wide")

# --- CSS for the "Previous Version" Look ---
st.markdown("""
    <style>
    .model-card {
        border-radius: 10px;
        padding: 15px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
        border-left: 5px solid #4A90E2;
    }
    .judge-card {
        border-radius: 10px;
        padding: 20px;
        background-color: #fff4e6;
        border: 2px solid #ff922b;
    }
    </style>
""", unsafe_allow_html=True)

def call_llm(model_id, prompt, system_prompt="You are a helpful assistant."):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:8501", 
            },
            data=json.dumps({
                "model": model_id,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            }),
            timeout=30
        )
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

st.title("⚖️ The LLM Council")
st.caption("Council Members debate, Moonshot Kimi K2 (Kimmy K) decides.")

user_input = st.text_area("Enter your query:", placeholder="Ask the council anything...")

if st.button("Consult the Council"):
    if not user_input:
        st.warning("Please enter a prompt.")
    else:
        # 1. Gather Council Responses (Visible to User)
        st.subheader("🏛️ Council Deliberations")
        cols = st.columns(len(COUNCIL_MODELS))
        responses = {}
        
        for i, (name, model_id) in enumerate(COUNCIL_MODELS.items()):
            with cols[i]:
                with st.status(f"Consulting {name}...", expanded=True):
                    res = call_llm(model_id, user_input)
                    responses[name] = res
                    st.write(res)

        # 2. Prepare Anonymized Input for the Judge
        # We replace model names with "Council Member A, B, C..."
        anonymized_context = ""
        for i, (name, res) in enumerate(responses.items()):
            label = chr(65 + i) # A, B, C...
            anonymized_context += f"--- COUNCIL MEMBER {label} RESPONSE ---\n{res}\n\n"

        judge_system_prompt = (
            "You are the Lead Judge, Kimmy K from Moonshot. You will receive several responses "
            "to a user's prompt from anonymous council members. Your task is to analyze these "
            "different perspectives, identify the best insights, resolve any contradictions, "
            "and provide a final, authoritative synthesis for the user. Do not refer to the "
            "members by name (they are anonymous to you); refer to them as 'Member A', 'Member B', etc."
        )

        # 3. Call the Judge (with Fallback logic)
        st.divider()
        st.subheader("👨‍⚖️ Final Verdict (Kimmy K)")
        
        judge_placeholder = st.empty()
        with st.spinner("Kimmy K is deliberating..."):
            # Primary attempt
            final_verdict = call_llm(PRIMARY_JUDGE, anonymized_context, judge_system_prompt)
            
            # Fallback check
            if "Error" in final_verdict or not final_verdict:
                st.info("Kimmy K is currently unavailable. Calling a backup judge...")
                for fallback_id in FALLBACK_JUDGES:
                    final_verdict = call_llm(fallback_id, anonymized_context, judge_system_prompt)
                    if "Error" not in final_verdict:
                        break
        
        st.markdown(f"""
            <div class="judge-card">
                {final_verdict}
            </div>
        """, unsafe_allow_html=True)

st.sidebar.info("Council members are visible to you, but anonymous to Kimmy K to prevent bias.")

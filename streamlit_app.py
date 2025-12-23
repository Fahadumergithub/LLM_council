import streamlit as st
import requests
import time
from PIL import Image
import PyPDF2
from config import OPENROUTER_API_KEY, COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES

st.set_page_config(page_title="LLM Council", layout="wide")
st.title("⚖️ The LLM Council")

# -----------------------------
# Persistent Debug Log
# -----------------------------
if "debug_log" not in st.session_state:
    st.session_state.debug_log = []

# -----------------------------
# LLM Call
# -----------------------------
def call_llm(model_id, messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://llm-council.streamlit.app"
    }

    payload = {
        "model": model_id,
        "messages": messages
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )

        st.session_state.debug_log.append(
            f"Model: {model_id} | Status: {response.status_code}"
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.session_state.debug_log.append(response.text[:120])
            return None

    except Exception as e:
        st.session_state.debug_log.append(str(e))
        return None

# -----------------------------
# User Input
# -----------------------------
user_query = st.text_area(
    "Ask the Council",
    height=100,
    placeholder="Enter your question here"
)

# -----------------------------
# Attachments
# -----------------------------
uploaded_files = st.file_uploader(
    "Attach supporting material (PDF, images, text)",
    type=["pdf", "png", "jpg", "jpeg", "txt"],
    accept_multiple_files=True
)

extracted_text = ""

if uploaded_files:
    st.subheader("📎 Attachments")
    for file in uploaded_files:
        st.write(f"**{file.name}**")

        if file.type.startswith("image/"):
            img = Image.open(file)
            st.image(img, width=280)

        elif file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text += (page.extract_text() or "") + "\n"

        elif file.type == "text/plain":
            extracted_text += file.read().decode("utf-8") + "\n"

# -----------------------------
# Summon Council
# -----------------------------
if st.button("Summon Council"):
    if not user_query.strip() and not extracted_text.strip():
        st.warning("Please enter a question or attach a file.")
        st.stop()

    st.session_state.debug_log = []

    full_prompt = user_query
    if extracted_text:
        full_prompt += "\n\nSupporting material:\n" + extracted_text

    # -----------------------------
    # Council Phase
    # -----------------------------
    st.subheader("🧠 Council Deliberation")

    council_outputs = []
    cols = st.columns(len(COUNCIL_MODELS))

    for i, (name, model_id) in enumerate(COUNCIL_MODELS.items()):
        with cols[i]:
            st.markdown(f"**{name}**")
            with st.spinner("Thinking..."):
                response = call_llm(
                    model_id,
                    messages=[
                        {"role": "system", "content": "You are an expert advisor. Respond concisely and clearly."},
                        {"role": "user", "content": full_prompt}
                    ]
                )
            if response:
                st.info(response)
                council_outputs.append(response)
            else:
                st.error("Model unavailable")

        time.sleep(1)  # rate safety

    # -----------------------------
    # Judge Phase (Anonymous)
    # -----------------------------
    st.divider()
    st.subheader("👨‍⚖️ Chairman’s Synthesis")

    anonymous_bundle = (
        "You are the chairman of an expert council.\n"
        "Below are independent expert opinions provided anonymously.\n"
        "Synthesize them into a single, balanced, and well-reasoned response.\n\n"
    )

    for idx, text in enumerate(council_outputs, start=1):
        anonymous_bundle += f"Expert {idx}:\n{text}\n\n"

    verdict = None
    judges_to_try = [PRIMARY_JUDGE] + FALLBACK_JUDGES

    with st.status("Chairman is deliberating...", expanded=True) as status:
        for judge in judges_to_try:
            status.write(f"Consulting {judge}")
            verdict = call_llm(
                judge,
                messages=[
                    {"role": "system", "content": "You are a senior judge synthesising expert opinions."},
                    {"role": "user", "content": anonymous_bundle}
                ]
            )
            if verdict:
                status.update(label="Verdict ready", state="complete")
                break
            time.sleep(2)

    if verdict:
        st.success(verdict)
    else:
        st.error("Chairman unavailable. See system logs.")

# -----------------------------
# Debug Sidebar
# -----------------------------
with st.sidebar:
    st.header("🔍 System Logs")
    if st.button("Clear Logs"):
        st.session_state.debug_log = []
    for entry in reversed(st.session_state.debug_log):
        st.text(entry)


import streamlit as st
import requests
import time
import base64
import io
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
# Multimodal Capability Map
# -----------------------------
MULTIMODAL_MODELS = [
    "google/gemma-3-27b-it:free",
    "moonshotai/kimi-k2:free"
]

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
            f"{model_id} | {response.status_code}"
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            st.session_state.debug_log.append(response.text[:150])
            return None

    except Exception as e:
        st.session_state.debug_log.append(str(e))
        return None

# -----------------------------
# User Input
# -----------------------------
user_query = st.text_area(
    "Ask the Council",
    height=110,
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
image_payloads = []

if uploaded_files:
    st.subheader("📎 Attachments")

    for file in uploaded_files:
        st.write(f"**{file.name}**")

        if file.type.startswith("image/"):
            img = Image.open(file)
            st.image(img, width=280)

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_b64 = base64.b64encode(buffer.getvalue()).decode()
            image_payloads.append(img_b64)

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

            messages = [
                {"role": "system", "content": "You are an expert advisor. Respond clearly and concisely."},
                {"role": "user", "content": full_prompt}
            ]

            if image_payloads:
                if model_id in MULTIMODAL_MODELS:
                    for img in image_payloads:
                        messages.append({
                            "role": "user",
                            "content": [
                                {"type": "input_text", "text": "Analyse the following image."},
                                {"type": "input_image", "image_base64": img}
                            ]
                        })
                else:
                    st.warning("⚠️ This model cannot analyse images.")

            with st.spinner("Deliberating..."):
                response = call_llm(model_id, messages)

            if response:
                st.info(response)
                council_outputs.append(response)
            else:
                st.error("Model unavailable")

        time.sleep(1)

    # -----------------------------
    # Chairman Phase (Anonymous)
    # -----------------------------
    st.divider()
    st.subheader("👨‍⚖️ Chairman’s Verdict")

    synthesis_prompt = (
        "You are the chairman of an expert council.\n"
        "The following opinions were provided independently and anonymously.\n"
        "Synthesize them into a single, balanced, and well-reasoned response.\n\n"
    )

    for idx, text in enumerate(council_outputs, start=1):
        synthesis_prompt += f"Expert {idx}:\n{text}\n\n"

    verdict = None
    judges = [PRIMARY_JUDGE] + FALLBACK_JUDGES

    with st.status("Chairman deliberating...", expanded=True) as status:
        for judge in judges:
            status.write(f"Consulting {judge}")
            verdict = call_llm(
                judge,
                messages=[
                    {"role": "system", "content": "You are a senior judge synthesising expert opinions."},
                    {"role": "user", "content": synthesis_prompt}
                ]
            )
            if verdict:
                status.update(label="Verdict ready", state="complete")
                break
            time.sleep(2)

    if verdict:
        st.success(verdict)
    else:
        st.error("Chairman unavailable. See logs.")

# -----------------------------
# Debug Sidebar
# -----------------------------
with st.sidebar:
    st.header("🔍 System Logs")
    if st.button("Clear Logs"):
        st.session_state.debug_log = []
    for entry in reversed(st.session_state.debug_log):
        st.text(entry)

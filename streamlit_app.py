import streamlit as st
from openrouter import call_openrouter
from config import COUNCIL_MODELS, PRIMARY_JUDGE, FALLBACK_JUDGES
from PIL import Image
import PyPDF2

st.set_page_config(page_title="LLM Council", layout="wide")
st.title("🧠 LLM Council")

# -----------------------------
# User Question
# -----------------------------
user_question = st.text_area(
    "Enter your question",
    height=120
)

# -----------------------------
# Attachments
# -----------------------------
uploaded_files = st.file_uploader(
    "Attach files (PDF, images, text)",
    type=["pdf", "png", "jpg", "jpeg", "txt"],
    accept_multiple_files=True
)

extracted_text = ""

if uploaded_files:
    st.subheader("📎 Attachments")

    for file in uploaded_files:
        st.write(f"**{file.name}**")

        if file.type.startswith("image/"):
            image = Image.open(file)
            st.image(image, width=300)

        elif file.type == "application/pdf":
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                extracted_text += (page.extract_text() or "") + "\n"

        elif file.type == "text/plain":
            extracted_text += file.read().decode("utf-8") + "\n"

# -----------------------------
# Ask Council
# -----------------------------
if st.button("Ask LLM Council"):
    if not user_question.strip() and not extracted_text.strip():
        st.warning("Please enter a question or attach a file.")
        st.stop()

    with st.spinner("Council is deliberating..."):

        base_prompt = user_question
        if extracted_text:
            base_prompt += "\n\nAttached material:\n" + extracted_text

        council_outputs = []

        for name, model in COUNCIL_MODELS.items():
            response = call_openrouter(
                model,
                messages=[{"role": "user", "content": base_prompt}]
            )
            council_outputs.append((name, response))

        judge_prompt = (
            "You are the judge of an expert council.\n"
            "Your task is to synthesise the following expert opinions into a single, "
            "clear, balanced, and well-reasoned answer.\n\n"
        )

        for name, text in council_outputs:
            judge_prompt += f"{name}:\n{text}\n\n"

        try:
            final_answer = call_openrouter(
                PRIMARY_JUDGE,
                messages=[{"role": "user", "content": judge_prompt}]
            )
        except:
            fallback = FALLBACK_JUDGES[0]
            final_answer = call_openrouter(
                fallback,
                messages=[{"role": "user", "content": judge_prompt}]
            )

    st.subheader("✅ Final Judgement")
    st.write(final_answer)

import streamlit as st
from council import run_full_council
from openrouter import call_model

st.set_page_config(page_title="LLM Council Prototype")

st.title("LLM Council – Prototype")

mode = st.radio(
    "Select mode",
    ["Single model (Gemini)", "LLM Council"]
)

prompt = st.text_area("Enter prompt", height=200)

if st.button("Run"):
    if not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Running..."):
            if mode == "Single model (Gemini)":
                response = call_model(
                    model="google/gemini-pro",
                    prompt=prompt
                )
                st.subheader("Gemini Output")
                st.write(response)

            else:
                result = run_council(prompt)
                st.subheader("Council Output")
                st.write(result)


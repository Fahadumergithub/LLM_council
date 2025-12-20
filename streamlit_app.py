import streamlit as st
import asyncio
from openrouter import query_model

st.set_page_config(
    page_title="Gemini-only Test",
    layout="centered"
)

st.title("Gemini-only Test")
st.write("This verifies OpenRouter + Gemini connectivity.")

question = st.text_input("Enter your question:")

if st.button("Run"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying Gemini..."):

            async def run_query():
                messages = [{"role": "user", "content": question}]
                return await query_model(
                    model="google/gemini-2.5-flash",
                    messages=messages
                )

            result = asyncio.run(run_query())

        if result is None:
            st.error("Gemini did not return a response.")
        else:
            st.success("Response received")
            st.write(result.get("content", "No content returned"))

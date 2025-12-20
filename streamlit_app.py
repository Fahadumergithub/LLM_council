import streamlit as st
import asyncio
from openrouter import query_model

st.set_page_config(page_title="Gemini Test", layout="centered")

st.title("Gemini-only Test")
st.write("This verifies OpenRouter + Gemini connectivity.")

query = st.text_input("Enter your question:")

if st.button("Run"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Querying Gemini..."):
            async def run():
                messages = [{"role": "user", "content": query}]
                return await query_model("google/gemini-2.5-flash", messages)

            response = asyncio.run(run())

        if response is None:
            st.error("Gemini did not return a response.")
        else:
            st.success("Response received")
            st.write(response.get("content", "No content"))

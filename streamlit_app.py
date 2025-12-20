import streamlit as st
import asyncio
from openrouter import query_model

st.set_page_config(
    page_title="DeepSeek V3.1 Test",
    layout="centered"
)

st.title("🤖 DeepSeek V3.1 Nex N1 Test")
st.write("Testing **DeepSeek V3.1 Nex N1** (free) via OpenRouter")
st.caption("Good for general queries, coding, and agent tasks")

question = st.text_input(
    "Enter your question:", 
    placeholder="e.g., Explain quantum computing in simple terms"
)

if st.button("🚀 Run", type="primary"):
    if not question.strip():
        st.warning("⚠️ Please enter a question.")
    else:
        with st.spinner("🔄 Querying DeepSeek V3.1..."):

            async def run_query():
                messages = [{"role": "user", "content": question}]
                return await query_model(
                    model="nex-agi/deepseek-v3.1-nex-n1:free",
                    messages=messages
                )

            result = asyncio.run(run_query())

        if result is None:
            st.error("❌ No response received from the model.")
        elif "error" in result:
            st.error(f"❌ Error: {result['error']}")
            st.info("💡 Check the logs for more details")
        else:
            st.success("✅ Response received!")
            st.markdown("### Response:")
            st.write(result.get("content", "No content returned"))

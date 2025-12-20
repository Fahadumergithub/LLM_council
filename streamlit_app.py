import streamlit as st
import asyncio

# Import the correct function
from council import run_full_council

st.set_page_config(
    page_title="LLM Council",
    layout="wide"
)

st.title("LLM Council Prototype")
st.write(
    "This app compares responses from multiple LLMs, "
    "has them rank each other, and produces a final synthesized answer."
)

# User input
user_query = st.text_area(
    "Enter your question:",
    height=120,
    placeholder="Ask a question to the LLM Council..."
)

run_button = st.button("Run Council")

if run_button and user_query.strip():

    with st.spinner("Running LLM Council..."):
        try:
            # Run async council pipeline
            stage1, stage2, stage3, metadata = asyncio.run(
                run_full_council(user_query)
            )

            st.success("Council completed successfully")

            # -------------------------
            # Stage 3 – Final Answer
            # -------------------------
            st.subheader("Final Synthesized Answer")
            st.markdown(stage3["response"])

            # -------------------------
            # Stage 1 – Individual Responses
            # -------------------------
            st.subheader("Stage 1: Individual Model Responses")

            for item in stage1:
                with st.expander(f"Model: {item['model']}"):
                    st.markdown(item["response"])

            # -------------------------
            # Aggregate Rankings
            # -------------------------
            if metadata.get("aggregate_rankings"):
                st.subheader("Aggregate Rankings (Peer Review)")

                for rank in metadata["aggregate_rankings"]:
                    st.write(
                        f"**{rank['model']}** — "
                        f"Average Rank: {rank['average_rank']} "
                        f"(n={rank['rankings_count']})"
                    )

        except Exception as e:
            st.error("An error occurred while running the council.")
            st.exception(e)

else:
    st.info("Enter a question and click **Run Council**.")

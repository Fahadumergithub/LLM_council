import streamlit as st
import time
from config import COUNCIL_MEMBERS, JUDGE_MODEL, call_llm

st.set_page_config(page_title="LLM Council", page_icon="🏛️", layout="wide")

st.title("🏛️ LLM Council Decision System")
st.markdown("4 AI models debate, 1 judge decides • Powered by OpenRouter Free Models")

# Sidebar for settings
with st.sidebar:
    st.header("Council Settings")
    st.info("Currently using 4 free models to minimize costs.")
    if st.button("Clear History"):
        st.rerun()

# User Input
user_query = st.text_area("📝 Enter your question or problem for the Council:", placeholder="Should I learn Python or JavaScript first?")

if st.button("Gather the Council"):
    if not user_query:
        st.warning("Please enter a question first!")
    else:
        # --- STEP 1: COUNCIL RESPONSES ---
        st.subheader("🗣️ Step 1: Council Members Responding...")
        
        council_responses = []
        cols = st.columns(2) # Display responses in a grid
        
        progress_bar = st.progress(0)
        
        for i, member in enumerate(COUNCIL_MEMBERS):
            with cols[i % 2]:
                with st.expander(f"Opinion from {member['name']}", expanded=True):
                    with st.spinner(f"{member['name']} is thinking..."):
                        response = call_llm(member['id'], user_query)
                        st.write(response)
                        council_responses.append({"name": member['name'], "response": response})
                        # Small delay to prevent hitting Rate Limits
                        time.sleep(1.5) 
            
            progress_bar.progress((i + 1) / len(COUNCIL_MEMBERS))

        # --- STEP 2: THE JUDGE ---
        st.divider()
        st.subheader("⚖️ Step 2: The Judge's Final Verdict")
        
        # Prepare the prompt for the Judge
        council_text = "\n\n".join([f"Model {r['name']} said: {r['response']}" for r in council_responses])
        judge_prompt = f"""
        The following are responses from 4 different AI models regarding the user's question: '{user_query}'
        
        COUNCIL RESPONSES:
        {council_text}
        
        Based on the above opinions, provide a final, definitive answer. 
        Identify common themes, point out contradictions, and give the user the best possible advice.
        """
        
        with st.spinner("The Judge is reviewing the council's notes..."):
            final_decision = call_llm(JUDGE_MODEL, judge_prompt, system_prompt="You are a wise Lead Judge. Synthesize the council's opinions into one clear path forward.")
            
        st.success("### Final Decision")
        st.write(final_decision)
        
        st.balloons()

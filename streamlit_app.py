import streamlit as st
import time
from config import COUNCIL_MEMBERS, JUDGE_MODEL, call_llm

st.set_page_config(page_title="LLM Council", page_icon="🏛️", layout="wide")

st.title("🏛️ LLM Council: Power Edition")
st.markdown("Using the latest **Gemma 3**, **Gemini 2.0**, and **DeepSeek Chimera** models.")

user_query = st.text_area("📝 Enter your question:", placeholder="Ex: Explain quantum computing like I'm five.")

if st.button("⚖️ Summon the Council"):
    if not user_query:
        st.error("Please enter a question!")
    else:
        st.subheader("🗣️ The Council is Deliberating...")
        council_responses = []
        
        # Display in columns
        cols = st.columns(len(COUNCIL_MEMBERS))
        
        for i, member in enumerate(COUNCIL_MEMBERS):
            with cols[i]:
                st.markdown(f"**{member['name']}**")
                with st.spinner("Processing..."):
                    resp = call_llm(member['id'], user_query)
                    
                    if "⚠️" not in resp and "❌" not in resp:
                        st.success("Success")
                        st.write(resp)
                        council_responses.append(f"Model {member['name']}: {resp}")
                    else:
                        st.error("Offline")
                        st.caption(resp)
            
            # CRITICAL: 2 second delay between calls to avoid OpenRouter's 20 RPM limit
            time.sleep(2)

        # --- JUDGE PHASE ---
        st.divider()
        st.subheader("⚖️ Lead Judge Verdict")
        
        if not council_responses:
            st.warning("No valid responses from council members. The Judge cannot proceed.")
        else:
            with st.spinner("The Judge is synthesizing the council's wisdom..."):
                # Safety wait before Judge call
                time.sleep(2)
                
                context = "\n\n".join(council_responses)
                judge_prompt = f"""Summarize the following council responses to the question: "{user_query}"
                
                COUNCIL OPINIONS:
                {context}
                
                Synthesize a single best answer."""
                
                final_answer = call_llm(JUDGE_MODEL, judge_prompt, "You are a lead judge. Give a final, authoritative answer.")
                
                if "⚠️" in final_answer or "❌" in final_answer:
                    st.error("The Judge failed to respond. Try asking a simpler question or waiting a minute.")
                    st.caption(final_answer)
                else:
                    st.success("### 📜 Final Decision")
                    st.markdown(final_answer)
                    st.balloons()

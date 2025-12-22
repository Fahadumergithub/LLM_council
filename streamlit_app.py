import streamlit as st
import time
from config import COUNCIL_MEMBERS, JUDGE_MODEL, call_llm

# 1. Page Configuration
st.set_page_config(
    page_title="LLM Council Decision System",
    page_icon="🏛️",
    layout="wide"
)

# 2. UI Styling & Header
st.title("🏛️ LLM Council Decision System")
st.markdown("""
**The Process:** 4 AI models debate your question, and a Lead Judge synthesizes their opinions into a final verdict.
*Powered by OpenRouter Free Models.*
""")
st.divider()

# 3. Sidebar Configuration
with st.sidebar:
    st.header("Council Status")
    for member in COUNCIL_MEMBERS:
        st.write(f"✅ {member['name']} (Active)")
    st.info("Note: Using free models may occasionally result in slower response times.")
    if st.button("Reset Session"):
        st.rerun()

# 4. User Input Area
user_query = st.text_area(
    "📝 Enter your question or problem for the Council:",
    placeholder="Example: Should I invest in learning AI coding or traditional software engineering?",
    height=100
)

# 5. The Logic Flow
if st.button("⚖️ Convene the Council"):
    if not user_query:
        st.warning("Please enter a question for the council to consider.")
    else:
        # --- STEP 1: COUNCIL DELIBERATION ---
        st.subheader("🗣️ Step 1: Council Members Responding...")
        
        # We store valid responses here for the judge to read later
        council_responses = []
        
        # Create a grid for the 4 models
        col1, col2 = st.columns(2)
        cols = [col1, col2, col1, col2] # Alternating layout
        
        progress_bar = st.progress(0)
        
        for i, member in enumerate(COUNCIL_MEMBERS):
            with cols[i]:
                with st.expander(f"Opinion from {member['name']}", expanded=True):
                    with st.spinner(f"Querying {member['name']}..."):
                        response = call_llm(member['id'], user_query)
                        
                        # Filter out errors so they don't confuse the Judge
                        if "Error" in response or "⚠️" in response or "Failed" in response:
                            st.error(f"Member Offline: {member['name']}")
                            st.caption(response) # Show small error for debugging
                        else:
                            st.write(response)
                            council_responses.append({
                                "name": member['name'],
                                "opinion": response
                            })
            
            # Progress update
            progress_bar.progress((i + 1) / len(COUNCIL_MEMBERS))
            
            # CRITICAL: 1.5s delay to prevent the "429 Too Many Requests" error
            time.sleep(1.5)

        # --- STEP 2: THE JUDGE'S VERDICT ---
        st.divider()
        st.subheader("⚖️ Step 2: The Judge's Final Verdict")

        if len(council_responses) == 0:
            st.error("Total Failure: All council members are currently offline or rate-limited. Please try again in 1 minute.")
        else:
            # Build the context for the judge
            judge_context = "\n\n".join([f"MODEL {r['name']} OPINION:\n{r['opinion']}" for r in council_responses])
            
            judge_prompt = f"""
            You are the Lead Judge of a high-level AI council. 
            Below are opinions from different AI models regarding this question: "{user_query}"
            
            --- COUNCIL DATA ---
            {judge_context}
            --- END DATA ---
            
            Your task:
            1. Summarize the key points of agreement.
            2. Highlight any major contradictions between the models.
            3. Provide a final, definitive recommendation to the user based on the collective wisdom provided.
            """

            with st.spinner("The Judge is synthesizing the council's arguments..."):
                final_decision = call_llm(JUDGE_MODEL, judge_prompt, "You are a wise Lead Judge. Be decisive and helpful.")
                
            if "Error" in final_decision:
                st.error("The Judge was unable to reach a verdict. Please try again.")
            else:
                st.success("### 📜 The Official Verdict")
                st.markdown(final_decision)
                st.balloons()

# 6. Footer
st.markdown("---")
st.caption("LLM Council Prototype • Created for 'Vibe Coding' Experimentation")

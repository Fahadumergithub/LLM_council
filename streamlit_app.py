import streamlit as st
import asyncio
from council import get_council_responses, chairman_rank_responses, parse_ranking
from config import MODEL_NAMES, CHAIRMAN_NAME

st.set_page_config(
    page_title="🏛️ LLM Council",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better visuals
st.markdown("""
<style>
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    .model-card {
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #ddd;
        margin-bottom: 1rem;
        background-color: #f9f9f9;
    }
    .rank-1 { border-color: #FFD700; background-color: #FFFACD; }
    .rank-2 { border-color: #C0C0C0; background-color: #F5F5F5; }
    .rank-3 { border-color: #CD7F32; background-color: #FFF8DC; }
    .rank-4 { border-color: #A9A9A9; background-color: #F0F0F0; }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🏛️ LLM Council Decision System")
st.markdown("**4 AI models debate, 1 judge decides** • Powered by OpenRouter Free Models")

# Sidebar info
with st.sidebar:
    st.header("🎯 Council Members")
    for model, name in MODEL_NAMES.items():
        st.markdown(f"**{name}**")
        st.caption(model.split("/")[1].replace(":free", ""))
    
    st.divider()
    st.header("👑 Chairman")
    st.markdown(f"**{CHAIRMAN_NAME}**")
    st.caption("Final decision maker")
    
    st.divider()
    st.markdown("### How it works:")
    st.markdown("""
    1️⃣ **Council debates** - 4 models answer independently
    
    2️⃣ **Anonymous review** - Chairman sees shuffled responses
    
    3️⃣ **Ranking** - Best to worst
    
    4️⃣ **Winner announced** - Top response revealed
    """)

# Main interface
question = st.text_area(
    "📝 Enter your question:",
    placeholder="e.g., Explain quantum entanglement in simple terms\nor\nWrite a Python function to detect palindromes",
    height=100
)

col1, col2 = st.columns([1, 5])
with col1:
    run_button = st.button("🚀 Start Council", type="primary", use_container_width=True)
with col2:
    if st.button("🔄 Clear Results", use_container_width=True):
        st.rerun()

if run_button:
    if not question.strip():
        st.warning("⚠️ Please enter a question first!")
    else:
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Step 1: Council Responses
        status_text.markdown("### 🗣️ Step 1: Council Members Responding...")
        progress_bar.progress(25)
        
        async def run_council():
            return await get_council_responses(question)
        
        council_responses = asyncio.run(run_council())
        
        if not council_responses:
            st.error("❌ Failed to get responses from council members")
            st.stop()
        
        # Display council responses
        status_text.markdown("### ✅ Step 1 Complete: All Council Members Responded")
        progress_bar.progress(50)
        
        with st.expander("📋 View All Council Responses", expanded=True):
            cols = st.columns(2)
            for i, resp in enumerate(council_responses):
                with cols[i % 2]:
                    st.markdown(f"**{resp['name']}**")
                    st.info(resp['response'][:300] + "..." if len(resp['response']) > 300 else resp['response'])
        
        st.divider()
        
        # Step 2: Chairman Ranking
        status_text.markdown("### 🤔 Step 2: Chairman Analyzing Responses (Anonymous)...")
        progress_bar.progress(75)
        
        async def run_ranking():
            return await chairman_rank_responses(question, council_responses)
        
        chairman_output, anonymous_responses = asyncio.run(run_ranking())
        
        if not chairman_output:
            st.error("❌ Chairman failed to rank responses")
            st.stop()
        
        # Step 3: Parse and Display Results
        status_text.markdown("### 🏆 Step 3: Final Rankings Revealed!")
        progress_bar.progress(100)
        
        ranked_responses, reasoning = parse_ranking(chairman_output, anonymous_responses)
        
        st.success("✅ Council Decision Complete!")
        
        # Display Rankings
        st.markdown("## 🏅 Final Rankings")
        
        if ranked_responses:
            ranks = ["🥇 1st Place", "🥈 2nd Place", "🥉 3rd Place", "4th Place"]
            rank_classes = ["rank-1", "rank-2", "rank-3", "rank-4"]
            
            for i, resp in enumerate(ranked_responses):
                st.markdown(f"### {ranks[i]}: {resp['name']}")
                with st.container():
                    st.markdown(f'<div class="model-card {rank_classes[i]}">', unsafe_allow_html=True)
                    st.markdown(resp['response'])
                    st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("")
        
        # Chairman's Reasoning
        st.divider()
        st.markdown("## 🧠 Chairman's Analysis")
        with st.container():
            st.markdown(f"**{CHAIRMAN_NAME}** explains the decision:")
            st.markdown(reasoning if reasoning else chairman_output)
        
        # Winner highlight
        if ranked_responses:
            st.balloons()
            st.success(f"🎉 **Winner: {ranked_responses[0]['name']}**")

# Footer
st.divider()
st.caption("Built with Streamlit • Powered by OpenRouter Free Tier • 4 Council Models + 1 Chairman")

import os
import streamlit as st
from groq import Groq

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Research Hub", layout="wide")

# 2. INJECT A CUTE & SMOOTH PASTEL DESIGN
st.markdown("""
<style>
    /* Soft Warm Pastel Background */
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #f0fff4 50%, #f3e8ff 100%);
        color: #4a4a4a !important;
        font-family: 'Quicksand', 'Inter', sans-serif;
    }
    
    /* Smooth transition animations */
    * {
        transition: all 0.3s ease-in-out !important;
    }
    
    /* Cute Gradient Title */
    h1 {
        background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    /* Pastel Glass Text Inputs */
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #ffe3e3 !important;
        color: #4a4a4a !important;
        border-radius: 16px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 10px rgba(255, 117, 140, 0.05) !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #ff758c !important;
        box-shadow: 0 0 0 4px rgba(255, 117, 140, 0.15) !important;
    }
    
    /* Rounded, Friendly Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: rgba(255, 255, 255, 0.5);
        padding: 8px;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab"] {
        color: #8a8a8a !important;
        border-radius: 12px;
        padding: 8px 20px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff758c !important;
        color: #ffffff !important;
    }
    
    /* Cheerful Rounded Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #ff758c 0%, #ff7eb3 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 16px !important;
        padding: 14px 28px !important;
        font-weight: 700 !important;
        box-shadow: 0 6px 16px rgba(255, 117, 140, 0.3) !important;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 22px rgba(255, 117, 140, 0.43) !important;
    }
    
    /* Styled Containers for Output */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #e6fffa !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. App Header Layout
st.title("✨ My Cute AI Agent Hub")
st.caption("Your friendly, autonomous companion that handles research and writing for you!")
st.markdown("<br>", unsafe_allow_html=True)

# Create Cute Interface Tabs
tab_workspace, tab_about = st.tabs(["🚀 Launch Workspace", "📖 How It Works & About Page"])

# TAB 1: THE ABOUT & KEY GUIDE PAGE
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_guide, col_logic = st.columns(2, gap="large")
    
    with col_guide:
        st.subheader("🔑 How to Get Your Free Key")
        st.write("To use this app for free without creating a paid account, you just need a temporary access key:")
        st.markdown("1. Click this link to go to the **[Groq Developers Console](https://groq.com)**.")
        st.markdown("2. Sign in instantly using your standard **Google or GitHub account**.")
        st.markdown("3. In the left panel, click on **API Keys**, then hit the **Create API Key** button.")
        st.markdown("4. Copy the long string starting with `gsk_` and paste it right into our settings box below!")
        
        st.markdown("---")
        user_key = st.text_input("🌸 Paste your Groq API Key here:", type="password")

    with col_logic:
        st.subheader("🤖 How the Agentic AI Works")
        st.write("Unlike simple chat bots, this app deploys an autonomous multi-agent sequence behind the scenes:")
        st.markdown("🤝 **The Collaboration Loop**:")
        st.markdown("- **The Researcher Agent**: Evaluates your chosen topic, extracts deep insight variables, and organizes a rough factual index sheet.")
        st.markdown("- **The Content Writer Agent**: Receives those rough notes, applies creative text formatting rules, and refines everything into a gorgeous, readable report.")
        st.info("Because they collaborate step-by-step, the output is significantly more detailed than a simple standalone AI prompt!")

# TAB 2: MAIN WORKSPACE
with tab_workspace:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid split structure
    col_input, col_output = st.columns([4, 6], gap="large")
    
    with col_input:
        st.subheader("Your Task Settings")
        user_topic = st.text_input(
            "What should the agents work on today?", 
            placeholder="e.g., The cutest coffee shop designs in Tokyo",
        )
        
        with st.expander("🎈 Fun Adjustment Options"):
            agent_creativity = st.slider("Writing Playfulness (Temperature)", 0.0, 1.0, 0.7)
            
        st.markdown("<br>", unsafe_allow_html=True)
        button_clicked = st.button("Start the AI Magic! ✨", use_container_width=True)

    with col_output:
        st.subheader("Live Working Feed")
        
        if button_clicked:
            # Check for key from the other tab variable
            if 'user_key' not in locals() or not user_key:
                st.error("💝 Please hop over to the 'How It Works' tab and paste your API key first!")
            elif not user_topic:
                st.warning("🧁 Oops! Please write a topic vector parameter so the agents know what to look for.")
            else:
                with st.spinner("✨ Tiny agents are typing, thinking, and cleaning raw research files..."):
                    try:
                        client = Groq(api_key=user_key)
                        
                        # Step 1
                        research_prompt = f"You are a Senior Research Analyst. Break down key trends, pros, and cons regarding: {user_topic}. Provide a detailed bulleted summary of research findings."
                        research_response = client.chat.completions.create(
                            messages=[{"role": "user", "content": research_prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=0.2
                        )
                        research_notes = research_response.choices[0].message.content
                        
                        # Step 2
                        writer_prompt = f"You are a professional Content Strategist. Take these raw research findings and rewrite them into a compelling, 3-paragraph article:\n\n{research_notes}"
                        writer_response = client.chat.completions.create(
                            messages=[{"role": "user", "content": writer_prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=agent_creativity
                        )
                        final_article = writer_response.choices[0].message.content
                        
                        st.success("🎉 All tasks are perfectly completed!")
                        st.markdown("### 📝 Your Custom Generated Report:")
                        st.info(final_article)
                        
                    except Exception as e:
                        st.error(f"Oh no! An execution glitch happened: {e}")
        else:
            st.info("App is currently resting. Fill out a topic layout on the left panel to wake the agents up!")

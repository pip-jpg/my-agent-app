import os
import streamlit as st
from groq import Groq

# 1. Initialize High-End Workspace Configuration
st.set_page_config(page_title="AI Agent Intelligence Hub", layout="wide")

# 2. INJECT ULTRA-SMOOTH FINISHED DESIGN STYLE (Custom Color Palette & Soft Shadows)
st.markdown("""
<style>
    /* Global Background and Typography Setup */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f8fafc !important;
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    /* Global Smooth Animations for Interactive Assets */
    * {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }
    
    /* Premium Header Titles Styling */
    h1 {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.05em;
    }
    
    /* Make Input Text Fields Look Smoother & Glass-morphic */
    .stTextInput>div>div>input {
        background-color: rgba(30, 41, 59, 0.7) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #f8fafc !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    }
    .stTextInput>div>div>input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.2) !important;
    }
    
    /* Style Layout Interface Card Containers */
    div[data-testid="stForm"], div[data-testid="element-container"] .stElementContainer {
        border-radius: 16px;
    }
    
    /* Customize Action Buttons to Pop Nicely */
    .stButton>button {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(79, 70, 229, 0.4) !important;
        cursor: pointer;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.6) !important;
    }
    .stButton>button:active {
        transform: translateY(1px);
    }
    
    /* Soft Design Enhancements for Output Alert Boxes */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        border-radius: 14px !important;
        color: #f8fafc !important;
    }
    
    /* Clean Styling for Interface Layout Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(15, 23, 42, 0.4);
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8 !important;
        border-radius: 8px;
        padding: 8px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1e293b !important;
        color: #38bdf8 !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# 3. Structural Web App Layout Header
st.title("Intelligence Hub")
st.caption("Custom enterprise orchestration space managing autonomous agent processing streams.")
st.markdown("<br>", unsafe_allow_html=True)

# Create Interface Tabs
tab_workspace, tab_settings, tab_about = st.tabs(["🚀 Research Workspace", "🔑 API Configurations", "ℹ️ System Info"])

# WINDOW 1: API CONFIGURATIONS
with tab_settings:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Authentication Gateways")
    user_key = st.text_input("Enter your Groq API Key:", type="password", help="Authentication keys are processed securely.")
    st.markdown("[Generate your platform credentials here](https://groq.com)")

# WINDOW 2: SYSTEM INFO
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Orchestration Details")
    st.write("This workspace runs an automated sequence across specialized virtual operations personas:")
    st.markdown("- **Research Persona**: Evaluates context constraints and summarizes underlying technical structures.")
    st.markdown("- **Delivery Persona**: Compiles and refines syntax assets into ready documentation.")

# WINDOW 3: MAIN WORKSPACE
with tab_workspace:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Split layout: Left column inputs (45%), right column outputs (55%)
    col_input, col_output = st.columns([45, 55], gap="large")
    
    with col_input:
        st.subheader("Target Objectives")
        user_topic = st.text_input(
            "Define research vector parameters:", 
            placeholder="e.g., Cross-border blockchain payment infrastructure 2026",
        )
        
        with st.expander("🛠️ Advanced Execution Controls"):
            agent_creativity = st.slider("System Temperature Control", 0.0, 1.0, 0.7)
            
        st.markdown("<br>", unsafe_allow_html=True)
        button_clicked = st.button("Initialize Agent Sequence", use_container_width=True)

    with col_output:
        st.subheader("Live Processing Feed")
        
        if button_clicked:
            if not user_key:
                st.error("Authentication Failure: Please provide your Groq API key inside the Settings tab.")
            elif not user_topic:
                st.warning("Input Error: Missing target project parameter requirements.")
            else:
                with st.spinner("Processing agent sequence..."):
                    try:
                        client = Groq(api_key=user_key)
                        
                        # Agent Step 1 Execution
                        research_prompt = f"You are a Senior Research Analyst. Break down key trends, pros, and cons regarding: {user_topic}. Provide a detailed bulleted summary of research findings."
                        research_response = client.chat.completions.create(
                            messages=[{"role": "user", "content": research_prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=0.2
                        )
                        research_notes = research_response.choices[0].message.content
                        
                        # Agent Step 2 Execution
                        writer_prompt = f"You are a professional Content Strategist. Take these raw research findings and rewrite them into a compelling, 3-paragraph article:\n\n{research_notes}"
                        writer_response = client.chat.completions.create(
                            messages=[{"role": "user", "content": writer_prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=agent_creativity
                        )
                        final_article = writer_response.choices[0].message.content
                        
                        st.success("Sequence completed successfully.")
                        st.markdown("### Processed Artifact Output:")
                        st.info(final_article)
                        
                    except Exception as e:
                        st.error(f"Processing Exception: {e}")
        else:
            st.info("System idle. Define an execution vector target in the configuration workspace to begin.")

import os
import streamlit as st
from groq import Groq
# Swapped the search component for the robust AI-native Tavily library
from tavily import TavilyClient

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Research Hub", layout="wide")

# 2. INJECT CUTE & SMOOTH PASTEL DESIGN WITH REFRESH FIXES
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

# 3. INITIALIZE SESSION STATE MEMORY: Keeps outputs frozen on screen
if "agent_output" not in st.session_state:
    st.session_state.agent_output = ""
if "last_query" not in st.session_state:
    st.session_state.last_query = ""

# App Header Layout
st.title("✨ My Cute AI Agent Hub")
st.caption("Your friendly, autonomous companion with live web search and smart memory storage!")
st.markdown("<br>", unsafe_allow_html=True)

# Create Cute Interface Tabs
tab_workspace, tab_about = st.tabs(["🚀 Launch Workspace", "📖 How It Works & About Page"])

# TAB 1: ABOUT & INSTRUCTIONS PAGE
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    col_guide, col_logic = st.columns(2, gap="large")
    
    with col_guide:
        st.subheader("🔑 Access Gateways")
        st.write("To keep your execution loops completely free, paste your personal credentials below:")
        
        user_key = st.text_input("🌸 Paste your Groq API Key:", type="password")
        st.markdown("[Get a free Groq key here](https://groq.com)")
        
        # Added input field for the Tavily search key
        tavily_key = st.text_input("🌐 Paste your Tavily Search Key:", type="password")
        st.markdown("[Get a free Tavily Search key here](https://tavily.com)")

    with col_logic:
        st.subheader("🤖 How Live Search Works")
        st.write("Unlike simple chat bots, this app can step outside its training data to scrape live internet data:")
        st.markdown("- **Live Web Querying**: Formulates automated keyword vectors and harvests fresh search snippets via Tavily Search API.")
        st.markdown("- **Information Retention**: Utilizes dedicated memory clusters so your data never gets erased when clicking menus!")

# TAB 2: MAIN WORKSPACE
with tab_workspace:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Grid split structure
    col_input, col_output = st.columns(2, gap="large")
    
    with col_input:
        st.subheader("Your Task Settings")
        user_query = st.text_input(
            "What should the agents research for you right now?", 
            placeholder="e.g., What World Cup matches are lined up for today?",
        )
        
        with st.expander("🎈 Fun Adjustment Options"):
            agent_creativity = st.slider("Writing Playfulness (Temperature)", 0.0, 1.0, 0.7)
            
        st.markdown("<br>", unsafe_allow_html=True)
        button_clicked = st.button("Start the AI Magic! ✨", use_container_width=True)
        
        # Clear button to wipe the frozen state manually
        if st.button("Wipe Memory Clear 🧊", use_container_width=True):
            st.session_state.agent_output = ""
            st.session_state.last_query = ""
            st.rerun()

    with col_output:
        st.subheader("Live Working Feed")
        
        if button_clicked:
            if 'user_key' not in locals() or not user_key:
                st.error("💝 Please hop over to the 'How It Works' tab and paste your Groq API key first!")
            elif 'tavily_key' not in locals() or not tavily_key:
                st.error("💝 Please hop over to the 'How It Works' tab and paste your Tavily Search key first!")
            elif not user_query:
                st.warning("🧁 Oops! Please write a topic vector parameter so the agents know what to look for.")
            else:
                with st.spinner("✨ Tiny agents are typing, thinking, and cleaning raw research files..."):
                    try:
                        # STEP 1: Run Premium AI-Native Search via Tavily
                        tavily_client = TavilyClient(api_key=tavily_key)
                        response_data = tavily_client.search(query=user_query, max_results=3)
                        
                        search_results = []
                        for item in response_data.get('results', []):
                            search_results.append(f"Title: {item['title']}\nSnippet: {item['content']}\n")
                        
                        raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                        
                        # STEP 2: Pass internet context bundle straight into Groq
                        client = Groq(api_key=user_key)
                        
                        agent_prompt = f"""You are a professional real-time AI Agent. 
                        Answer the question clearly using the live internet search context provided below.
                        
                        User Question: {user_query}
                        
                        Live Web Search Context:
                        {raw_web_context}"""
                        
                        response = client.chat.completions.create(
                            messages=[{"role": "user", "content": agent_prompt}],
                            model="llama-3.3-70b-versatile",
                            temperature=agent_creativity
                        )
                        
                        # Save the generated text into memory session dictionary profiles
                        st.session_state.agent_output = response.choices[0].message.content
                        st.session_state.last_query = user_query
                        
                    except Exception as e:
                        st.error(f"Oh no! An execution glitch happened: {e}")
                        
        # RENDER PERSISTENT OUTPUT: Displays saved memory logs so they stay stuck on the screen
        if st.session_state.agent_output:
            st.success(f"🎉 Results for: '{st.session_state.last_query}'")
            st.markdown("### 📝 Your Custom Generated Report:")
            st.info(st.session_state.agent_output)
        else:
            st.info("App is currently resting. Fill out a topic layout on the left panel to wake the agents up!")

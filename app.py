import os
import streamlit as st
from groq import Groq
from tavily import TavilyClient

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Chat Hub", layout="wide")

# 2. INJECT CUTE & SMOOTH PASTEL DESIGN FOR CHAT & TUTORIALS
st.markdown("""
<style>
    /* Soft Warm Pastel Background */
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #f0fff4 50%, #f3e8ff 100%);
        color: #4a4a4a !important;
        font-family: 'Quicksand', 'Inter', sans-serif;
    }
    
    * { transition: all 0.2s ease-in-out !important; }
    
    /* Cute Gradient Title */
    h1 {
        background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    /* Style Chat Input Bar at Bottom */
    .stChatInput {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(255, 117, 140, 0.1) !important;
    }
    
    /* Soft Rounded Cards for Individual Message Bubbles */
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 2px solid #ffe3e3 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

    /* Rounded, Friendly Navigation Tabs */
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

    /* Cute Instruction Cards */
    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #ffe3e3 !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZE INTERACTIVE CHAT HISTORY STORAGE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 I am your live agent companion. Ask me anything about current events, sports lineups, or general knowledge!"}]

st.title("✨ Bunny Chat Hub")
st.caption("A friendly, autonomous agent chat experience fueled by live search engines.")
st.markdown("<br>", unsafe_allow_html=True)

# Create Navigation Layout Tabs (Chat and Guide are side-by-side)
tab_chat, tab_about = st.tabs(["💬 Chat Messenger", "📖 How It Works & Key Tutorial"])

# TAB 1: ABOUT & STEP-BY-STEP KEY TUTORIAL PAGE
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    col_guide, col_logic = st.columns(2, gap="large")
    
    with col_guide:
        st.subheader("🔑 Step-by-Step Key Setup")
        st.write("To keep your execution loops completely free, paste your personal credentials below:")
        
        st.markdown("### **1. Get Your Free AI Brain Key (Groq)**")
        st.markdown("- Go to the **[Groq Developers Console](https://groq.com)**.")
        st.markdown("- Sign in instantly using your standard **Google or GitHub account**.")
        st.markdown("- Click **API Keys** on the left menu, hit **Create API Key**, and copy the string.")
        user_key = st.text_input("🌸 Paste your Groq API Key here:", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### **2. Get Your Free Live Search Key (Tavily)**")
        st.markdown("- Go to the **[Tavily AI Portal](https://tavily.com)**.")
        st.markdown("- Create a free account (includes 1,000 free web searches per month!).")
        st.markdown("- Copy the main API Key from your dashboard page.")
        tavily_key = st.text_input("🌐 Paste your Tavily Search Key here:", type="password")
        
        st.markdown("---")
        if st.button("Clear Conversation History 🧊", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 Chat memory cleared. What should we look into next?"}]
            st.rerun()

    with col_logic:
        st.subheader("🤖 How Your Agentic AI Operates")
        st.write("This app does not work like a basic, simple chatbot. It deploys an automated operational sequence across specialized virtual personas:")
        
        st.markdown("### 🕸️ **Phase 1: Real-Time Scraping**")
        st.markdown("The app catches your question and instantly builds an optimized keyword array. It uses **Tavily Search** to crawl active live websites, pulling down fresh data blocks before the AI even reads your message.")
        
        st.markdown("### 🧠 **Phase 2: Contextual Synthesis**")
        st.markdown("The scraped webpage snippets are packaged together with your chat conversation log and fed directly into the flagship **Llama 3.3 Versatile engine** hosted on Groq's high-speed servers.")
        
        st.markdown("### 📝 **Phase 3: Final Response Delivery**")
        st.markdown("The agent analyzes the web context, isolates current information profiles (ignoring its old training cuts), and formats the final interactive bubble delivery smoothly onto your screen.")
        st.info("Because it loops web data straight into the prompt layer, it knows exactly what happens in the world in real-time!")

# TAB 2: LIVE CHAT INTERFACE WINDOW
with tab_chat:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render all historic messages out of memory cells
    for msg in st.session_state.messages:
        avatar = "🌸" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
    # Listen for fresh message typing loops
    if user_input := st.chat_input("Ask a question... (e.g., What World Cup matches are lined up for today?)"):
        
        # Instantly append human input bubble onto screen layout map
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Verify both credentials exist before running cloud scripts
        if 'user_key' not in locals() or 'tavily_key' not in locals() or not user_key or not tavily_key:
            with st.chat_message("assistant", avatar="🌸"):
                st.error("💝 Please jump over to the 'How It Works & Key Tutorial' tab and enter BOTH keys first so I can unlock the AI brain!")
        else:
            # Wake up assistant response loading cells
            with st.chat_message("assistant", avatar="🌸"):
                with st.spinner("Searching the live web and thinking..."):
                    try:
                        # Step 1: Run Live Web Scraper via Tavily
                        tavily_client = TavilyClient(api_key=tavily_key)
                        response_data = tavily_client.search(query=user_input, max_results=3)
                        
                        search_results = []
                        for item in response_data.get('results', []):
                            search_results.append(f"Title: {item['title']}\nSnippet: {item['content']}\n")
                        raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                        
                        # Step 2: Assemble System Prompt and Dispatch to Groq Client
                        client = Groq(api_key=user_key)
                        agent_prompt = f"You are a professional real-time AI Agent with access to live internet metrics. Answer the user query clearly using the recent web context provided below.\n\nLive Web Search Context:\n{raw_web_context}"
                        
                        # Package memory parameters so it tracks recent back-and-forth chat strings
                        payload_messages = [{"role": "system", "content": agent_prompt}]
                        for m in st.session_state.messages[-5:]:  # Keep last 5 messages for conversation flow
                            payload_messages.append({"role": m["role"], "content": m["content"]})
                            
                        response = client.chat.completions.create(
                            messages=payload_messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.7
                        )
                        
                        agent_reply = response.choices[0].message.content
                        
                        # Render agent response bubble on-screen and commit to structural history array
                        st.markdown(agent_reply)
                        st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                        
                    except Exception as e:
                        st.error(f"Execution Error Encountered: {e}")

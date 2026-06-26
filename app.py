import os
import streamlit as st
import urllib.parse
from groq import Groq
from tavily import TavilyClient

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Magic Hub", layout="wide")

# 2. INJECT THE CUTE PASTEL LOOK WITH CHAT DESIGN
st.markdown("""
<style>
    /* Soft Warm Pastel Background */
    .stApp {
        background: linear-gradient(135deg, #fff5f5 0%, #f0fff4 50%, #f3e8ff 100%);
        color: #4a4a4a !important;
        font-family: 'Quicksand', 'Inter', sans-serif;
    }
    
    * { transition: all 0.2s ease-in-out !important; }
    
    h1 {
        background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        letter-spacing: -0.02em;
    }
    
    .stChatInput {
        border-radius: 20px !important;
        box-shadow: 0 4px 15px rgba(255, 117, 140, 0.1) !important;
    }
    
    div[data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 2px solid #ffe3e3 !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin-bottom: 10px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important;
    }

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

    .stAlert {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid #ffe3e3 !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.03) !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZE INTERACTIVE CHAT STORAGE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! 🌸 I can chat, search the live web, or draw pictures for you! To see a picture, just type something like: `/image a cute white bunny wearing a crown`"}]

st.title("✨ Bunny Magic Hub")
st.caption("A multi-agent messaging hub equipped with live search routers and free art engines.")
st.markdown("<br>", unsafe_allow_html=True)

tab_chat, tab_about = st.tabs(["💬 Chat & Art Messenger", "📖 Tutorial Configurations"])

# STEP-BY-STEP KEY TUTORIAL GUIDE PORTAL
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    col_guide, col_logic = st.columns(2, gap="large")
    
    with col_guide:
        st.subheader("🔑 Step-by-Step Key Setup Guide")
        st.write("To use this app completely for free, paste your personal credentials below:")
        
        st.markdown("### **1. Get Your Free AI Brain Key (Groq)**")
        st.markdown("- Click to open the **[Groq Developers Console](https://groq.com)**.")
        st.markdown("- Sign in instantly using your standard **Google or GitHub account**.")
        st.markdown("- Click **API Keys** on the left menu, hit **Create API Key**, and copy the string.")
        user_key = st.text_input("🌸 Paste your Groq API Key here:", type="password", key="groq_key_input")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### **2. Get Your Free Live Search Key (Tavily)**")
        st.markdown("- Click to open the **[Tavily AI Portal](https://tavily.com)**.")
        st.markdown("- Create a free developer account (includes 1,000 free web searches per month!).")
        st.markdown("- Copy the main API Key displayed directly on your homepage dashboard.")
        tavily_key = st.text_input("🌐 Paste your Tavily Search Key here:", type="password", key="tavily_key_input")
        
        st.markdown("---")
        if st.button("Wipe Chat Memory 🧊", use_container_width=True):
            st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 Memory cleared. What should we look into next?"}]
            st.rerun()

    with col_logic:
        st.subheader("🎨 App Engine Guide")
        st.write("This workspace runs distinct digital processing channels depending on your query type:")
        st.markdown("### **🤖 The Real-Time Chat Engine**")
        st.markdown("When asking general or time-sensitive questions, the system calls your **Tavily Key** to scrape live online articles, matching findings against **Groq's Llama 3.3 model** to give you current answers.")
        st.markdown("### **✨ The Free Art Generator Engine**")
        st.markdown("When you pass the keyword `/image`, the app drops the search stack entirely and streams text arrays directly through open-source rendering grids to output high-resolution graphics completely for free!")

# INTERACTIVE STREAM CHAT DISPLAY
with tab_chat:
    st.markdown("<br>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        avatar = "🌸" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                # FIX: Explicitly passing use_container_width=True natively displays HTML images safely
                st.image(msg["content"]["url"], caption=msg["content"]["prompt"], use_container_width=True)
            else:
                st.markdown(msg["content"])
            
    if user_input := st.chat_input("Ask a question, or type /image to generate art..."):
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # INTERACTION branch 1: The user wants an IMAGE
        if user_input.strip().lower().startswith("/image"):
            image_prompt = user_input.replace("/image", "").strip()
            
            if not image_prompt:
                with st.chat_message("assistant", avatar="🌸"):
                    st.warning("🧁 Please provide a description prompt after the word /image!")
            else:
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Generating art canvas..."):
                        encoded_prompt = urllib.parse.quote(image_prompt)
                        # Updated the generation endpoint string configuration to render flawlessly 
                        free_image_url = f"https://pollinations.ai{encoded_prompt}?width=800&height=800&seed=42&nofeed=true"
                        
                        st.image(free_image_url, caption=image_prompt, use_container_width=True)
                        st.session_state.messages.append({"role": "assistant", "content": {"type": "image", "url": free_image_url, "prompt": image_prompt}})
        
        # INTERACTION branch 2: Standard Live Text Answer Questions Loop
        else:
            # Safe checking from inputs
            g_key = st.session_state.get("groq_key_input", "")
            t_key = st.session_state.get("tavily_key_input", "")
            
            if not g_key or not t_key:
                with st.chat_message("assistant", avatar="🌸"):
                    st.error("💝 Please jump over to the 'Tutorial Configurations' tab and enter both keys first!")
            else:
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Searching live data feeds..."):
                        try:
                            tavily_client = TavilyClient(api_key=t_key)
                            response_data = tavily_client.search(query=user_input, max_results=3)
                            
                            search_results = []
                            for item in response_data.get('results', []):
                                search_results.append(f"Title: {item['title']}\nSnippet: {item['content']}\n")
                            raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                            
                            client = Groq(api_key=g_key)
                            agent_prompt = f"You are a professional real-time AI Agent with access to live internet metrics. Answer the user query clearly using the recent web context provided below.\n\nLive Web Search Context:\n{raw_web_context}"
                            
                            payload_messages = [{"role": "system", "content": agent_prompt}]
                            for m in st.session_state.messages[-5:]:
                                if isinstance(m["content"], str):
                                    payload_messages.append({"role": m["role"], "content": m["content"]})
                                
                            response = client.chat.completions.create(
                                messages=payload_messages,
                                model="llama-3.3-70b-versatile",
                                temperature=0.7
                            )
                            
                            agent_reply = response.choices.message.content
                            st.markdown(agent_reply)
                            st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                            
                        except Exception as e:
                            st.error(f"Execution Error Encountered: {e}")

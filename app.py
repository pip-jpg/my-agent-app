import os
import streamlit as st
import urllib.parse
from groq import Groq
from tavily import TavilyClient

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Magic Hub", layout="wide")

# 2. INJECT THE CUTE PASTEL LOOK WITH IMAGE DISPLAY BOXES
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
    }
    .stTabs [data-baseweb="tab"] {
        color: #8a8a8a !important;
        border-radius: 12px;
        padding: 8px 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff758c !important;
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZE INTERACTIVE CHAT STORAGE
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! 🌸 I can chat, search the web, or draw pictures for you! To see a picture, just type something like: `/image a cute white bunny wearing a crown`"}]

st.title("✨ Bunny Magic Hub")
st.caption("A multi-agent messaging hub equipped with live search routers and free art engines.")
st.markdown("<br>", unsafe_allow_html=True)

tab_chat, tab_about = st.tabs(["💬 Chat & Art Messenger", "📖 Tutorial Configurations"])

# CREDENTIAL KEYS GATEWAY PORTAL
with tab_about:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Platform Credentials")
    user_key = st.text_input("🌸 Paste your Groq API Key:", type="password")
    tavily_key = st.text_input("🌐 Paste your Tavily Search Key:", type="password")
    
    st.markdown("---")
    st.subheader("🎨 How Image Generation Works")
    st.write("When you type the special command keyword `/image`, the application isolates your descriptor parameters and calls an open-source image generation engine to render a visual layout for free!")

    if st.button("Wipe Chat Memory 🧊", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 Memory cleared. What should we look into next?"}]
        st.rerun()

# INTERACTIVE STREAM CHAT DISPLAY
with tab_chat:
    st.markdown("<br>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        avatar = "🌸" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            # Check if message is a saved image link dictionary block
            if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                st.image(msg["content"]["url"], caption=msg["content"]["prompt"], use_container_width=True)
            else:
                st.markdown(msg["content"])
            
    if user_input := st.chat_input("Ask a question, or type /image to generate art..."):
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # INTERACTION branch 1: The user wants an IMAGE
        if user_input.strip().lower().startswith("/image"):
            # Strip away the command keyword to fetch the raw design description string
            image_prompt = user_input.replace("/image", "").strip()
            
            if not image_prompt:
                with st.chat_message("assistant", avatar="🌸"):
                    st.warning("🧁 Please provide a description prompt after the word /image!")
            else:
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Generating art canvas..."):
                        # Safe URL encode translation formatting
                        encoded_prompt = urllib.parse.quote(image_prompt)
                        # Connect directly to free, open-source stable diffusion router API
                        free_image_url = f"https://pollinations.ai{encoded_prompt}?width=1024&height=1024&nologo=true"
                        
                        # Render live onto the screen layout panel
                        st.image(free_image_url, caption=image_prompt, use_container_width=True)
                        # Push dictionary indicator object straight to historical message arrays
                        st.session_state.messages.append({"role": "assistant", "content": {"type": "image", "url": free_image_url, "prompt": image_prompt}})
        
        # INTERACTION branch 2: Standard Live Text Answer Questions Loop
        else:
            if not user_key or not tavily_key:
                with st.chat_message("assistant", avatar="🌸"):
                    st.error("💝 Please jump over to the 'Tutorial Configurations' tab and enter both keys first!")
            else:
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Searching live data feeds..."):
                        try:
                            tavily_client = TavilyClient(api_key=tavily_key)
                            response_data = tavily_client.search(query=user_input, max_results=3)
                            
                            search_results = []
                            for item in response_data.get('results', []):
                                search_results.append(f"Title: {item['title']}\nSnippet: {item['content']}\n")
                            raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                            
                            client = Groq(api_key=user_key)
                            agent_prompt = f"You are a professional real-time AI Agent with access to live internet metrics. Answer the user query clearly using the recent web context provided below.\n\nLive Web Search Context:\n{raw_web_context}"
                            
                            payload_messages = [{"role": "system", "content": agent_prompt}]
                            for m in st.session_state.messages[-5:]:
                                if isinstance(m["content"], str): # Filter text blocks only
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

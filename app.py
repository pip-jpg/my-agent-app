import os
import streamlit as st
from groq import Groq
from tavily import TavilyClient

# 1. Initialize Page Config
st.set_page_config(page_title="Bunny Chat Hub", layout="wide")

# 2. INJECT CUTE & SMOOTH PASTEL DESIGN FOR CHAT INTERFACES
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
</style>
""", unsafe_allow_html=True)

# 3. INITIALIZE INTERACTIVE CHAT HISTORY STORAGE
if "messages" not in st.session_state:
    # Seed conversational array structure
    st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 I am your live agent companion. Ask me anything about current events or general knowledge!"}]

st.title("✨ Bunny Chat Hub")
st.caption("A friendly, autonomous agent chat experience fueled by live search engines.")
st.markdown("<br>", unsafe_allow_html=True)

# Create Navigation Layout Tabs
tab_chat, tab_config = st.tabs(["💬 Chat Messenger", "🔑 API Gateways"])

# CONFIGURATION CONTROL PORTAL
with tab_config:
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Platform Credentials")
    user_key = st.text_input("🌸 Paste your Groq API Key:", type="password")
    st.markdown("[Get a free Groq key here](https://groq.com)")
    
    tavily_key = st.text_input("🌐 Paste your Tavily Search Key:", type="password")
    st.markdown("[Get a free Tavily Search key here](https://tavily.com)")
    
    if st.button("Wipe Chat Memory 🧊", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": "Hi there! 🌸 Memory cleared. What should we look into next?"}]
        st.rerun()

# LIVE CHAT INTERFACE WINDOW
with tab_chat:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 4. RENDER PREVIOUS CONVERSATION STREAM FROM SYSTEM MEMORY
    for msg in st.session_state.messages:
        avatar = "🌸" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
            
    # 5. LISTEN FOR NEW CHAT INPUNT FROM USER
    if user_input := st.chat_input("Ask a question... (e.g., What WC matches are lined up for today?)"):
        
        # Instantly append human input bubble onto screen layout map
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Verify credential statuses before hitting cloud targets
        if not user_key or not tavily_key:
            with st.chat_message("assistant", avatar="🌸"):
                st.error("💝 Please jump over to the 'API Gateways' configuration tab and insert both authorization keys first!")
        else:
            # Wake up assistant response loading cells
            with st.chat_message("assistant", avatar="🌸"):
                with st.spinner("Searching and parsing live metrics..."):
                    try:
                        # Step 1: Run Live Web Scraper
                        tavily_client = TavilyClient(api_key=tavily_key)
                        response_data = tavily_client.search(query=user_input, max_results=3)
                        
                        search_results = []
                        for item in response_data.get('results', []):
                            search_results.append(f"Title: {item['title']}\nSnippet: {item['content']}\n")
                        raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                        
                        # Step 2: Assemble System Prompt and Dispatch to Groq
                        client = Groq(api_key=user_key)
                        agent_prompt = f"""You are a professional real-time AI Agent with access to live internet metrics.
                        Answer the user query clearly using the recent web context provided below.
                        
                        Live Web Search Context:
                        {raw_web_context}"""
                        
                        # Pack historical memory so the bot can remember past message texts
                        payload_messages = [{"role": "system", "content": agent_prompt}]
                        for m in st.session_state.messages[-5:]: # Keep last 5 messages for context
                            payload_messages.append({"role": m["role"], "content": m["content"]})
                            
                        response = client.chat.completions.create(
                            messages=payload_messages,
                            model="llama-3.3-70b-versatile",
                            temperature=0.7
                        )
                        
                        agent_reply = response.choices[0].message.content
                        
                        # Render agent bubble text on-screen and commit to history array
                        st.markdown(agent_reply)
                        st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                        
                    except Exception as e:
                        st.error(f"Execution Error Encountered: {e}")

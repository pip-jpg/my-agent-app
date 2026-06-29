import os
import streamlit as st
import urllib.parse
from groq import Groq
from tavily import TavilyClient
from supabase import create_client, Client

# 1. Initialize Supabase Cloud Database Connection
SUPABASE_URL = "https://ryxozerjvgbxszkemama.supabase.co"
SUPABASE_KEY = "sb_publishable_o1RU6g-yg8K2kkmZwGizRg_7H-XDe7-E"  # Keep your long anon key pasted here

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Page Configuration & Cute Styling
st.set_page_config(page_title="Bunny Magic Hub", layout="wide")
st.markdown("""
<style>
    .stApp { background: linear-gradient(135deg, #fff5f5 0%, #f0fff4 50%, #f3e8ff 100%); color: #4a4a4a !important; font-family: 'Quicksand', sans-serif; }
    * { transition: all 0.2s ease-in-out !important; }
    h1 { background: linear-gradient(90deg, #ff758c 0%, #ff7eb3 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800 !important; }
    .stChatInput { border-radius: 20px !important; box-shadow: 0 4px 15px rgba(255, 117, 140, 0.1) !important; }
    div[data-testid="stChatMessage"] { background-color: rgba(255, 255, 255, 0.7) !important; border: 2px solid #ffe3e3 !important; border-radius: 20px !important; padding: 15px !important; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02) !important; }
    .stTabs [data-baseweb="tab-list"] { gap: 12px; background-color: rgba(255, 255, 255, 0.5); padding: 8px; border-radius: 16px; }
    .stTabs [aria-selected="true"] { background-color: #ff758c !important; color: #ffffff !important; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# Initialize Session Account Tracking States
if "user_session" not in st.session_state:
    st.session_state.user_session = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! 🌸 Log in on the account tab to link your saved keys, then chat with me here!"}]

st.title("✨ Bunny Magic Hub")
st.caption("A protected messaging hub equipped with permanent database account profiling.")
st.markdown("<br>", unsafe_allow_html=True)

tab_chat, tab_account = st.tabs(["💬 Secure Chat Space", "🔒 User Registration & Logins"])

# TAB 1: THE LOGIN AND USER KEY PERMANENT STORAGE GATEWAY
with tab_account:
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.session_state.user_session is None:
        col_login, col_reg = st.columns(2, gap="large")
        
        with col_login:
            st.subheader("Sign In")
            login_email = st.text_input("Email address:", key="login_em")
            login_pass = st.text_input("Password:", type="password", key="login_pw")
            if st.button("Log into Account", use_container_width=True):
                try:
                    res = supabase.auth.sign_in_with_password({"email": login_email, "password": login_pass})
                    st.session_state.user_session = res.user
                    st.success("🎉 Logged in successfully! Refreshing details...")
                    st.rerun()
                except Exception as e:
                    st.error(f"Sign in failed: {e}")
                    
        with col_reg:
            st.subheader("Create Free Account")
            reg_email = st.text_input("Email address:", key="reg_em")
            reg_pass = st.text_input("Choose Password (min 6 chars):", type="password", key="reg_pw")
            if st.button("Register New User", use_container_width=True):
                try:
                    res = supabase.auth.sign_up({"email": reg_email, "password": reg_pass})
                    st.success("✉️ Account initialized! Check your email inbox to click the confirmation link before signing in.")
                except Exception as e:
                    st.error(f"Registration failed: {e}")
    else:
        # User is logged in!
        st.subheader(f"👋 Welcome back, {st.session_state.user_session.email}!")
        
        # CRITICAL FIX: Wrapped inside a try block to shield against RLS API database crashes
        saved_groq = ""
        saved_tavily = ""
        try:
            db_profile = supabase.table("user_profiles").select("*").eq("id", st.session_state.user_session.id).execute()
            if db_profile.data and len(db_profile.data) > 0:
                saved_groq = db_profile.data[0].get("groq_key", "")
                saved_tavily = db_profile.data[0].get("tavily_key", "")
        except Exception:
            # Safely fallback to blank fields if database rows are inaccessible
            pass
        
        st.markdown("### 💾 Your Stored API Keys")
        new_groq = st.text_input("Saved Groq Key Profile:", value=saved_groq, type="password")
        new_tavily = st.text_input("Saved Tavily Key Profile:", value=saved_tavily, type="password")
        
        if st.button("Save Keys and Sync to Database Lock", use_container_width=True):
            try:
                # Upsert profile into the secure database table
                supabase.table("user_profiles").upsert({
                    "id": st.session_state.user_session.id,
                    "groq_key": new_groq,
                    "tavily_key": new_tavily
                }).execute()
                st.success("🌸 Keys safely saved to your cloud profile! You can now use the chat freely.")
                st.rerun()
            except Exception as e:
                st.error(f"Database save error: {e}")
                
        if st.button("Log Out of Account", type="secondary"):
            supabase.auth.sign_out()
            st.session_state.user_session = None
            st.rerun()

# TAB 2: CHAT ENGINE RUNNING SCRIPT USING DATABASE SAVED PROFILE KEYS
with tab_chat:
    st.markdown("<br>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        avatar = "🌸" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=avatar):
            if isinstance(msg["content"], dict) and msg["content"].get("type") == "image":
                st.image(msg["content"]["url"], caption=msg["content"]["prompt"], use_container_width=True)
            else:
                st.markdown(msg["content"])
                
    if user_input := st.chat_input("Message your agent space..."):
        with st.chat_message("user", avatar="👤"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        if st.session_state.user_session is None:
            with st.chat_message("assistant", avatar="🌸"):
                st.error("💝 Security Alert: Please jump over to the Registration tab and log in first to access the AI worker!")
        else:
            # CRITICAL FIX: Wrapped inside a try block to shield chat routing from crashing
            g_key = ""
            t_key = ""
            try:
                db_profile = supabase.table("user_profiles").select("*").eq("id", st.session_state.user_session.id).execute()
                if db_profile.data and len(db_profile.data) > 0:
                    g_key = db_profile.data[0].get("groq_key", "")
                    t_key = db_profile.data[0].get("tavily_key", "")
            except Exception:
                pass
            
            if not g_key or not t_key:
                with st.chat_message("assistant", avatar="🌸"):
                    st.warning("🧁 Account found, but your key vault is blank! Please add both keys inside the profile tab.")
            else:
                with st.chat_message("assistant", avatar="🌸"):
                    with st.spinner("Processing secure execution clusters..."):
                        try:
                            if user_input.strip().lower().startswith("/image"):
                                image_prompt = user_input.replace("/image", "").strip()
                                encoded_prompt = urllib.parse.quote(image_prompt)
                                free_image_url = f"https://pollinations.ai{encoded_prompt}?width=800&height=800&seed=42&nofeed=true"
                                st.image(free_image_url, caption=image_prompt, use_container_width=True)
                                st.session_state.messages.append({"role": "assistant", "content": {"type": "image", "url": free_image_url, "prompt": image_prompt}})
                            else:
                                tavily_client = TavilyClient(api_key=t_key)
                                response_data = tavily_client.search(query=user_input, max_results=3)
                                search_results = [f"Title: {item['title']}\nSnippet: {item['content']}\n" for item in response_data.get('results', [])]
                                raw_web_context = "\n---\n".join(search_results) if search_results else "No live results found."
                                
                                client = Groq(api_key=g_key)
                                agent_prompt = f"You are a professional real-time AI Agent. Answer using this live context:\n\n{raw_web_context}"
                                payload_messages = [{"role": "system", "content": agent_prompt}]
                                for m in st.session_state.messages[-5:]:
                                    if isinstance(m["content"], str):
                                        payload_messages.append({"role": m["role"], "content": m["content"]})
                                        
                                response = client.chat.completions.create(messages=payload_messages, model="llama-3.3-70b-versatile", temperature=0.7)
                                agent_reply = response.choices.message.content
                                st.markdown(agent_reply)
                                st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                        except Exception as e:
                            st.error(f"Glitch encountered: {e}")

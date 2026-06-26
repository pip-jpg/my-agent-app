import streamlit as st
from groq import Groq

# 1. Setup the Web App Interface
st.set_page_config(page_title="My First AI Agent App", layout="wide")
st.title("My Custom Agentic AI App")
st.sidebar.header("API Settings")
user_key = st.sidebar.text_input("Enter your Groq API Key:", type="password")
st.sidebar.markdown("[Get a free Groq API key here](https://console.groq.com/)")

# 2. Main App Inputs
user_topic = st.text_input("Topic to research", placeholder="e.g., Future of AI")
button_clicked = st.button("Launch Agent Loop")

# 3. Native Agent Logic (Bypasses LiteLLM/CrewAI header bugs completely)
if button_clicked:
    if not user_key:
        st.error("Please enter your Groq API key in the sidebar!")
    elif not user_topic:
        st.warning("Please enter a topic.")
    else:
        with st.spinner("Agents are executing tasks..."):
            try:
                # Initialize the official Groq client directly
                client = Groq(api_key=user_key)
                
                # Agent 1: The Researcher Persona Prompt
                research_prompt = f"You are a Senior Research Analyst. Break down key trends, pros, and cons regarding: {user_topic}. Provide a detailed bulleted summary of research findings."
                
                # FIX: Swapped out decommissioned model name for the updated flagship versatile version
                research_response = client.chat.completions.create(
                    messages=[{"role": "user", "content": research_prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.2
                )
                research_notes = research_response.choices[0].message.content
                
                # Agent 2: The Writer Persona Prompt consuming Researcher notes
                writer_prompt = f"You are a professional Content Strategist. Take these raw research findings and rewrite them into a compelling, 3-paragraph article:\n\n{research_notes}"
                
                # FIX: Swapped out decommissioned model name for the updated flagship versatile version
                writer_response = client.chat.completions.create(
                    messages=[{"role": "user", "content": writer_prompt}],
                    model="llama-3.3-70b-versatile",
                    temperature=0.7
                )
                final_article = writer_response.choices[0].message.content
                
                # Display Results
                st.success("Task Completed!")
                st.markdown("### Final Article Output:")
                st.write(final_article)
                
            except Exception as e:
                st.error(f"Error: {e}")


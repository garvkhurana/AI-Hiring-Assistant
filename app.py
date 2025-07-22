import streamlit as st
from chatbot.context_handler import ChatContext
from chatbot.prompts import generate_greeting, end_conversation_check
import os

st.set_page_config(page_title="TalentScout AI", layout="centered")


st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #ece9e6, #ffffff);
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
        margin: 5px 0;
    }
    .stChatMessage.user {
        background-color: #D1C4E9;
        color: #000;
    }
    .stChatMessage.assistant {
        background-color: #B2EBF2;
        color: #000;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center; color:#673AB7;'>🌍 TalentScout – AI Hiring Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Multilingual | Smart | Context-Aware</p>", unsafe_allow_html=True)

if "chat" not in st.session_state:
    st.session_state.chat = None

if "started" not in st.session_state:
    st.session_state.started = False

if "reset" not in st.session_state:
    st.session_state.reset = False

with st.sidebar:
    st.header("🔐 API Key")
    api_key = st.text_input("Enter your Groq API key", type="password")

    if api_key:
        os.environ["GROQ_API_KEY"] = api_key

        if st.button("🔄 Restart Chat"):
            st.session_state.chat = ChatContext()
            st.session_state.started = False
            st.experimental_rerun()

        if st.session_state.chat:
            st.markdown("---")
            st.subheader("📋 Candidate Details")
            for k, v in st.session_state.chat.data.items():
                st.markdown(f"{'✅' if v else '🕘'} **{k.replace('_',' ').title()}:** {v or '*pending...*'}")
    else:
        st.warning("🔑 Please enter your Groq API key to start.")
        st.stop()

if not st.session_state.chat:
    st.session_state.chat = ChatContext()

if not st.session_state.started:
    st.session_state.started = True
    st.chat_message("assistant").markdown(generate_greeting())
    name_prompt = st.session_state.chat.start()
    st.chat_message("assistant").markdown(name_prompt)

user_input = st.chat_input("Type your response...")

if user_input:
    st.chat_message("user").markdown(user_input)

    if end_conversation_check(user_input):
        st.session_state.chat.end()
        st.chat_message("assistant").markdown("✅ Thank you! We'll get back to you soon.")
    else:
        bot_reply = st.session_state.chat.get_bot_response(user_input)
        st.chat_message("assistant").markdown(bot_reply)

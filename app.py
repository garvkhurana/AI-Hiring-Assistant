import streamlit as st
from chatbot.context_handler import ChatContext
from chatbot.prompts import generate_greeting
import os

st.set_page_config(page_title="TalentScout - AI Hiring Assistant")

st.title(" TalentScout - AI Hiring Assistant")


st.sidebar.title("🔐 Groq API Key & Context")

if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""

st.session_state.groq_key = st.sidebar.text_input(
    "Enter your Groq API Key", type="password", value=st.session_state.groq_key
)

os.environ["GROQ_API_KEY"] = st.session_state.groq_key


if "chat" not in st.session_state or st.sidebar.button("🔄 Start New Session"):
    st.session_state.chat = ChatContext()
    st.session_state.chat.started = True
    st.chat_message("assistant").markdown(generate_greeting())
    first_prompt = st.session_state.chat.start()
    st.chat_message("assistant").markdown(first_prompt)


st.sidebar.subheader(" Collected Info")
for key, val in st.session_state.chat.data.items():
    st.sidebar.text(f"{key.capitalize()}): {val if val else 'Not provided'}")


user_input = st.chat_input("Enter your response here...")

if user_input:
    st.chat_message("user").markdown(user_input)
    response = st.session_state.chat.get_bot_response(user_input)
    st.chat_message("assistant").markdown(response)


if st.session_state.chat.ready_for_questions:
    if st.button("👉 Go Ahead to Questions"):
        response = st.session_state.chat.get_bot_response("go ahead")
        st.chat_message("assistant").markdown(response)



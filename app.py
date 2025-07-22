import streamlit as st
from chatbot.context_handler import ChatContext
from chatbot.prompts import generate_greeting
import os

st.set_page_config(page_title="TalentScout - AI Hiring Assistant")

st.title(" TalentScout - AI Hiring Assistant")

st.sidebar.title("🔐Groq API Key & Context")


if "groq_key" not in st.session_state:
    st.session_state.groq_key = ""


st.session_state.groq_key = st.sidebar.text_input(
    "Enter your Groq API Key", type="password", value=st.session_state.groq_key
)

os.environ["GROQ_API_KEY"] = st.session_state.groq_key


if "chat" not in st.session_state or st.sidebar.button("🔄 Start New Session"):
    if st.session_state.groq_key:  
        st.session_state.chat = ChatContext()
        st.session_state.chat.started = True
        st.session_state.messages = [] 
        
      
        greeting = generate_greeting()
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        
        first_prompt = st.session_state.chat.start()
        st.session_state.messages.append({"role": "assistant", "content": first_prompt})
    else:
        st.error("Please enter your Groq API Key to start.")


if "chat" in st.session_state and "messages" in st.session_state:
    
    st.sidebar.subheader("📋 Collected Info")
    for key, val in st.session_state.chat.data.items():
        display_key = key.replace('_', ' ').title()
        st.sidebar.text(f"{display_key}: {val if val else 'Not provided'}")
    
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    
    user_input = st.chat_input("Enter your response here...")
    
    if user_input:
        
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        
        try:
            response = st.session_state.chat.get_bot_response(user_input)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response)
        except Exception as e:
            error_msg = f"Error: {str(e)}. Please check your API key."
            st.error(error_msg)
    
   
    if hasattr(st.session_state.chat, 'ready_for_questions') and st.session_state.chat.ready_for_questions:
        if st.button("👉 Proceed to Technical Questions"):
            try:
                response = st.session_state.chat.get_bot_response("go ahead")
                st.session_state.messages.append({"role": "assistant", "content": response})
                with st.chat_message("assistant"):
                    st.markdown(response)
                st.rerun()  
            except Exception as e:
                st.error(f"Error generating questions: {str(e)}")
else:
    st.info("Please enter your Groq API Key in the sidebar to get started.")
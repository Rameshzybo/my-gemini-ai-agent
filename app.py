import os
import streamlit as st
from google import genai

st.title("🤖 My Gemini AI Agent")

api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

@st.cache_resource
def get_client():
    return genai.Client(api_key=api_key)

client = get_client()

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-3.8-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.chat.send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)

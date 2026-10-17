import os
import streamlit as st
from google import genai

# 1. Page Configuration (Browser tab title & icon)
st.set_page_config(
    page_title="My zybo AI Assistant",  # Change the browser tab title
    page_icon="🤖",                        # Change the browser icon (emoji)
    layout="centered"                     # Options: "centered" or "wide"
)

# 2. Main Page Header
st.title("🤖 My Zybo AI Assistant")
st.caption("Powered by Google Gemini")

# Retrieve API key securely
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

@st.cache_resource
def get_client():
    return genai.Client(api_key=api_key)

client = get_client()

# 3. System Instruction / Behavior (Optional Customization)
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash"
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Box
if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    response = st.session_state.chat.send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.markdown(response.text)

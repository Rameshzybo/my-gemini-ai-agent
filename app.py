import os
import json
import streamlit as st
from google import genai

# 1. Page Configuration (Browser tab title & icon)
st.set_page_config(
    page_title="My Zybo AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# 2. Display Zybo Logo and Header
st.image("https://raw.githubusercontent.com/Rameshzybo/my-gemini-ai-agent/main/logo.png", width=220)

st.title("My Zybo AI Assistant")
st.caption("Powered by Google Gemini")

# 3. Local File for Storing Chat History
CHAT_HISTORY_FILE = "chat_history.json"

def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_chat_history(messages):
    with open(CHAT_HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# Retrieve API key securely
api_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY"))

@st.cache_resource
def get_client():
    return genai.Client(api_key=api_key)

client = get_client()

# 4. System Instruction / Behavior & Chat Session
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(
        model="gemini-3.8-flash"
    )

# Load saved messages into session state
if "messages" not in st.session_state:
    st.session_state.messages = load_chat_history()

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

    # Save the updated conversation to local file
    save_chat_history(st.session_state.messages)

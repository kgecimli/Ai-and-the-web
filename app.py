import streamlit as st
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.chat import define_goal, handle_user_input
from utils.chat import guess

load_dotenv()

openai_api_key = os.getenv('OPENAI_KEY')

with st.sidebar:
    st.write("sidebar")

st.title("💬 Chatbot")

client = OpenAI(api_key=openai_api_key)

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if "goal" not in st.session_state:
    define_goal(client)

client = OpenAI(api_key=openai_api_key)
handle_user_input(client)

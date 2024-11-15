import streamlit as st
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.chat import define_goal, handle_user_input, populate_sidebar, init_session_variables
from utils.chat import guess

load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
if "loaded" not in st.session_state or not st.session_state.loaded:
    init_session_variables()

populate_sidebar()

st.title("💬 Chatbot")

client = OpenAI(api_key=openai_api_key)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if not st.session_state.goal:
    define_goal(client)

client = OpenAI(api_key=openai_api_key)
handle_user_input(client)

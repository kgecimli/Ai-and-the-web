import streamlit as st
import random
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.chat import handle_user_input, init_session_variables, start, hint, create_response, write_messages
from utils.ui import restart_button, give_up_button, hint_button, sidebar


if "loaded" not in st.session_state or not st.session_state.loaded:
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=openai_api_key)
    init_session_variables()
    st.session_state.client = client

client = st.session_state.client

st.title("💬 Chatbot")
sidebar()

write_messages()
handle_user_input(client)

if not st.session_state.goal:
    start(client,
          intro_msg="Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                    "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")

restart_button(client)
give_up_button(client)
hint_button(client)

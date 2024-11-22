import os

import streamlit as st
from dotenv import load_dotenv  # ist um den wert aus der env datei zu laden
from openai import OpenAI

from utils.chat import handle_user_input, init_session_variables, start, write_messages
from utils.ui import restart_button, give_up_button, hint_button, sidebar

# setup
if "loaded" not in st.session_state or not st.session_state.loaded:  # st.session_state ist ein dictionary
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=openai_api_key)
    init_session_variables()
    st.session_state.client = client

# ui building
st.title("💬 Chatbot")
sidebar()

write_messages()

# TODO: buttons in sidebar

restart_button()
give_up_button()
hint_button()

# user handling

# if no goal is defined, we are just starting the first session
if not st.session_state.goal:
    start(intro_msg="Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                    "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")
handle_user_input()

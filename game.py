import streamlit as st

from utils.chat import handle_user_input, start, write_messages
from utils.ui import sidebar

# This page is the actual guessing game

# ui building
st.title("💬 Chatbot")
write_messages()

# if no goal is defined, we are just starting the first session
if not st.session_state.goal:
    start(intro_msg="Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                    "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")

# user handling
handle_user_input()

# sidebar at the end because of message order
sidebar()

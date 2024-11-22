import streamlit as st

from utils.chat import handle_user_input, init_session_variables, start, write_messages
from utils.ui import restart_button, give_up_button, hint_button, sidebar

with st.expander("Actions"):
    restart_button()
    give_up_button()
    #hint_button()

# ui building
st.title("💬 Chatbot")
#sidebar()

write_messages()

# TODO: buttons in sidebar

# user handling

# if no goal is defined, we are just starting the first session
if not st.session_state.goal:
    start(intro_msg="Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                    "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")
handle_user_input()
sidebar()
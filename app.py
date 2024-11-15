import streamlit as st
import random
import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.chat import handle_user_input, populate_sidebar, init_session_variables, start, hint, create_response


load_dotenv()
openai_api_key = os.getenv('OPENAI_KEY')
if "loaded" not in st.session_state or not st.session_state.loaded:
    init_session_variables()


populate_sidebar()

st.title("💬 Chatbot")

client = OpenAI(api_key=openai_api_key)

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


client = OpenAI(api_key=openai_api_key)
handle_user_input(client)

if not st.session_state.goal:
    start(client, intro_msg = "Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                            "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")


if st.button("Restart", type = "primary"):
    start(client = client, intro_msg = "I've got a new word for you. You can just continue playing as before.")

if st.button("Give up", type = "primary"):
    create_response(client = client, prompt= "The user gave up on our guessing game. Write a creative message to cheer them up and tell them that the word was ." + st.session_state.goal)
    #TODO: end the game such that you can't give up multiple times in a row for the same word

if st.button("Hint", type = "primary"):
    hint(client)
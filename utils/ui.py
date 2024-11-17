import streamlit as st
from openai import OpenAI

from utils.chat import start, create_response, hint


def restart_button(client: OpenAI):
    if st.button("Restart", type="primary"):
        start(client=client, intro_msg="I've got a new word for you. You can just continue playing as before.")


def give_up_button(client: OpenAI):
    if st.button("Give up", type="primary"):
        create_response(client=client,
                        prompt="The user gave up on our guessing game. Write a creative message to cheer them up and "
                               "tell them that the word was ." + st.session_state.goal)
        # TODO: end the game such that you can't give up multiple times in a row for the same word


def hint_button(client: OpenAI):
    if st.button("Hint", type="primary"):
        hint(client)


def sidebar():
    """
    fills the sidebar
    """
    with st.sidebar:
        st.write("sidebar")

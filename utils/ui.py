import streamlit as st

from utils.chat import start, create_response, hint


def restart_button():
    """
    creates a button and calls start() if pressed
    """
    if st.button("Restart", type="primary"):
        start(intro_msg="I've got a new word for you. You can just continue playing as before.")


def give_up_button():
    """
    creates a button WIP
    """
    if st.button("Give up", type="primary"):
        create_response(prompt="The user gave up on our guessing game. Write a creative message to cheer them up and "
                               "tell them that the word was ." + st.session_state.goal)
        # TODO: end the game such that you can't give up multiple times in a row for the same word


def hint_button():
    """
    creates a button and calls hint() if pressed
    """
    if st.button("Hint", type="primary"):
        hint()


def sidebar():
    """
    fills the sidebar
    """
    with st.sidebar:
        st.write("sidebar")

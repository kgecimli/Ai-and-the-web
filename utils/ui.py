import streamlit as st
from streamlit import session_state

from utils.chat import start, create_response, hint, append_message
from utils.statistics import Statistics


def restart_button():
    """
    creates a button and calls start() if pressed
    """
    if st.sidebar.button("Restart", type="primary"):
        #TODO: no idea why messages are not deleted right away (but maybe that's good)
        session_state.messages.clear()
        start(intro_msg="I've got a new word for you. You can just continue playing as before.")


def give_up_button():
    """
    creates a button WIP
    """
    if st.sidebar.button("Give up", type="primary"):
        create_response(prompt="The user gave up on our guessing game. Write a creative message to cheer them up and "
                               "tell them that the word was ." + st.session_state.goal)
        session_state.messages.clear()
        start(intro_msg="I've got a new word for you. You can just continue playing as before.")
        # TODO: end the game such that you can't give up multiple times in a row for the same word (current solution is not perfect)



def hint_button():
    """
    creates a button and calls hint() if pressed
    """
    if st.sidebar.button("Hint", type="primary"):
        hint()


def sidebar():
    """
    fills the sidebar
    """
    with st.sidebar:
        st.write("sidebar")
        st.print(Statistics)
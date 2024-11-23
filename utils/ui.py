import streamlit as st
from streamlit import session_state

from utils.chat import start, create_response, hint, append_message, give_up
from utils.statistics import Statistics


def restart_button():
    """
    creates a button and calls start() if pressed
    """
    if st.button("Restart", type="primary"):
        # TODO: no idea why messages are not deleted right away (but maybe that's good)
        session_state.messages.clear()
        start(intro_msg="I've got a new word for you. You can just continue playing as before.", write=False)


def give_up_button():
    """
    creates a button WIP
    """
    st.button("Give up", type="primary", on_click=give_up)


def hint_button():
    """
    creates a button and calls hint() if pressed
    """
    st.button("Hint", type="primary", on_click=hint)


def sidebar():
    """
    fills the sidebar
    """
    with st.sidebar:
        st.markdown("## Actions")
        hint_button()
        give_up_button()
        restart_button()

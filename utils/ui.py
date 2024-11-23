import streamlit as st
from streamlit import session_state

from utils.chat import start, create_response, hint, append_message, give_up, restart
from utils.statistics import Statistics


def restart_button():
    """
    creates a button and calls start() if pressed
    """
    st.button("Restart", type="primary", on_click=restart)



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

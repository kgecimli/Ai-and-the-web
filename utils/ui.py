import streamlit as st

from utils.chat import hint, give_up, restart


def restart_button():
    """
    creates a button and calls restart() if pressed
    """
    st.button("Restart", type="primary", on_click=restart)


def give_up_button():
    """
    creates a button and calls give_up() if pressed
    """
    st.button("Give up", type="primary", on_click=give_up)


def hint_button():
    """
    creates a button and calls hint() if pressed
    """
    st.button("Hint", type="primary", on_click=hint)


def sidebar():
    """
    fills the sidebar with action buttons (hint, give up, restart)
    """
    with st.sidebar:
        st.markdown("## Actions")
        hint_button()
        give_up_button()
        restart_button()

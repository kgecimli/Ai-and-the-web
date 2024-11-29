import streamlit as st

from utils.chat import give_hint, give_up, restart

# This overrides the button width since we want our buttons to have a uniform width. <style> accesses CSS, button gets
# styles for <button> HTML Tags, width sets width to 100%, ensuring that buttons use the full width of their parent
# element, !important is used to override default streamlit styles. We simply do this for every button, since we only
# have those three we want to override
st.markdown(
    """
<style>
button {
    width: 100% !important;
}
</style>
""",
    unsafe_allow_html=True,
)


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
    st.button("Hint", type="primary", on_click=give_hint)


def sidebar():
    """
    fills the sidebar with action buttons (hint, give up, restart)
    """
    with st.sidebar:
        st.markdown("## Actions")
        hint_button()
        give_up_button()
        restart_button()

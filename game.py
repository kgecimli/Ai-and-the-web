import streamlit as st

from utils.chat import handle_user_input, start, write_messages
from utils.ui import sidebar

# This page is the actual guessing game


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

# ui building
with st.expander("Rules"):
    st.write("In this guessing game, I will provide you with a random noun. You can ask me as many yes/no questions "
             "as you want. If you think you got the word, you can guess by typing 'Guess:' followed by your guess. "
             "If you need a hint, want to give up or restart the game, use the buttons in the sidebar.")

st.title("Guess What⁉️")
write_messages()

# if no goal is defined, we are just starting the first session
if not st.session_state.goal:
    start(intro_msg="Welcome to the guessing game. I randomly chose a word you should guess now. You can either "
                    "ask me Yes/No questions or guess by typing 'Guess: ' followed by your guess.")

# user handling
handle_user_input()

# sidebar at the end because of message order
sidebar()

import streamlit as st
from openai import OpenAI


def append_and_write(role: str, message: str):
    """
    appends the given message and writes it to the chat
    :param role: role of the message
    :param message: message to be appended and written
    :return:
    """
    st.session_state.messages.append({"role": role, "content": message})
    st.chat_message(role).write(message)


def define_goal(client: OpenAI):
    """
    defines a goal for the streamlit session by prompting ChatGPT
    :param client: OpenAI client to use for prompts
    """
    goal_prompt = {"role": "user",
                   "content": "Give one random noun for my guessing game. Your answer should only consist of that one word."}
    st.session_state.goal = client.chat.completions.create(model="gpt-3.5-turbo", messages=[goal_prompt]).choices[
        0].message.content
    append_and_write("assistant", "Next guess word is: " + st.session_state.goal)


def guess(client: OpenAI, message: str):
    """
    function that evaluates whether the guess for the goal is correct
    :param client: OpenAI client to use for prompts
    :param message: user message
    """
    return_message = ""
    if st.session_state.goal.lower() not in message.lower():
        return_message = "Not quite yet. Guess again or continue asking yes/no questions."
    else:
        return_message = "Congratulations, you got the word!"
    append_and_write("assistant", return_message)
    if st.session_state.goal.lower() in message.lower():
        st.balloons()
        # FIXME das hier vllt eher wenn man den restart button drückt? und hier stattdessen "Wenn du nochmal spielen
        # FIXME möchtest, drücke einfach den restart button"
        define_goal(client)
        append_and_write("assistant", "I've got a new word for you. You can just continue playing as before.")


def start(client: OpenAI, clear: bool = True, intro_msg: str = ""):
    """
    starts a round of the guessing game
    :param client: OpenAI client to use for prompts
    :param clear: whether to delete previous messages
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    if clear:
        st.session_state.messages = []
    define_goal(client)
    if intro_msg:
        append_and_write("assistant", intro_msg)


def handle_user_input(client: OpenAI):
    """
    handles user input
    :param client: OpenAI client to use for prompts
    """
    if prompt := st.chat_input("Type here..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        if prompt.lower().startswith("guess:"):
            guess(client, message=prompt)
        elif prompt:
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)


def populate_sidebar():
    """
    fills the sidebar
    """
    with st.sidebar:
        st.write("sidebar")


def init_session_variables():
    """
    populates session state variables so we don't have to check every time
    TODO Idee: dict mit default values
    variables: messages (list), goal (string), loaded (bool)
    """
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "goal" not in st.session_state:
        st.session_state.goal = None
    if "loaded" not in st.session_state or not st.session_state.loaded:
        st.session_state.loaded = True

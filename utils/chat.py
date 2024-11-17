from venv import create

import streamlit as st
from openai import OpenAI
import random


def create_response(client: OpenAI, prompt: str, rand_sel: bool = False, append: bool = True) -> str:
    """
    :param client: the client used to generate the response
    :param prompt: prompt for the chatbot
    :param rand_sel: whether a random response should be selected or not
    :param append: whether the generated response should be appended and written or not
    :return: the response as a string
    """
    prompt = {"role": "user",
              "content": prompt}
    response_selection = 0
    responses = client.chat.completions.create(model="gpt-3.5-turbo", messages=[prompt]).choices
    if rand_sel:
        response_selection = random.randint(0, len(responses) - 1)
    response = responses[response_selection].message.content
    if append:
        append_and_write("assistant", response)
    return response


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
    # TODO: Idea: save goals we had before and tell ChatGPT to use a different one
    prompt = "Give one random noun for my guessing game. Your answer should only consist of that one word."
    already_used = [goal for goal in st.session_state.goals]
    if already_used:
        prompt += "Do not use any of the following words: " + ", ".join(already_used)
    st.session_state.goal = create_response(client=client,
                                            prompt=prompt,
                                            append=False, rand_sel=True)
    st.session_state.goals.append(st.session_state.goal)
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
        append_and_write("assistant", "To play again, press Restart.")


def start(client: OpenAI, clear: bool = True, intro_msg: str = ""):
    """
    starts a round of the guessing game
    :param client: OpenAI client to use for prompts
    :param clear: whether to delete previous messages
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    # TODO @abrecht this code does not delete the messages belonging to the previous guess word from the chat
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
    if "goals" not in st.session_state:
        st.session_state.goals = []
    if "client" not in st.session_state:
        st.session_state.client = None


def hint(client: OpenAI):
    messages_as_str = ""
    for message in st.session_state.messages:
        messages_as_str += message["content"] + "\n"
    create_response(client=client,
                    prompt="The user needs a hint to guess the word. Provide one based on the guessing word: " + st.session_state.goal + "and refer to the questions and guesses the user has done so far" + messages_as_str)


def write_messages():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

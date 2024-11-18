import streamlit as st
from openai import OpenAI


def create_response(prompt: str, hide: bool = False) -> str:
    """
    :param prompt: prompt for the chatbot
    :param hide: whether the generated response should be appended and written or not
    :return: the response as a string
    """
    prompt = {"role": "user",
              "content": prompt}
    responses = st.session_state.client.chat.completions.create(model="gpt-3.5-turbo",
                                                                messages=(st.session_state.messages + [prompt])).choices
    response = responses[0].message.content
    append_message("assistant", response, hidden=hide)
    return response


def append_message(role: str, message: str, hidden: bool = False):
    """
    appends the given message and writes it to the chat
    :param role: role of the message
    :param message: message to be appended and written
    :param hidden: whether the message is hidden or not
    """

    st.session_state.messages.append({"role": role, "content": message, "hidden": hidden})


def define_goal():
    """
    defines a goal for the streamlit session by prompting ChatGPT
    """
    # TODO: Idea: save goals we had before and tell ChatGPT to use a different one
    prompt = "Give one random noun for my guessing game. Your answer should only consist of that one word."
    already_used = [goal for goal in st.session_state.goals]
    if already_used:
        prompt += "Do not use any of the following words: " + ", ".join(already_used)
    st.session_state.goal = create_response(prompt=prompt,
                                            hide=False)
    st.session_state.goals.append(st.session_state.goal)
    # debug to see the goal
    append_message("assistant", "Next guess word is: " + st.session_state.goal)


def guess(message: str):
    """
    function that evaluates whether the guess for the goal is correct
    :param message: user message
    """
    return_message = ""
    # FIXME has to be identical not only included
    if st.session_state.goal.lower() not in message.lower():
        return_message = "Not quite yet. Guess again or continue asking yes/no questions."
    else:
        return_message = "Congratulations, you got the word!"
    append_message("assistant", return_message)
    if st.session_state.goal.lower() in message.lower():
        st.balloons()
        append_message("assistant", "To play again, press Restart.")


def start(intro_msg: str = ""):
    """
    starts a round of the guessing game
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    define_goal()
    if intro_msg:
        append_message("assistant", intro_msg)


def handle_user_input():
    """
    handles user input
    """
    if prompt := st.chat_input("Type here..."):
        append_message("user", prompt)
        if prompt.lower().startswith("guess:"):
            guess(message=prompt)
        elif prompt:
            # make sure chatgpt knows what to do
            append_text = (f". As a reminder, the goal word is {st.session_state.goal} and you should only ever "
                           f"respond with 'Yes' or 'No'.")
            # copy messages by value so we can modify the last user message for chatgpt without displaying the change
            prompt_msgs = st.session_state.messages[:]
            prompt_msgs[-1] = {"role": prompt_msgs[-1]["role"], "content": prompt_msgs[-1]["content"] + append_text}
            response = st.session_state.client.chat.completions.create(model="gpt-3.5-turbo", messages=prompt_msgs)
            msg = response.choices[0].message.content
            append_message("assistant", msg)


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


def hint():
    messages_as_str = ""
    for message in st.session_state.messages:
        messages_as_str += message["content"] + "\n"
    create_response(
        prompt="The user needs a hint to guess the word. Provide one based on the guessing word: " +
               st.session_state.goal +
               "and refer to the questions and guesses the user has done so far" +
               messages_as_str)


def write_messages():
    """
    write all messages saved in st.session_state.messages to chat
    """
    for msg in st.session_state.messages:
        print(msg)
        # dont display if hidden
        if not msg["hidden"]:
            st.chat_message(msg["role"]).write(msg["content"])


def yes_no_function(client: OpenAI, message: str):
    """
    function ensures that the guess will be answered with yes or no
    :param client:  
    :param message:
    :return:
    """

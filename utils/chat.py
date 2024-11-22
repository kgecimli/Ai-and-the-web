import streamlit as st
from openai import OpenAI
from streamlit import session_state

from utils.statistics import Statistics


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


def append_message(role: str, message: str, hidden: bool = False, write: bool = True):
    """
    appends the given message and writes it to the chat
    :param write: whether to instantly write the message
    :param role: role of the message
    :param message: message to be appended and written
    :param hidden: whether the message is hidden or not
    """

    st.session_state.messages.append({"role": role, "content": message, "hidden": hidden})
    if not hidden and write:
        st.chat_message(role).write(message)
        # write_messages()


def define_goal():
    """
    defines a goal for the streamlit session by prompting ChatGPT
    """
    prompt = "Give one random noun for my guessing game. Your answer should only consist of that one word. I really need a one word answer, any answer with more than one word will destroy my code."
    already_used = [goal for goal in st.session_state.goals]
    if already_used:
        prompt += "Do not use any of the following words: " + ", ".join(already_used)
    st.session_state.goal = create_response(prompt=prompt,
                                            hide=False)
    # check whether ChatGPTs goal word really only consists of one word, if yes append it, else redefine the goal word
    if len(st.session_state.goal.split()) == 1:
        # remove any spaces from the goal
        st.session_state.goals.append(st.session_state.goal.replace(" ", ""))
        # debug to see the goal
        append_message("assistant", "Next guess word is: " + st.session_state.goal)
    else:
        define_goal()


def guess(message: str):
    """
    function that evaluates whether the guess for the goal is correct
    :param message: user message
    """
    Statistics.num_of_guesses += 1
    return_message = ""
    if st.session_state.goal.lower() == message.lower():
        return_message = "Congratulations, you got the word!"
    else:
        return_message = "Not quite yet. Guess again or continue asking yes/no questions."
    append_message("assistant", return_message)
    if st.session_state.goal.lower() == message.lower():
        st.balloons()
        st.session_state.messages.clear()
        start(intro_msg="I've got a new word for you. You can just continue playing as before.")


def start(intro_msg: str = ""):
    """
    starts a round of the guessing game
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    Statistics.games_played += 1
    define_goal()
    if intro_msg:
        append_message("assistant", intro_msg)


def handle_user_input():
    """
    handles user input
    """
    if prompt := st.chat_input("Type here..."):
        append_message("user", prompt)
        if prompt.lower().startswith("guess: "):
            session_state.Statistics.guesses += 1
            # splits the prompt and excludes the first word (guess:) and any spaces, such that only the actual guess is passed to the guess function
            guess(message=' '.join(prompt.lower().split()[1:]).replace(" ", ""))
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
    if "Statistics" not in st.session_state:
        stats = Statistics(0,0,0,0)
        st.session_state.Statistics = stats



def hint():
    messages_as_str = ""
    for message in st.session_state.messages:
        messages_as_str += message["content"] + "\n"
    response = create_response(
        prompt="The user needs a hint to guess the word. Provide one based on the guessing word: " +
               st.session_state.goal +
               "but it is very important that the goal is not mentioned in the hint. Refer to the questions and guesses the user has done so far" +
               messages_as_str, hide=True)
    if st.session_state.goal in response:
        hint()
    else:
        append_message("assistant", response, write=False)


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
    if message != "Yes" and message != "No":
        create_response("you are really only allowed to answer with yes or no")

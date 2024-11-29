import random

import streamlit as st
from nltk.corpus import wordnet as wn
from streamlit import session_state

from utils.Statistics import Statistics
from utils.constants import INTRO_MSG, ASSISTANT, USER, GPT_VERSION, BACKUP_GOAL_WORDS, DEBUG, VALID_RESPONSES, \
    CORRECT_RESPONSE_PROMPT, GIVE_HINT_PROMPT, GIVE_UP_PROMPT, DEFINE_GOAL_PROMPT, DEFINE_GOAL_USED_PROMPT, \
    DEFINE_GOAL_FAILSAFE_PROMPT, IDK


# functions that are triggered by user actions
def handle_user_input():
    """
    handles user input by checking whether the input is a guess or a question and responding accordingly
    """
    user_msg = st.chat_input("Type here...")
    # if we dont get a user_msg we exit the function
    if not user_msg:
        return

    append_msg(USER, user_msg)
    write_message(USER, user_msg)
    # we saved the original user_msg, so we can modify it for following checks
    user_msg = user_msg.lower()
    if len(user_msg) > 10000:
        msg = "Wow, that's pretty big. Please keep your questions and guesses shorter."
        append_msg(ASSISTANT, msg)
        write_message(ASSISTANT, msg)
    elif user_msg.startswith("guess:"):
        st.session_state.statistics[-1].guesses += 1

        # splits the prompt and excludes the first word (guess:) and any spaces, such that only the actual guess
        # is passed to the guess function
        if st.session_state.debug:
            print(user_msg.split("guess:"))
        evaluate_guess(guess=user_msg.split("guess:")[1].strip())

    else:
        st.session_state.statistics[-1].questions += 1
        # make sure chatgpt knows what to do
        append_text = (f". As a reminder, the goal word is {st.session_state.goal} and you should only ever "
                       f"respond with 'Yes' or 'No'.")
        # copy messages by value so we can modify the last user message for chatgpt without displaying the change
        prompt_msgs = st.session_state.messages[:]
        msg = send_prompt(prompt_msgs[-1]["content"] + append_text)
        counter = 0  # counter for max amount of iterations
        while not yes_no_function(msg) and counter <= 5:
            msg = correct_response()
            counter += 1
        if not yes_no_function(msg):
            msg = "I am not sure, please ask me another question."
        append_msg(ASSISTANT, msg)
        write_message(ASSISTANT, msg)


def give_hint():
    """
    Gives the user a hint for the goal word
    """
    st.session_state.statistics[-1].hints += 1
    response = ""
    # ensure ChatGPT gives a proper response and does not spoil the goal word
    while st.session_state.goal in response or response == "" or not response.startswith("Hint:"):
        hints_so_far = [p["content"] for p in st.session_state.prompts if "hint:" in p["content"][:6].lower()]
        hints = ", ".join(hints_so_far) if len(hints_so_far) > 0 else "no hints"
        response = send_prompt(GIVE_HINT_PROMPT.format(goal_word=st.session_state.goal, hints=hints))
    append_msg(ASSISTANT, response)


def give_up():
    """
    called when user gives up. starts a new game
    """
    session_state.messages.clear()
    response = send_prompt(GIVE_UP_PROMPT.format(goal_word=st.session_state.goal))
    append_msg(ASSISTANT, response)
    start(intro_msg=INTRO_MSG, write=False)


def restart():
    """
    restarts the game
    """
    session_state.messages.clear()
    session_state.prompts.clear()
    start(intro_msg=INTRO_MSG, write=False)


# basic helper functions
def write_message(role, content):
    """
    writes a message to the chat
    :param role: role of the message
    :param content: content of the message
    :return:
    """
    st.chat_message(role).write(content)


def write_messages():
    """
    write all messages saved in st.session_state.messages to chat
    """
    for msg in st.session_state.messages:
        if st.session_state.debug:
            print(msg)
        write_message(msg["role"], msg["content"])


def append_msg(role: str, content: str):
    """
    appends a message to the session state
    :param role: role of the message
    :param content: content of the message
    """
    st.session_state.messages.append(to_prompt(role, content))


def to_prompt(role: str, content: str) -> dict:
    """
    takes a role and a messages and returns a dict in the ChatGPT-appropriate format
    :param role: role
    :param content: content
    :return: dict containing role and content
    """
    return {"role": role, "content": content}


def send_prompt(content: str) -> str:
    """
    Sends a prompt to the OpenAI API and returns the answer
    :param content: prompt for the chatbot
    :return: response given by ChatGPT
    """
    responses = (st.session_state.client
                 .chat.completions.create(model=GPT_VERSION,
                                          messages=(st.session_state.prompts + [to_prompt(USER, content)])).choices)
    # we take the first answer from gpt
    response = responses[0].message.content
    st.session_state.prompts.append(to_prompt(USER, content))
    st.session_state.prompts.append(to_prompt(ASSISTANT, response))
    if st.session_state.debug:
        print(f"Prompt: {content}\nResponse: {response}")
    return response


# more complex or specific functions
def init_session_variables():
    """
    populates session state variables so we don't have to check every time
    variables: messages (list), goal (str), loaded (bool), goals (list), client (OpenAI), statistics (list),
                debug (bool), prompts (list)
    """
    # all messages that are sent (or not sent but prompted)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    # the current goal word
    if "goal" not in st.session_state:
        st.session_state.goal = None
    # whether the setup has been done (set to True only when this function was executed)
    if "loaded" not in st.session_state or not st.session_state.loaded:
        st.session_state.loaded = True
    # list of all previous goal words
    if "goals" not in st.session_state:
        st.session_state.goals = []
    # OpenAI client used for prompting
    if "client" not in st.session_state:
        st.session_state.client = None
    # list of statistics objects
    if "statistics" not in st.session_state:
        st.session_state.statistics = []
    # debug flag for e.g. showing the goal word in the chat
    if "debug" not in st.session_state:
        st.session_state.debug = DEBUG
    # all prompts and responses sent and received from ChatGPT
    if "prompts" not in st.session_state:
        st.session_state.prompts = []


def start(intro_msg: str = None, write: bool = True):
    """
    starts a round of the guessing game
    :param write whether to instantly write the message
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    st.session_state.statistics.append(Statistics())
    define_goal()
    if intro_msg:
        append_msg(ASSISTANT, intro_msg)
        if write:
            write_message(ASSISTANT, intro_msg)


def define_goal(depth=0):
    """
    defines a goal for the streamlit session by prompting ChatGPT
    :parameter depth: recursion depth as a failsafe
    """
    already_used = [goal for goal in st.session_state.goals]
    if already_used:
        prompt = DEFINE_GOAL_USED_PROMPT.format(already_used=", ".join(already_used))
    else:
        prompt = DEFINE_GOAL_PROMPT
    new_goal = send_prompt(prompt)

    # check whether ChatGPTs goal word really only consists of one word, if yes append it, else redefine the goal word
    if len(new_goal.split()) == 1:
        # Remove all non-letter characters
        only_letters = ''.join(char for char in new_goal if char.isalpha())
        st.session_state.goals.append(only_letters)
        st.session_state.goal = only_letters

    elif depth >= 5:
        # in case ChatGPT goes crazy and doesnt give us a proper goal word
        new_goal = random.choice(BACKUP_GOAL_WORDS)
        st.session_state.goals.append(new_goal)
        st.session_state.goal = new_goal
        send_prompt(DEFINE_GOAL_FAILSAFE_PROMPT)
    else:
        # trying again
        depth += 1
        define_goal(depth)

    # debug to see the goal
    if st.session_state.debug:
        write_message(ASSISTANT, "Next guess word is: " + st.session_state.goal)


def evaluate_guess(guess: str):
    """
    function that evaluates whether the guess for the goal is correct
    :param guess: guess to be evaluated
    """
    if st.session_state.goal.lower() == guess.lower():
        st.balloons()
        st.session_state.messages.clear()
        start(intro_msg=INTRO_MSG)
    else:
        similarity_msg = calculate_similarity(guess)
        append_msg(ASSISTANT, similarity_msg)
        write_message(ASSISTANT, similarity_msg)


def calculate_similarity(message: str) -> str:
    """
    only works in english because wordnet only has english words
    :param message: word to be compared to goal word
    :return: similarity indicator message
    """
    # get synsets of both the guess and the goal word
    msg_synsets = wn.synsets(message)
    goal_synsets = wn.synsets(st.session_state.goal)

    # if no synsets were found for either word, abort
    if len(msg_synsets) == 0 or len(goal_synsets) == 0:
        st.session_state.statistics[-1].unknown += 1
        return ("Mh, I don't recognize this word. Please make sure your guess is a properly spelled english word "
                "without any special characters.")

    msg_synset = msg_synsets[0]
    goal_synset = goal_synsets[0]
    similarity = msg_synset.path_similarity(goal_synset)
    if not similarity:
        st.session_state.statistics[-1].unknown += 1
        return ("Mh, I don't recognize this word. Please make sure your guess is a properly spelled english word "
                "without any special characters.")
    similarity = similarity * 100
    # the best score you can probably reach is about 17 so everything above 12 is a good similarity score
    if similarity > 12:
        st.session_state.statistics[-1].verygood += 1
        return "You are very close. Keep going!"
    elif 12 > similarity > 10:
        st.session_state.statistics[-1].good += 1
        return "You are close."
    elif 10 >= similarity > 8:
        st.session_state.statistics[-1].moderate += 1
        return "Your guess goes in the right direction."
    elif 8 >= similarity > 6:
        st.session_state.statistics[-1].bad += 1
        return "Your guess is bad."
    elif 6 >= similarity:
        st.session_state.statistics[-1].verybad += 1
        return "It seems like you have no clue, maybe asking more questions might help."


def yes_no_function(response: str, predefined: str = IDK) -> bool:
    """
    Checks whether the given response is yes, no or a predefined message
    :param response: response to check
    :param predefined: alternative accepted message
    :return: whether the given response is yes, no or a predefined message
    """
    response = response.lower()
    return response in VALID_RESPONSES or response == predefined.lower()


def correct_response() -> str:
    """
    tries to correct ChatGPT's response by telling it to only answer with Yes or No
    """
    response = send_prompt(CORRECT_RESPONSE_PROMPT)
    return response

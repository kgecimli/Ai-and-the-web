import streamlit as st
from nltk.corpus import wordnet as wn
from streamlit import session_state

from utils.Statistics import Statistics


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
    response = responses[0].message.content  # we take the first answer from gpt
    append_message("assistant", response, hidden=hide)
    return response


def append_message(role: str, message: str, hidden: bool = False, write: bool = False):
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
                                            hide=not st.session_state.debug)
    # check whether ChatGPTs goal word really only consists of one word, if yes append it, else redefine the goal word
    if len(st.session_state.goal.split()) == 1:
        # Remove all non-letter characters
        only_letters = ''.join(char for char in st.session_state.goal if char.isalpha())
        st.session_state.goals.append(only_letters)
        # debug to see the goal
        if st.session_state.debug:
            append_message("assistant", "Next guess word is: " + st.session_state.goal)
    else:
        define_goal()


def guess(message: str):
    """
    function that evaluates whether the guess for the goal is correct
    :param message: user message
    """
    return_message = ""
    if st.session_state.goal.lower() == message.lower():
        return_message = "Congratulations, you got the word!"
    else:
        similarity(message)
    if st.session_state.goal.lower() == message.lower():
        st.balloons()
        st.session_state.messages.clear()
        start(intro_msg="I've got a new word for you. You can just continue playing as before.")


def start(intro_msg: str = "", write: bool = True):
    """
    starts a round of the guessing game
    :param write whether to instantly write the message
    :param intro_msg: message that's sent at the start of the game (if provided. By default, no message is sent)
    """
    st.session_state.statistics.append(Statistics(0, 0, 0))
    define_goal()
    if intro_msg:
        append_message("assistant", intro_msg, write=write)


def handle_user_input():
    """
    handles user input
    """
    if prompt := st.chat_input("Type here..."):
        append_message("user", prompt, write=True)
        if prompt.lower().startswith("guess:"):
            st.session_state.statistics[-1].guesses += 1
            # splits the prompt and excludes the first word (guess:) and any spaces, such that only the actual guess is passed to the guess function
            guess(message=prompt.split("guess:")[1].strip())
            # guess(message=' '.join(prompt.lower().split()[1:]).replace(" ", ""))
        elif prompt:
            st.session_state.statistics[-1].questions += 1
            # make sure chatgpt knows what to do
            append_text = (f". As a reminder, the goal word is {st.session_state.goal} and you should only ever "
                           f"respond with 'Yes' or 'No'.")
            # copy messages by value so we can modify the last user message for chatgpt without displaying the change
            prompt_msgs = st.session_state.messages[:]
            prompt_msgs[-1] = {"role": prompt_msgs[-1]["role"], "content": prompt_msgs[-1]["content"] + append_text}
            response = st.session_state.client.chat.completions.create(model="gpt-3.5-turbo", messages=prompt_msgs)
            msg = response.choices[0].message.content
            counter = 0  # counter for max amount of iterations
            while not yes_no_function(msg) and counter <= 5:
                msg = correct_response(prompt, msg)
                counter += 1

            append_message("assistant", msg, write=True)


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
    if "statistics" not in st.session_state:
        st.session_state.statistics = []
    if "debug" not in st.session_state:
        st.session_state.debug = False


def hint():
    st.session_state.statistics[-1].hints += 1
    messages_as_str = ""
    response = ""
    while st.session_state.goal in response or response == "" or not response.startswith("Hint:"):
        for message in st.session_state.messages:
            messages_as_str += message["content"] + "\n"
        response = create_response(
            prompt="The user needs a hint to guess the word. Provide one based on the guessing word: " +
                   st.session_state.goal +
                   "but it is very important that the goal is not mentioned in the hint. Refer to the questions and guesses the user has done so far. Your answer should start with 'Hint:', followed by the hint" +
                   messages_as_str, hide=True)
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


def yes_no_function(response: str):
    if response == "Yes" or response == "No" or response == "i am not sure, please ask me another question":
        return True
    else:
        return False


def correct_response(prompt: str, response: str):
    response = create_response(
        prompt="Only answer with 'Yes' or 'No' " +
               "If you are not sure how to answer say 'i am not sure, please ask me another question' ", hide=True, )
    return response


def similarity(message: str):
    """
    only works in english because wordnet only has english words
    :param message:  guess from the user
    :return:
    """
    synsets1 = wn.synsets(message)
    synsets2 = wn.synsets(st.session_state.goal)

    if len(synsets1) > 0 and len(synsets2) > 0:
        synset1 = synsets1[0]
        synset2 = synsets2[0]
        similarity_ = synset1.path_similarity(synset2)
        similarity_ = similarity_ * 100
        # the best score you can probably reach is about 17 so everything above 12 is a good similarity  score
        if similarity_ > 12:
            append_message(role="assistant", message=str("you are very close"), write=True)
        elif 12 > similarity_ > 10:
            append_message(role="assistant", message=str("you are close"), write=True)
        elif 10 >= similarity_ > 8:
            append_message(role="assistant", message=str("your guess goes in the right direction"), write=True)
        elif 8 >= similarity_ > 6:
            append_message(role="assistant", message=str("your guess is bad"), write=True)
        elif 6 >= similarity_ > 1:
            append_message(role="assistant", message=str("it seems like you have to clue, ask more questions"),
                           write=True)
    else:
        append_message(role="assistant",
                       message=str("i am not able to calculate the similarity meassure try somthing else"), write=True)


def give_up():
    """
    called when user gives up. starts a new game
    """
    session_state.messages.clear()
    create_response(prompt="The user gave up on our guessing game. Write a creative message to cheer them up and "
                           "tell them that the word was ." + st.session_state.goal)
    start(intro_msg="I've got a new word for you. You can just continue playing as before.", write=False)


def restart():
    # TODO: no idea why messages are not deleted right away (but maybe that's good)
    session_state.messages.clear()
    start(intro_msg="I've got a new word for you. You can just continue playing as before.", write=False)

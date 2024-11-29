INTRO_MSG = "I've got a new word for you. You can just continue playing as before."
ASSISTANT = "assistant"
USER = "user"
GPT_VERSION = "gpt-4o-mini"  # gpt-3.5-turbo
BACKUP_GOAL_WORDS = ["car", "fish", "orange", "christmas", "water", "candle", "guitar", "controller", "wardrobe"]
DEBUG = True
VALID_RESPONSES = ["yes.", "no.", "yes", "no", "I am not sure, please ask me another question."]

# responses
IDK = "I am not sure, please ask me another question."

# prompts
CORRECT_RESPONSE_PROMPT = ("If it is true for the Goal answer with 'Yes.' if it is false for the goal answer with 'No.'"
                           f" If you are not sure how to answer say '{IDK}'")
GIVE_HINT_PROMPT = (
    "The user needs a hint to guess the word. Provide one based on the goal word: {goal_word}. "
    "It is very important that the goal is not mentioned in the hint. Refer to the questions and guesses "
    "the user has done so far. Your first hint should be general and then the hints should get more and more"
    "specific. In the chat you will find several messages starting with 'Hint:'. It is of "
    "uttermost importance that your hint has a different meaning than those hints. Your hint should provide "
    "new information to the user they have not received yet through the chat. Your answer should start with "
    "'Hint:', followed by the hint")
GIVE_UP_PROMPT = ("The user gave up on our guessing game. Write a creative message to cheer them up and tell them that "
                  "the word was {goal_word}.")
DEFINE_GOAL_PROMPT = ("Give one random noun for my guessing game. Your answer should only consist of that one word. "
                      "I really need a one word answer, any answer with more than one word will destroy my code.")
DEFINE_GOAL_USED_PROMPT = ("Give one random noun for my guessing game. Your answer should only consist of that one "
                           "word. I really need a one word answer, any answer with more than one word will destroy my "
                           "code. Do not use any of the following words: {already_used}")
DEFINE_GOAL_FAILSAFE_PROMPT = ("I decided on a goal word by myself. In the following I will ask questions trying to "
                               "guess the word.")

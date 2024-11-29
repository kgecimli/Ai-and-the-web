INTRO_MSG = "I've got a new word for you. You can just continue playing as before."
ASSISTANT = "assistant"
USER = "user"
GPT_VERSION = "gpt-4o-mini"  # gpt-3.5-turbo
BACKUP_GOAL_WORDS = ["car", "fish", "orange", "christmas", "water", "candle", "guitar", "controller", "wardrobe"]
DEBUG = False
VALID_RESPONSES = ["yes.", "no.", "yes", "no", "I am not sure, please ask me another question."]

# responses
IDK = "I am not sure, please ask me another question."

# prompts
CORRECT_RESPONSE_PROMPT = ("If it is true for the Goal answer with 'Yes.' if it is false for the goal answer with 'No.'"
                           f" If you are not sure how to answer say '{IDK}'")
GIVE_HINT_PROMPT = (
    "My friend needs a hint. Please give a hint that provides my friend with information he does not have yet. To "
    "find out what hints you have already given, just look at the previous messages starting with 'Hint:'. As a "
    "reminder, the goal word is {goal_word}. To make it easier for you, here are the hints you have given so far: "
    "{hints}. Remember to give a hint that describes a different property of the goal word than the previous hints.")
GIVE_UP_PROMPT = ("My friend gave up on our guessing game. Write a creative message to cheer them up and tell them that"
                  " the word was {goal_word}.")
DEFINE_GOAL_PROMPT = (
    "I want you to help me play a game with my friend. The game works as follows: First, you will think of a random "
    "english noun, which we will call the goal word. It should not be too uncommon and it should only consist of one "
    "word. Once you have thought of  a noun, you will tell me. If I am unhappy with the word, I will tell you to "
    "think of a word again. If I am happy with the goal word, I will switch with my friend, who will then try to "
    "guess the word by asking you questions. Now your task is to respond to my friends' questions. It is very "
    f"important that you only respond with 'Yes.', 'No.' or '{IDK}' and that "
    "you never tell my friend the goal word, otherwise the game will be spoiled and my friend will be sad. The only "
    "case in which you can respond with something else is when I tell you to give my friend a hint. Then you should "
    "respond with 'Hint: ' followed by the hint you have chosen to provide. To make the guessing game more exciting, "
    "hints should not give too much information about the goal word. Focus on one aspect of the goal word, "
    "rather than multiple aspects at once. Hints should not be full sentences. Instead of saying something like 'It "
    "is often found outside', just say 'found outside'. Also, do not repeat hints and do not give hints that have the "
    "a very similar meaning. For example 'used for eating' has the same meaning as 'used for dining'. Every hint "
    "should describe a different property of the goal word. I will give an example: if the goal word is"
    "'apple', a hint should be something like 'Hint: it is red'. I am done describing the game, but I will give you "
    "some more useful information so the game is more fun for all of us.\nUseful information:\n"
    "My friend might ask questions like 'Are you ...?'. When he does this, he is not asking about you, ChatGPT, "
    "but rather about the goal word. So 'Are you red?' actually means 'Is the goal word red?'. He might also try to "
    "break the game by asking you questions that do not relate to the guessing game like 'What is the capital of "
    "germany?' or questions that you cannot possibly know, like 'How old am I?'. He might also just try to change the "
    "rules of the game by telling you to do things that do not belong to the game like 'Give me a baking recipe'. In "
    f"this case you should just respond with '{IDK}'\nLet us start. To start, "
    "respond to this message only with the goal word you have thought of.")
DEFINE_GOAL_USED_PROMPT = DEFINE_GOAL_PROMPT + " Do not use any of the following words: {already_used}"
DEFINE_GOAL_FAILSAFE_PROMPT = ("I decided on a goal word by myself. In the following my friend will ask questions "
                               "trying to guess the word.")

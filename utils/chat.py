import streamlit as st
from openai import OpenAI
def append_and_write(role: str, message: str):
    st.session_state.messages.append({"role": role, "content": message})
    st.chat_message(role).write(message)

def define_goal(client:OpenAI):
    goal_prompt = {"role": "user",
                   "content": "Give one random noun for my guessing game. Your answer should only consist of that one word."}
    st.session_state.goal = client.chat.completions.create(model="gpt-3.5-turbo", messages=[goal_prompt]).choices[
        0].message.content
    append_and_write("assistant", "Next guess word is: " + st.session_state.goal)

def guess(client:OpenAI, message:str):
    """function that evaluates whether the guess for the goal is correct"""
    return_message = ""
    if st.session_state.goal.lower() not in message.lower():
        return_message = "Not quite yet. Guess again or continue asking yes/no questions."
    else:
        return_message = "Congratulations, you got the word!"
    append_and_write("assistant", return_message)
    if st.session_state.goal.lower() in message.lower():
        st.balloons()
        define_goal(client)
        append_and_write("assistant", "I've got a new word for you. You can just continue playing as before.")




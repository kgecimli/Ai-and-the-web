import streamlit as st
from openai import OpenAI
def define_goal(client:OpenAI):
    if "goal" not in st.session_state:
        goal_prompt = {"role": "user",
                       "content": "Give one random noun for my guessing game. Your answer should only consist of that one word."}
        st.session_state.goal = client.chat.completions.create(model="gpt-3.5-turbo", messages=[goal_prompt]).choices[
            0].message.content
        st.chat_message("assistant").write(st.session_state.goal)


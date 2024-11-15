import streamlit as st
import random
import os
from dotenv import load_dotenv
from openai import OpenAI

from utils.chat import define_goal
from utils.chat import guess

load_dotenv()

openai_api_key = os.getenv('OPENAI_KEY')

with st.sidebar:
    st.write("sidebar")

st.title("💬 Chatbot")

client = OpenAI(api_key=openai_api_key)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]


for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if "goal" not in st.session_state:
    define_goal(client)

#if prompt := st.chat_input():
 #   if not openai_api_key:
  #      st.info("Please add your OpenAI API key to continue.")
   #     st.stop()

#prompt = st.chat_input("Type here...")
#current_message =  st.session_state.messages.content



client = OpenAI(api_key=openai_api_key)
if prompt:=st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    if prompt.lower().startswith("guess:"):
        guess(client, message =  prompt)
    elif prompt:
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
        msg = response.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)




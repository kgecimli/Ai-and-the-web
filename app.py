import os

import streamlit as st
from dotenv import load_dotenv  # ist um den wert aus der env datei zu laden
from openai import OpenAI

from utils.chat import init_session_variables

# setup
if "loaded" not in st.session_state or not st.session_state.loaded:  # st.session_state ist ein dictionary
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_KEY')
    client = OpenAI(api_key=openai_api_key)
    init_session_variables()
    st.session_state.client = client

game_page = st.Page("game.py", title="Guessing game", icon=":material/sports_esports:")
stats_page = st.Page("stats.py", title="Statistics", icon=":material/bar_chart:")

pg = st.navigation([game_page, stats_page])
st.set_page_config(page_title="Guessing GPT", page_icon=":material/sports_esports:")
pg.run()

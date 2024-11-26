import nltk
import streamlit as st
from openai import OpenAI

from utils.chat import init_session_variables

nltk.download("wordnet")

# setup
if "loaded" not in st.session_state or not st.session_state.loaded:  # st.session_state ist ein dictionary
    # loading the OpenAI key and creating a client
    openai_api_key = st.secrets.get("OPENAI_KEY")
    client = OpenAI(api_key=openai_api_key)

    # initialising all session variables once so we don't have to check if they exist every time
    init_session_variables()

    # making the client available everywhere in the app
    st.session_state.client = client

# pages
game_page = st.Page("game.py", title="Guessing game", icon=":material/sports_esports:")
stats_page = st.Page("stats.py", title="Statistics", icon=":material/bar_chart:")
credits_page = st.Page("credits.py", title="Credits", icon=":material/groups:")

pg = st.navigation([game_page, stats_page, credits_page])
st.set_page_config(page_title="Guessing GPT", page_icon=":material/sports_esports:", layout="wide")
pg.run()

import nltk
import streamlit as st

from utils.chat import init_app

# download wordnet from nltk for word similarity measuring
nltk.download("wordnet")

# setup
init_app()

# pages
game_page = st.Page("game.py", title="Play", icon=":material/sports_esports:")
stats_page = st.Page("stats.py", title="Stats", icon=":material/bar_chart:")
credits_page = st.Page("credits.py", title="Credits", icon=":material/groups:")

pg = st.navigation([game_page, stats_page, credits_page])
st.set_page_config(page_title="Guessing GPT", page_icon=":material/sports_esports:", layout="wide")
pg.run()

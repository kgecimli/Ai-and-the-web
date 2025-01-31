import pandas as pd
import streamlit as st

from utils.chat import init_app

# setup
init_app()

# This page displays statistics gathered from played rounds of the guessing game
st.title("Game statistics")

# extracting number of guesses for each individual game from the list of statistics
num_guesses = [element.guesses for element in st.session_state.statistics]
data_frame = pd.DataFrame(num_guesses, columns=["Numbers"], index=range(1, len(num_guesses) + 1))

# bar plot displaying number of guesses per game
st.markdown("### General stats")
st.markdown("**Number of guesses per game:**")
st.bar_chart(data_frame, x_label="Guesses", y_label="Game", horizontal=True)

# Average guesses make only sense if at least one game has been completed already
if len(st.session_state.statistics) > 1:
    average_guesses = sum(num_guesses)
    # -1 to exclude ongoing game (there is always a game running)
    average_guesses /= len(st.session_state.statistics) - 1
    st.markdown(f"**Games played:** {len(st.session_state.statistics) - 1}")
    st.markdown(f"**Average number of guesses per game:** {average_guesses}")

st.markdown("### Detailed stats")

for i, element in enumerate(st.session_state.statistics, 1):
    # for each game, output number of questions and of guesses
    st.markdown("#### Game " + str(i) + ": ")
    st.markdown(str(element))

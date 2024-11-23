import streamlit as st
import pandas as pd

st.write("hi")
i = 1


for element in st.session_state.statistics:
    #for each game, output number of questions and of guesses
    st.write("Game " + str(i) + ": ")
    st.write(element)
    i += 1

num_guesses = []
if st.session_state.statistics:
    for element in st.session_state.statistics:
        num_guesses.append(element.guesses)
    data_frame = pd.DataFrame(num_guesses, columns= ["Numbers"])
    #bar plot diplaying number of guesses per game
    st.write("Number of guesses per game:")
    st.bar_chart(data_frame, x_label = "Game", y_label = "Guesses", horizontal = True)
    average_guesses = 0
    for elements in st.session_state.statistics:
        average_guesses += elements.guesses
    average_guesses /= len(st.session_state.statistics)
    st.write(f"Average number of guesses per game: {average_guesses}")
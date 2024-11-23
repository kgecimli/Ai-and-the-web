import streamlit as st
import pandas as pd


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
    data_frame = pd.DataFrame(num_guesses, columns= ["Numbers"], index=range(1, len(num_guesses) + 1))
    #bar plot displaying number of guesses per game
    st.write("Number of guesses per game:")
    st.bar_chart(data_frame, x_label = "Guesses", y_label = "Game", horizontal = True)
    #Average guesses make only sense if at least one game has been completed already
    if len(st.session_state.statistics) > 1:
        average_guesses = 0
        for elements in st.session_state.statistics:
            average_guesses += elements.guesses
        #-1 to exclude ongoing game
        average_guesses /= len(st.session_state.statistics)-1
        st.write(f"Average number of guesses per game: {average_guesses}")
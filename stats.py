import streamlit as st
import pandas as pd

st.write("hi")
i = 1


for element in st.session_state.statistics:
    st.write("Game " + str(i) + ": ")
    st.write(element)
    i += 1

num_guesses = []
if st.session_state.statistics:
    for element in st.session_state.statistics:
        num_guesses.append(element.guesses)
    data_frame = pd.DataFrame(num_guesses, columns= ["Numbers"])
    st.bar_chart(data_frame)
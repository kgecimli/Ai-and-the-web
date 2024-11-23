import streamlit as st

st.write("hi")
i = 0
for element in st.session_state.statistics:
    st.write("Game " + i + ": ")
    st.write(element)
    i += 1
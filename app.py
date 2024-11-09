import streamlit as st
import random

st.title("Guess the Pokemons")

st.write("This is my first web app.")

if 'goal' not in st.session_state:
    st.session_state.goal = random.randint(1,100) #we want to guess a random number between 1 and 100
st.write("The right number is",st.session_state.goal) #everytime you enter something there will be a new number because it runs every time the client requests a new page
#the communication between server and client is stateless, we need a mechanism to store something in a so called session to solve this problem of the program always creating a new program every input
#sessions are recognised in coockies
#you can create this by session_state



guess = st.number_input(label="Guess a number", min_value=1, max_value=100) #every time the information is displayes the entire program is run again
st.write(guess) #we now have an input element where the user is expected to enter the number the user wants to guess

if guess == st.session_state.goal:
    st.balloons()
    st.session_state.goal = random.randint(1, 100)

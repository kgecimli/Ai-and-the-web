import streamlit as st

content = """These are the enormously talented programmers who dedicated huge parts of their lives and willpower to 
create this amazing app. The names of these icons of peak programmer performance are (in order of attractiveness): 
**Noah Schade** (_Head of International Business Relations and Partnerships_), **Adrian Brechtken** (_intern_), 
**Koray Erenler Gecimli** (_Geschäftsführer und AG Künstliche Intelligenz_)"""
st.title("Credits")
st.markdown(content)
st.image("static/programmers.jpeg")

import streamlit as st

from utils.chat import init_app

# setup
init_app()

content = """These are the enormously talented programmers who dedicated huge parts of their lives and willpower to 
create this masterpiece. The names of these icons of peak programmer performance are (in order of attractiveness): 
**Noah Schade** (_Head of International Business Relations and Partnerships_), **Adrian Brechtken** (_intern_), 
**Koray Erenler Gecimli** (_Geschäftsführer und AG Künstliche Intelligenz_)"""
st.title("Credits")
st.markdown(content)
st.image("static/programmers.jpeg")

cnt = """
### Here are our paypal links in case you want to contribute to our work
Please guys we really need this.
"""

urls = """
- [Noah's Paypal](https://www.paypal.me/NoahSchade825)
- [Adrian's Paypal](https://www.paypal.me/abrechtken)
- [Koray's Paypal](https://www.paypal.me/KorayGecimli)
"""
st.markdown(cnt)
with st.expander("..."):
    st.write(
        "Like actually guys we really really do we spend the last few years developing this and its not even good "
        "please")
st.markdown(urls)

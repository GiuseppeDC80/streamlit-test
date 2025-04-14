import streamlit as st

st.title("Hello, Streamlit!")

name = st.text_input("Come ti chiami?")
if name:
    st.write(f"Ciao, {name} 👋")

import streamlit as st
from rotta import defaults, programmi

st.set_page_config(page_title="Rotta Barca", layout="centered")
st.title("⛵️ Calcoli Rotta Barca")

scelte = list(programmi.keys())
scelta = st.selectbox("Scegli un programma:", scelte)
prog = programmi[scelta]

st.subheader("Inserisci i dati")
for key in prog["input"]:
    var = defaults[key]
    val = st.number_input(key.replace("_", " ").capitalize(), value=var.valore)
    var.valore = val

if st.button("Calcola"):
    prog["funzione"](defaults)
    st.subheader("Risultati")
    for out in prog["output"]:
        st.write(f"{out.replace('_',' ').capitalize()}: {defaults[out].valore}")

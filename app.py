
import streamlit as st
from math import isnan
from rotta_barca_varie_funzioni_3 import defaults, programmi

st.set_page_config(page_title="Rotta Barca", layout="centered")
st.title("⛵️ Calcoli Rotta Barca")

# Selezione programma
scelte = list(programmi.keys())
scelta = st.selectbox("Scegli un programma di calcolo:", scelte)
programma = programmi[scelta]

# Input dinamico
st.subheader("📥 Inserisci i dati")
for nome_input in programma["input"]:
    var = defaults[nome_input]
    valore = st.number_input(f"{nome_input.replace('_', ' ').capitalize()}", value=float(var.valore))
    var.valore = valore

# Esecuzione
if st.button("Calcola"):
    st.subheader("📤 Risultati")
    try:
        programma["funzione"](defaults)
    except Exception as e:
        st.error(f"Errore durante l'esecuzione: {e}")

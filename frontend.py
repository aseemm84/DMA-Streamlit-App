import streamlit as st
import backend as bk

st.title("Gen AI Project")

input_text = st.text_input("Enter  Your Message")

go_button = st.button("Go")

if go_button:
    output = bk.get_text_output(input_text)
    st.write(output)
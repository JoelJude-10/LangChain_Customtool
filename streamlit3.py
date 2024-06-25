import streamlit as st
import custom_tool
st.title("file converter")
user_input = st.text_input("Enter your wish")
a=0
if user_input:
    a = custom_tool.processing_tool(user_input)
st.write(a)
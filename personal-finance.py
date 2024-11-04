import pandas as pd
import requests
import streamlit as st
import os
from dotenv import load_dotenv
import numpy as np

st.set_page_config(
    page_title="Penny Pal 🧞‍♂️",
    page_icon=":money_with_wings:",
    layout="wide"
)

def main():
    st.markdown("<h1 style='text-align: center; color: #dcdcdc;'>Hi there! </h1> <h2 style='text-align: center;'>💰 Welcome to PennyPal, your Personal Finance genius 🧞‍♂️</h2>", unsafe_allow_html=True)    
    user_question = st.text_input("Ask me anything about your personal finance.")
    centering_html = """
    <div style='display: flex; justify-content: center; align-items: center; height: 135vh;'>
        <iframe title="Personal Finance Dash v1" width="1920" height="1080" src="https://app.powerbi.com/reportEmbed?reportId=dcc85b78-ef16-448a-9dfb-a22ab410f2bd&autoAuth=true&ctid=6dd87273-5fb3-4e6b-ac1c-029d6a5df713" frameborder="0" allowFullScreen="true"></iframe>
    </div>
    """
    st.markdown(centering_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
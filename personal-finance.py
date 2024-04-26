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
        <iframe title='Personal Finance Dash v1' width='1920' height='1080' src='https://app.powerbi.com/reportEmbed?reportId=adad8aec-38ff-4f42-91d7-90b9061e5f36&autoAuth=true&ctid=f0e2941c-aaa2-4a03-963b-404d2c2888b6' frameborder='0' allowFullScreen='false'></iframe>
    </div>
    """
    st.markdown(centering_html, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
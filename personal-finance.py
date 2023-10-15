import pandas as pd
import requests
import streamlit as st
import os
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse
from pandasai.helpers.openai_info import get_openai_callback
from dotenv import load_dotenv


load_dotenv()
GS_API = os.getenv('GS_API')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Send a request to the API and get the response
response = requests.get(GS_API)

# Parse the JSON data
data = response.json()

# Normalize the data and create a DataFrame
dfnor = pd.json_normalize(data)

#Clear empty rows
df = dfnor[dfnor['hash'] != ""]

st.set_page_config(
    page_title="Your Personal Finance Assistant 🧞‍♂️",
    page_icon=":money_with_wings:",
    layout="centered"
)

def main():
    st.markdown("<h1 style='text-align: center; color: #dcdcdc;'>Hi there! </h1> <h2>Welcome to PennyPal, your Personal Finance genius 🧞‍♂️💰</h2>", unsafe_allow_html=True)
    llm = OpenAI(api_token=OPENAI_API_KEY, temperature=0)
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse, "max_retries": 5, "conversational": True, "enable_cache": False})
    
    user_question = st.text_input("Ask me anything about your personal finance.")
    if user_question is not None and user_question != "":
        with get_openai_callback() as cb:
            output = sdf.chat(user_question)
            st.write(output)
            st.write(cb)

if __name__ == '__main__':
    main()

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
    page_title="Penny Pal 🧞‍♂️",
    page_icon=":money_with_wings:",
    layout="centered"
)

def main():
    st.markdown("<h1 style='text-align: center; color: #dcdcdc;'>Hi there! </h1> <h2 style='text-align: center;'>💰 Welcome to PennyPal, your Personal Finance genius 🧞‍♂️</h2>", unsafe_allow_html=True)
    llm = OpenAI(api_token=OPENAI_API_KEY, temperature=0)
    sdf = SmartDataframe(df, config={"llm": llm, "verbose": True, "response_parser": StreamlitResponse, "max_retries": 5, "conversational": True, "enable_cache": False})

    col1, col2 = st.columns([0.3, 0.6])

    with col1:

        if st.button('Detailed Monthly Expenses'):
            with get_openai_callback() as cb:
                st.write(sdf.chat("Show me a table with monthly total of the column \"outcome\", grouped by the column \"category\". Order ASCENDING by month. Use one column for every category. Exclude columns where categories is: T10, S.I Systems, Policy Reporter, Transfers and CRA. Replace empty (NaN) values with 0. Make one additional columns with the sum of the categories columns."))
                st.write(cb)

    with col2:

        if st.button('📊'):
            with get_openai_callback() as cb:
                st.write(sdf.chat("Show me a colored stacked bar chart with monthly total of the column "outcome", grouped by the column "category". Put legend for "category" outside the chart. Exclude rows where categories is: T10, S.I Systems, Policy Reporter, Transfers and CRA. Replace empty (NaN) values with 0. Filter results to month 6,7,8 and 9"))
                st.write(cb)
    
    user_question = st.text_input("Ask me anything about your personal finance.")
    if user_question is not None and user_question != "":
        with get_openai_callback() as cb:
            output = sdf.chat(user_question)
            st.write(output)
            st.write(cb)

if __name__ == '__main__':
    main()

import pandas as pd
import requests
import streamlit as st
import os
import pandasai
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.helpers.openai_info import get_openai_callback
from dotenv import load_dotenv



class StreamlitResponse(ResponseParser):
    def __init__(self, context):
        super().__init__(context)

    def format_plot(self, result) -> None:
        """
        Display plot against a user query in Streamlit
        Args:
            result (dict): result contains type and value
        """
        import matplotlib.pyplot as plt
        import matplotlib.image as mpimg

        # Load the image file
        try:
            image = mpimg.imread(result["value"])
        except FileNotFoundError:
            raise FileNotFoundError(f"The file {result['value']} does not exist.")
        except OSError:
            raise ValueError(f"The file {result['value']} is not a valid image file.")

        try:
            import streamlit as st
        except ImportError:
            raise ImportError(
                "The 'streamlit' module is required to use StreamLit Response. "
                "Please install it using pip: pip install streamlit"
            )

        # Display the image
        plt.imshow(image)
        fig = plt.gcf()
        st.pyplot(fig)

from pandasai.responses.response_parser import StreamlitResponse

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


def main():
    llm = OpenAI(api_token=OPENAI_API_KEY, temperature=0)
    sdf = SmartDataframe(df, config={"llm": llm, "enable_cache": False, "verbose": True, "conversational": True, "response_parser": StreamlitResponse})
    st.set_page_config(
        page_title="You Personal Finance Assistant 🧞‍♂️",
        page_icon=":sales:",
        layout="centered"
        )
    
    st.header("Hi, I am PennyPal! 🧞‍♂️💰")
    user_question = st.text_input("Ask me a question about your finances.")
    if user_question is not None and user_question != "":
        with get_openai_callback() as cb:
            output = sdf.chat(user_question)
            st.write(output)
            st.write(cb)

if __name__ == '__main__':
    main()

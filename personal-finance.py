import pandas as pd
import requests
import streamlit as st
import os
import pandasai
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.helpers.openai_info import get_openai_callback
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

class StreamlitResponse:
    def __init__(self):
        pass

    def format_plot(self, result) -> None:
        """
        Display plot against a user query in Streamlit
        Args:
            result (dict): result contains type and value
        """
        # Load the image file
        try:
            image = mpimg.imread(result["value"])
        except FileNotFoundError:
            st.error(f"The file {result['value']} does not exist.")
            return
        except OSError:
            st.error(f"The file {result['value']} is not a valid image file.")
            return

        # Display the image
        plt.imshow(image)
        fig = plt.gcf()
        st.pyplot(fig)

    def format_dataframe(self, dataframe) -> None:
        """
        Display a DataFrame in Streamlit
        """
        st.write(dataframe)

    def format_other(self, result) -> None:
        """
        Handle other types of outputs in Streamlit
        """
        st.write(result)




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
    # ... (your previous code)

    if user_question is not None and user_question != "":
        with get_openai_callback() as cb:
            output = sdf.chat(user_question)
            # Debug: print the type and value of output
            print(f"Type of output: {type(output)}")
            print(f"Value of output: {output}")

            # Check if output is a dictionary before accessing its elements
            if isinstance(output, dict):
                if 'type' in output and 'value' in output:
                    if output['type'] == 'plot':
                        img_path = output['value']
                        st.image(img_path, caption='Your Plot', use_column_width=True)
                    else:
                        st.write(output['value'])
                else:
                    st.write("Output does not contain 'type' or 'value'")
            else:
                st.write("Unexpected output format")
                st.write(output)

if __name__ == '__main__':
    main()


import pandas as pd
import requests
import streamlit as st
import os
from dotenv import load_dotenv
from pandasai.llm import OpenAI
from pandasai import SmartDataframe
from pandasai.responses.streamlit_response import StreamlitResponse
from pandasai.helpers.openai_info import get_openai_callback
import numpy as np
import matplotlib.pyplot as plt
import squarify

st.set_page_config(
    page_title="Penny Pal 🧞‍♂️",
    page_icon=":money_with_wings:",
    layout="centered"
)

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
    st.markdown("<h1 style='text-align: center; color: #dcdcdc;'>Hi there! </h1> <h2 style='text-align: center;'>💰 Welcome to PennyPal, your Personal Finance genius 🧞‍♂️</h2>", unsafe_allow_html=True)
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

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    datetime_columns = df.select_dtypes(['datetime64']).columns

    # Filtering the "category" column
    if "category" in df.columns:
        unique_values = df["category"].unique()
        multi_select_values = st.multiselect(
            "Select values for category", 
            unique_values, 
            default=unique_values  # set default to all unique values
        )
        df = df[df["category"].isin(multi_select_values)]

    # Filtering datetime columns
    for column in datetime_columns:
        min_date = df[column].min()
        max_date = df[column].max()
        date_values = st.date_input(
            f"Select a date range for {column}",
            (min_date, max_date)
        )
        df = df[(df[column] >= date_values[0]) & (df[column] <= date_values[1])]

    return df

df_filtered = filter_dataframe(df)

df2 = df

# Ensure the date column is in datetime format
df2['date'] = pd.to_datetime(df2['date'])

# Set the date as the index
df2.set_index('date', inplace=True)

# Resampling data monthly and summing it with numeric_only=True to avoid FutureWarning
monthly_data = df2.resample('M').sum(numeric_only=True)

# Plotting Time Series Analysis
fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(monthly_data.index, monthly_data['income'], label='Income', color='green')
ax1.plot(monthly_data.index, monthly_data['outcome'], label='Outcome', color='red')
ax1.set_title('Monthly Income and Outcome Over Time')
ax1.set_xlabel('Date')
ax1.set_ylabel('Amount')
ax1.legend()

# Category Analysis with numeric_only=True to avoid FutureWarning
category_data = df_filtered.groupby('category').sum(numeric_only=True)

# Filter categories with outcome greater than 0
category_data = category_data[category_data['outcome'] > 0]

# Plotting pie chart for outcome
fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.pie(category_data['outcome'], labels=category_data.index, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax2.set_title('Distribution of Expenses by Category')

# Grouping data by supplier and summing it
supplier_data = df_filtered.groupby('supplier').sum(numeric_only=True)

# Sorting values to keep the highest at the top and selecting top 10
top_10_suppliers = supplier_data.sort_values(by='outcome', ascending=False).head(10)

# Creating tree map
fig3, ax3 = plt.subplots(figsize=(12, 8))
squarify.plot(sizes=top_10_suppliers['outcome'], label=top_10_suppliers.index, alpha=0.6, color=plt.cm.Paired.colors)
ax3.set_title('Expenses by Top 10 Suppliers')

# Remove axis
ax3.axis('off')

# Ensure each day has unique values by grouping by day and summing
df_daily = df.resample('D').sum(numeric_only=True)


# Determine the last date in the dataset
last_date = df_daily.index.max()

# Filter data for the last 3 months
three_months_data = df_daily.loc[last_date - pd.DateOffset(months=3):last_date]

# Group by month and sum
monthly_data = three_months_data.resample('M').sum()

# Plotting
fig4, ax4 = plt.subplots(figsize=(10, 5))
monthly_data['outcome'].plot(kind='bar', ax=ax4)
ax4.set_title('Expenses in the Last 3 Months')
ax4.set_xlabel('Month')
ax4.set_ylabel('Amount')
ax4.set_xticklabels([date.strftime('%Y-%m') for date in monthly_data.index], rotation=45)

# Drop unnecessary columns
df_cleaned = df.drop(columns=['hash', 'split', 'original', 'origin'])

# Group by supplier and date to sum up transactions for the same supplier on the same date
df_cleaned = df_cleaned.groupby([df_cleaned.index, 'supplier']).sum().reset_index()

# Rename the columns for better understanding
df_cleaned.columns = ['Date', 'Supplier', 'Outcome', 'Income']

# Format the date column
#df_cleaned['Date'] = df_cleaned['Date'].dt.strftime('%B, %Y')

# Sort by 'Date' and then by 'Outcome'
df_cleaned = df_cleaned.sort_values(by=['Date', 'Outcome'], ascending=[False, False])

def dataframe_to_html_table(df):
    # Define styles for each column
    styles = {
        "Date": 'width: 30%',
        "Supplier": 'width: 30%',
        "Outcome": 'width: 20%',
        "Income": 'width: 20%'
    }
    
    # Convert dataframe to HTML
    table_html = df.to_html(classes='styled-table', border=0)
    
    # Apply the column widths
    for col, width in styles.items():
        table_html = table_html.replace(f'<th>{col}</th>', f'<th style="{width}">{col}</th>')
    
    return table_html

# Custom CSS for the table with a scrollbar
table_css = """
<style>
    .styled-table {
        height: 400px; /* Set the height you prefer */
        overflow-y: auto;
        display: block;
    }
    .styled-table th, .styled-table td {
        white-space: nowrap;  /* Prevents the cells from breaking content to next line */
    }
</style>
"""

# Render the styled HTML table in Streamlit
with st.expander("Expand to view a detailed table"):
    # Include the CSS and then the table HTML
    st.markdown(table_css + dataframe_to_html_table(df_cleaned), unsafe_allow_html=True)


# Define columns for the 2x2 layout
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Plotting Time Series Analysis for Monthly Income and Outcome Over Time
with col1:
    st.pyplot(fig1)

# Plotting Distribution of Expenses by Category
with col2:
    st.pyplot(fig2)

# Plotting Expenses by Top 10 Suppliers
with col3:
    st.pyplot(fig3)

# Plotting Expenses in the Last 3 Months
with col4:
    st.pyplot(fig4)



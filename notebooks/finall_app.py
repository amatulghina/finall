import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib
import gspread
from google.oauth2 import service_account

# Load the Google Sheets credentials from the Streamlit secrets
google_sheets_creds = st.secrets["google_sheets"]

# Create credentials using the google.oauth2 library
credentials = service_account.Credentials.from_service_account_info(google_sheets_creds)

# Define the scope (permissions) for the Google Sheets API
scoped_credentials = credentials.with_scopes(
    ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
)

# Authenticate and initialize the gspread client with scoped credentials
client = gspread.authorize(scoped_credentials)

# Open the Google Sheet by name
sheet = client.open("finall_project").visitor


st.write("""
# Welcome to FinAll Project!

Financial Education for All
""")

with st.form("User Profile"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=10, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    country = st.text_input("Country")
    submit = st.form_submit_button("Submit")

if submit:
    # Append the data to Google Sheets
    try:
        sheet.append_row([name, age, gender, country, savings])
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")





import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load the Google Sheets credentials from the Streamlit secrets
google_sheets_creds = st.secrets["google_sheets"]

# Define the scope (permissions) for the Google Sheets API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Set up the credentials for accessing Google Sheets
credentials = ServiceAccountCredentials.from_json_keyfile_dict(google_sheets_creds, scope)

# Authenticate and initialize the gspread client
client = gspread.authorize(credentials)

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





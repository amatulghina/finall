import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib
from datetime import datetime
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
sheet = client.open("finall_project").worksheet("visitor")


st.write("""
# Welcome to FinAll Project!

Financial Education for All
""")


st.write("""
Introduction content (to be developed)

In order to give you personalized financial advice, we would like to know you more.
Please fill the form below:

""")

with st.form("User Profile"):
    st.header("User Profile Information")
    country = st.selectbox("Country", ["France", "Germany", "Spain"])
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=15, max_value=100)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    # Risk Profiling Section
    st.header("Risk Profiling Questionnaire")
    # Risk Needs
    q1 = st.radio("What is the primary goal for your investment?", 
                  ["Capital preservation", "Moderate capital growth", "High capital growth"])
    q2 = st.radio("What is your expected investment time horizon?", 
                  ["Less than 3 years", "3-10 years", "More than 10 years"])
    q3 = st.radio("What annual return do you expect from your investments?", 
                  ["3-5%", "5-10%", "More than 10%"])

    # Risk-Taking Ability
    q4 = st.radio("What is your current annual income compared to your necessary living expenses?", 
                  ["Income is just sufficient", "Income exceeds expenses slightly", "Income greatly exceeds expenses"])
    q5 = st.radio("How would you describe your current savings?", 
                  ["Little to no savings", "Modest savings", "Significant savings"])
    q6 = st.radio("How secure is your primary source of income?", 
                  ["Not very stable", "Somewhat stable", "Very stable"])

    # Behavioral Loss Tolerance
    q7 = st.radio("If the value of your investment dropped by 10%, what would you do?", 
                  ["Sell immediately", "Do nothing", "Buy more"])
    q8 = st.radio("How would you feel if your portfolio lost 20% in 6 months?", 
                  ["Very uncomfortable", "Somewhat uncomfortable", "Comfortable"])
    q9 = st.radio("How much risk are you willing to take for higher returns?", 
                  ["Minimize risk", "Moderate risk", "High risk"])

    # Submit button
    submit = st.form_submit_button("Submit")
    
# Logic after form submission
if submit:
    # Check if all required fields are filled
    if not name:
        st.warning("Please fill in your name.")
    if not age:
        st.warning("Please fill in your age.")
    if not gender:
        st.warning("Please fill in your gender.")
    
    else:
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Collect user profile and risk profile data in one row
        user_data = [
            timestamp,  # Current timestamp
            name,       # Name
            age,        # Age  
            gender,     # Gender  
            country,    # Country
            q1, q2, q3, # Risk Needs
            q4, q5, q6, # Risk-Taking Ability
            q7, q8, q9  # Behavioral Loss Tolerance
        ]
        sheet.append_row(user_data)
        st.success(f"Thank you, {name}!")
        

        

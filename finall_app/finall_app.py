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
sheet2 = client.open("finall_project").worksheet("stock_index")

st.set_page_config(page_title="FinAll")

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
    country = st.selectbox("Country (Required)", ["France", "Germany", "Spain"])
    name = st.text_input("Name")
    age = st.number_input("Age (Required)", min_value=15, max_value=100)
    gender = st.selectbox("Gender (Required)", ["Male", "Female", "Other"])
    
    # Risk Profiling Section
    st.header("Risk Profiling Questionnaire")
    # Risk Needs
    q1 = st.radio("What is the primary goal for your investment?", 
                  ["Capital preservation", "Moderate capital growth", "High capital growth"])
    q2 = st.radio("What is your expected investment time horizon?", 
                  ["Less than 5 years", "5-10 years", "More than 10 years"])
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
    if not age:
        st.warning("Please fill in your age.")
    elif not gender:
        st.warning("Please fill in your gender.")
    
    else:
        points = 0
        # Assign points based on answers (you can create mappings for each question)
        points += {"Capital preservation": 1, "Moderate capital growth": 2, "High capital growth": 3}[q1]
        points += {"Less than 5 years": 1, "5-10 years": 2, "More than 10 years": 3}[q2]
        points += {"3-5%": 1, "5-10%": 2, "More than 10%": 3}[q3]
        points += {"Income is just sufficient": 1, "Income exceeds expenses slightly": 2, "Income greatly exceeds expenses": 3}[q4]
        points += {"Little to no savings": 1, "Modest savings": 2, "Significant savings": 3}[q5]
        points += {"Not very stable": 1, "Somewhat stable": 2, "Very stable": 3}[q6]
        points += {"Sell immediately": 1, "Do nothing": 2, "Buy more": 3}[q7]
        points += {"Very uncomfortable": 1, "Somewhat uncomfortable": 2, "Comfortable": 3}[q8]
        points += {"Minimize risk": 1, "Moderate risk": 2, "High risk": 3}[q9]

        # Risk Needs
        risk_need = 0
        risk_need += {"Capital preservation": 1, "Moderate capital growth": 2, "High capital growth": 3}[q1]
        risk_need += {"Less than 5 years": 1, "5-10 years": 2, "More than 10 years": 3}[q2]
        risk_need += {"3-5%": 1, "5-10%": 2, "More than 10%": 3}[q3]
        
        # Risk Taking Ability
        risk_taking = 0
        risk_taking += {"Income is just sufficient": 1, "Income exceeds expenses slightly": 2, "Income greatly exceeds expenses": 3}[q4]
        risk_taking += {"Little to no savings": 1, "Modest savings": 2, "Significant savings": 3}[q5]
        risk_taking += {"Not very stable": 1, "Somewhat stable": 2, "Very stable": 3}[q6]
        
        # Behavioural loss tolerance
        loss_tol = 0
        loss_tol += {"Sell immediately": 1, "Do nothing": 2, "Buy more": 3}[q7]
        loss_tol += {"Very uncomfortable": 1, "Somewhat uncomfortable": 2, "Comfortable": 3}[q8]
        loss_tol += {"Minimize risk": 1, "Moderate risk": 2, "High risk": 3}[q9]
        
        # Determine the risk profile based on the total score
        if points <= 9:
            profile = "Conservative"
        elif points <= 18:
            profile = "Moderate"
        else:
            profile = "Aggressive"
        
        # Function to generate sequential user ID
        def get_user_id(sheet):
            # Get all records from the sheet
            records = sheet.get_all_records()

            # Check if the sheet is empty
            if len(records) == 0:
                # Start with ID '00000001' if the sheet is empty
                return "00000001"

            # Get the last row's ID
            last_row = records[-1]
            last_id = last_row.get("user_id")  # Assumes 'ID' is the column header for the ID field

            # Increment the last ID
            next_id = int(last_id) + 1

            # Pad the ID with leading zeros to ensure 8 digits
            return str(next_id).zfill(8)
        
        # Generate User ID
        user_id = get_user_id(sheet)
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Collect user profile and risk profile data in one row
        user_data = [
            timestamp,  # Current timestamp
            user_id,    # User ID
            name,       # Name
            age,        # Age  
            gender,     # Gender  
            country,    # Country
            q1, q2, q3, # Risk Needs
            q4, q5, q6, # Risk-Taking Ability
            q7, q8, q9, # Behavioral Loss Tolerance
            risk_need,  # Risk Needs Points
            risk_taking,# Risk-Taking Ability Points
            loss_tol,   # Behavioral Loss Tolerance Points
            points,      # Total Points
            profile     # Overall Risk Profile
        ]
        
        sheet.append_row(user_data)
        
        st.success(f"Thank you {name} for providing your information!")
        
        st.header("Investment Allocation Recommendation")
        
        st.write(f"Based on the information provided, you are categorized as a **{profile}** investor. ")
        
        if profile == "Conservative":
            st.write(f"Given your **low risk tolerance** and preference for stable returns, we recommend focusing more on **low-risk instruments** such as government bonds and limiting your stock investments.")
        elif profile == "Moderate":
            st.write(f"Given your **moderate risk tolerance** and willingness to take on some risk for potential returns, we recommend **a balanced mix of stocks and bonds** in your investment portfolio.")
        elif profile == "Aggressive":
            st.write(f"As you are willing to **accept greater economic uncertainty** in exchange for the potential of higher returns, we suggest allocating a **significant portion of your investment portfolio to stocks**.")
        
        st.write("The table below provides a general classification of investment instruments based on their risk levels:")
        
        type_instruments = {
            'Risk Level': ["Low","Moderate","High"],
            'Example of Investing Instruments': ['Government Bonds \n High-quality Corporate Bonds',"Balanced mutual funds (bonds & stocks)",'Stocks'],
            'Description': ['Lower returns but are stable and less prone to volatility.','A balance of safety and growth.','Potential for high returns but also high volatility and risk.']
        }
        
        inv_instruments = pd.DataFrame(type_instruments)
        st.dataframe(inv_instruments, hide_index=True)
        
        st.write(f"""
        The **“100 - age rule”** is a popular guideline used in financial planning to roughly guide individuals determine an appropriate **asset allocation** between stocks (or equities) and bonds (or fixed-income investments) based on age. The rule suggests that you should subtract your age from 100 to determine the percentage of your investment portfolio that should be allocated to stocks, with the remaining portion allocated to bonds or other lower-risk assets. \n
Based on this rule, your investment portfolio may consists of :blue[**{100-age}%** in **stocks** and **{age}%** in **bonds**]. \n
:red[Keep in mind, **before building your investment portfolio**, you should have **established an emergency fund** (typically in forms of basic savings) at least between **3-6 months of living expenses**].
        """)
        
        # Next Section
        with st.form("User Profile"):
            response = st.radio(f"Do you want to know more about stock market index in {country} to build your investment portfolio?", ("Yes", "No"))
            # Submit button
            submit = st.form_submit_button("Submit")

            if st.button("Submit"):
                if response == "Yes":
                    sheet2.append_row(user_id, response)
                    # Redirect to another function or page
                    st.write("Redirecting to Stock Market Index Information Page (to be devloped)")
                    # Call next function
                else:
                    sheet2.append_row(user_id, response)
                    st.write("Thank you for visiting our app!")
                    st.stop()  # Stop further execution if No

        

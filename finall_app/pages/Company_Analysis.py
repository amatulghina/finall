import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib
from datetime import datetime

st.write("""
# Company Analysis
""")

# Define the stock market index by country
indices = {
    "France" : ["CAC 40","^FCHI",
                ['AIR.PA', 'ALO.PA', 'ORA.PA', 'BNP.PA', 'EN.PA', 'VIE.PA', 'ENGI.PA', 'CA.PA', 
                 'BN.PA', 'ACA.PA', 'SGO.PA', 'LR.PA', 'RMS.PA', 'RI.PA', 'SAN.PA', 'AI.PA',
                 'CAP.PA', 'SU.PA', 'DSY.PA', 'EDF.PA', 'VIV.PA', 'KER.PA', 'MC.PA', 'MT.PA',
                 'OR.PA', 'PUB.PA', 'SAF.PA', 'STM.PA', 'FTI.PA', 'DG.PA', 'HO.PA', 'ML.PA',
                 'FR.PA', 'WLN.PA', 'CS.PA', 'FP.PA', 'TTE.PA', 'SG.PA', 'URW.PA', 'VK.PA']],
    "Germany" : ["DAX 40","^GDAXI",
                 ['ADS.DE','AIR.DE','ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'CON.DE',
                  '1COV.DE', 'DHER.DE', 'DTE.DE', 'DPW.DE', 'DB1.DE', 'DBK.DE', 'ENR.DE', 'FRE.DE',   
                  'FME.DE', 'HEN3.DE', 'HNR1.DE', 'IFX.DE', 'LIN.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE',
                  'PUM.DE', 'RWE.DE', 'SAP.DE', 'SHL.DE', 'SIE.DE', 'VNA.DE', 'VOW3.DE', 'ZAL.DE',
                  'HEI.DE', 'BAYN.DE', 'SY1.DE', 'HFG.DE', 'MBG.DE', 'HLE.DE', 'BNR.DE', 'TYO.DE']],
    "Spain" : ["IBEX 35","^IBEX",
               ['ACX.MC', 'ACS.MC', 'AENA.MC', 'ALM.MC', 'AMS.MC', 'ANA.MC', 'BBVA.MC', 'BKT.MC',
                'CABK.MC', 'CLNX.MC', 'COL.MC', 'ELE.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IAG.MC',
                'IBE.MC', 'ITX.MC','MEL.MC', 'MTS.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'REP.MC', 'ROVI.MC',
                'SAB.MC', 'SAN.MC', 'SGRE.MC', 'SLR.MC', 'TEF.MC']]
        }


# Initialize session state variables
if 'country' not in st.session_state:
    st.session_state['country'] = 'France'  # Set a default country
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = indices[st.session_state['country']][2][0]  # Set default ticker based on the default country

# Function to handle country change
def update_ticker():
    # Update ticker options when country changes
    st.session_state['ticker'] = indices[st.session_state['country']][2][0]

# Selectbox for country with a callback to update ticker options
st.session_state['country'] = st.selectbox(
    "Country", 
    ["France", "Germany", "Spain"], 
    index=["France", "Germany", "Spain"].index(st.session_state['country']),
    on_change=update_ticker  # Callback function when country changes
)

# Selectbox for ticker, dynamically populated based on selected country
st.session_state['ticker'] = st.selectbox(
    "Select one of the companies in the list to be analyzed:", 
    indices[st.session_state['country']][2],  # Populate based on the selected country
    index=indices[st.session_state['country']][2].index(st.session_state['ticker']) if st.session_state['ticker'] in indices[st.session_state['country']][2] else 0
)

# Button to confirm selections and move to the next step
if st.button("Submit"):
    
    st.write("""
    # Fundamental Analysis
    """)
    
    # Use the selected country and ticker for modeling
    ticker = st.session_state['ticker']
    
    company = yf.Ticker(ticker)
    
    income_stmt = company.income_stmt.reset_index()
    income_stmt.columns = ['Income Statement','2023','2022','2021','2020','2019']
    income_stmt=income_stmt[['Income Statement','2023','2022','2021','2020']]
    list_income_stmt = ['Total Revenue','Cost of Revenue','Gross Profit','Operating Income','Net Income','Diluted EPS']
    income_stmt = income_stmt[income_stmt['Income Statement'].isin(list_income_stmt)]
    income_stmt[['2023','2022','2021','2020']] = income_stmt[['2023','2022','2021','2020']].astype(float) 
    income_stmt['Income Statement'] = pd.Categorical(income_stmt['Income Statement'], categories=list_income_stmt, ordered=True)
    income_stmt = income_stmt.sort_values('Income Statement')
    income_stmt.reset_index(drop=True, inplace=True)
    st.dataframe(income_stmt, hide_index=True)
    
    balance_sheet = company.balance_sheet.reset_index()
    balance_sheet.columns = ['Balance Sheet','2023','2022','2021','2020','2019']
    balance_sheet=balance_sheet[['Balance Sheet','2023','2022','2021','2020']]
    list_balance_sheet = ['Current Assets','Total Assets','Current Liabilities','Long Term Debt And Capital Lease Obligation','Stockholders Equity']
    balance_sheet = balance_sheet[balance_sheet['Balance Sheet'].isin(list_balance_sheet)]
    balance_sheet[['2023','2022','2021','2020']] = balance_sheet[['2023','2022','2021','2020']].astype(float) 
    balance_sheet['Balance Sheet'] = pd.Categorical(balance_sheet['Balance Sheet'], categories=list_balance_sheet, ordered=True)
    balance_sheet = balance_sheet.sort_values('Balance Sheet')
    balance_sheet.reset_index(drop=True, inplace=True)
    balance_sheet['Balance Sheet'] = balance_sheet['Balance Sheet'].replace('Long Term Debt And Capital Lease Obligation', 'Long Term Debt')
    st.dataframe(balance_sheet, hide_index=True)
    
    cash_flow = company.cashflow.reset_index()
    cash_flow.columns = ['Cash Flow','2023','2022','2021','2020','2019']
    cash_flow=cash_flow[['Cash Flow','2023','2022','2021','2020']]
    list_cash_flow = ['Operating Cash Flow','Investing Cash Flow','Financing Cash Flow','Free Cash Flow']
    cash_flow = cash_flow[cash_flow['Cash Flow'].isin(list_cash_flow)]
    cash_flow[['2023','2022','2021','2020']] = cash_flow[['2023','2022','2021','2020']].astype(float) 
    cash_flow['Cash Flow'] = pd.Categorical(cash_flow['Cash Flow'], categories=list_cash_flow, ordered=True)
    cash_flow = cash_flow.sort_values('Cash Flow')
    cash_flow.reset_index(drop=True, inplace=True)
    st.dataframe(cash_flow, hide_index=True)
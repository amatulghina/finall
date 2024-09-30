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

with st.form("Company"):
    country = st.selectbox("Country", ["France", "Germany", "Spain"])
    ticker = st.selectbox("Select one of the company in the list to be analysed:", indices[country][2])
    
    # Submit button
    submit = st.form_submit_button("Submit")

if submit:
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
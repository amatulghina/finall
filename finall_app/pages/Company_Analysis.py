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
                         'FR.PA', 'WLN.PA', 'CS.PA', 'FP.PA', 'TTE.PA', 'SG.PA', 'URW.PA', 'VK.PA'],
                       ['AXA SA','Airbus SE', 'Alstom SA', 'ArcelorMittal SA', 'BNP Paribas SA',
                         'Bouygues SA', 'Capgemini SE', 'Carrefour SA', 'Compagnie Générale des Établissements Michelin Société en commandite par actions',
                         'Compagnie de Saint-Gobain S.A.', 'Crédit Agricole S.A.', 'Danone S.A.', 'Dassault Systèmes SE',
                         'Engie SA', 'Hermès International Société en commandite par actions', 'Kering SA',
                         "L'Air Liquide S.A.", "L'Oréal S.A.", 'LVMH Moët Hennessy - Louis Vuitton, Société Européenne',
                         'Legrand SA', 'Orange S.A.', 'Pernod Ricard SA', 'Publicis Groupe S.A.',
                         'Safran SA', 'Sanofi', 'Schneider Electric S.E.', 'Thales S.A.',
                         'TotalEnergies SE', 'Unibail-Rodamco-Westfield SE', 'Valeo SE', 'Vallourec S.A.',
                         'Veolia Environnement SA', 'Vinci SA', 'Vivendi SE', 'Worldline SA']],
            "Germany" : ["DAX 40","^GDAXI",
                         ['ADS.DE','AIR.DE','ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'CON.DE',
                          '1COV.DE', 'DHER.DE', 'DTE.DE', 'DPW.DE', 'DB1.DE', 'DBK.DE', 'ENR.DE', 'FRE.DE',   
                          'FME.DE', 'HEN3.DE', 'HNR1.DE', 'IFX.DE', 'LIN.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE',
                          'PUM.DE', 'RWE.DE', 'SAP.DE', 'SHL.DE', 'SIE.DE', 'VNA.DE', 'VOW3.DE', 'ZAL.DE',
                          'HEI.DE', 'BAYN.DE', 'SY1.DE', 'HFG.DE', 'MBG.DE', 'HLE.DE', 'BNR.DE', 'TYO.DE'],
                        ['adidas AG','Airbus SE','Allianz SE','BASF SE','Bayer Aktiengesellschaft', 'Bayerische Motoren Werke Aktiengesellschaft',
                     'Beiersdorf Aktiengesellschaft', 'Brenntag SE', 'Continental Aktiengesellschaft', 'Covestro AG', 'Delivery Hero SE',
                     'Deutsche Bank Aktiengesellschaft', 'Deutsche Börse AG', 'Deutsche Telekom AG', 'Fresenius Medical Care AG',
                     'Fresenius SE & Co. KGaA', 'HELLA GmbH & Co. KGaA', 'Hannover Rück SE', 'Heidelberg Materials AG',
                     'HelloFresh SE', 'Henkel AG & Co. KGaA', 'Infineon Technologies AG', 'Linde plc',
                     'MTU Aero Engines AG', 'Mercedes-Benz Group AG', 'Merck KGaA', 'Münchener Rückversicherungs-Gesellschaft Aktiengesellschaft in München',
                    'PUMA SE', 'RWE Aktiengesellschaft', 'SAP SE', 'Siemens Aktiengesellschaft', 'Siemens Energy AG', 'Siemens Healthineers AG',
                     'Symrise AG', 'Volkswagen AG', 'Vonovia SE', 'Zalando SE']],
            "Spain" : ["IBEX 35","^IBEX",
                       ['ACX.MC', 'ACS.MC', 'AENA.MC', 'ALM.MC', 'AMS.MC', 'ANA.MC', 'BBVA.MC', 'BKT.MC',
                        'CABK.MC', 'CLNX.MC', 'COL.MC', 'ELE.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IAG.MC',
                        'IBE.MC', 'ITX.MC','MEL.MC', 'MTS.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'REP.MC', 'ROVI.MC',
                        'SAB.MC', 'SAN.MC', 'SGRE.MC', 'SLR.MC', 'TEF.MC'],
                      ['ACS, Actividades de Construcción y Servicios, S.A.','Acciona, S.A.', 'Acerinox, S.A.',
                     'Aena S.M.E., S.A.', 'Almirall, S.A.', 'Amadeus IT Group, S.A.', 'ArcelorMittal S.A.',
                     'Banco Bilbao Vizcaya Argentaria, S.A.', 'Banco Santander, S.A.', 'Banco de Sabadell, S.A.',
                     'Bankinter, S.A.', 'CaixaBank, S.A.', 'Cellnex Telecom, S.A.', 'Enagás, S.A.', 'Endesa, S.A.',
                     'Ferrovial SE', 'Grifols, S.A.', 'Iberdrola, S.A.', 'Industria de Diseño Textil, S.A.',
                     'Inmobiliaria Colonial, SOCIMI, S.A.', 'International Consolidated Airlines Group S.A.', 'Laboratorios Farmaceuticos Rovi, S.A.',
                     'Meliá Hotels International, S.A.', 'Naturgy Energy Group, S.A.', 'Pharma Mar, S.A.', 'Redeia Corporación, S.A.', 'Repsol, S.A.', 'Solaria Energía y Medio Ambiente, S.A.',
                     'Telefónica, S.A.']]
        }

company_tickers = {'Airbus SE': 'AIR.PA','Alstom SA': 'ALO.PA','Orange S.A.': 'ORA.PA','BNP Paribas SA': 'BNP.PA',
            'Bouygues SA': 'EN.PA','Veolia Environnement SA': 'VIE.PA','Engie SA': 'ENGI.PA','Carrefour SA': 'CA.PA',
            'Danone S.A.': 'BN.PA', 'Crédit Agricole S.A.': 'ACA.PA', 'Compagnie de Saint-Gobain S.A.': 'SGO.PA',
            'Legrand SA': 'LR.PA', 'Hermès International Société en commandite par actions': 'RMS.PA', 'Pernod Ricard SA': 'RI.PA',
            'Sanofi': 'SAN.PA', "L'Air Liquide S.A.": 'AI.PA', 'Capgemini SE': 'CAP.PA', 'Schneider Electric S.E.': 'SU.PA', 
            'Dassault Systèmes SE': 'DSY.PA', 'Vivendi SE': 'VIV.PA', 'Kering SA': 'KER.PA',
            'LVMH Moët Hennessy - Louis Vuitton, Société Européenne': 'MC.PA', 'ArcelorMittal SA': 'MT.PA', "L'Oréal S.A.": 'OR.PA',
            'Publicis Groupe S.A.': 'PUB.PA', 'Safran SA': 'SAF.PA', 'Vinci SA': 'DG.PA', 'Thales S.A.': 'HO.PA', 'Compagnie Générale des Établissements Michelin Société en commandite par actions': 'ML.PA',
            'Valeo SE': 'FR.PA', 'Worldline SA': 'WLN.PA', 'AXA SA': 'CS.PA', 'TotalEnergies SE': 'TTE.PA', 'Unibail-Rodamco-Westfield SE': 'URW.PA',
            'Vallourec S.A.': 'VK.PA',
            'adidas AG': 'ADS.DE','Airbus SE': 'AIR.DE', 'Allianz SE': 'ALV.DE',
             'BASF SE': 'BAS.DE', 'Bayer Aktiengesellschaft': 'BAYN.DE', 'Beiersdorf Aktiengesellschaft': 'BEI.DE',
            'Bayerische Motoren Werke Aktiengesellschaft': 'BMW.DE', 'Continental Aktiengesellschaft': 'CON.DE', 'Covestro AG': '1COV.DE', 'Delivery Hero SE': 'DHER.DE',
            'Deutsche Telekom AG': 'DTE.DE', 'Deutsche Börse AG': 'DB1.DE', 'Deutsche Bank Aktiengesellschaft': 'DBK.DE',
            'Siemens Energy AG': 'ENR.DE', 'Fresenius SE & Co. KGaA': 'FRE.DE', 'Fresenius Medical Care AG': 'FME.DE', 'Henkel AG & Co. KGaA': 'HEN3.DE',
            'Hannover Rück SE': 'HNR1.DE', 'Infineon Technologies AG': 'IFX.DE', 'Linde plc': 'LIN.DE', 'Merck KGaA': 'MRK.DE',
            'MTU Aero Engines AG': 'MTX.DE', 'Münchener Rückversicherungs-Gesellschaft Aktiengesellschaft in München': 'MUV2.DE',
            'PUMA SE': 'PUM.DE', 'RWE Aktiengesellschaft': 'RWE.DE', 'SAP SE': 'SAP.DE', 'Siemens Healthineers AG': 'SHL.DE', 'Siemens Aktiengesellschaft': 'SIE.DE', 'Vonovia SE': 'VNA.DE',
            'Volkswagen AG': 'VOW3.DE', 'Zalando SE': 'ZAL.DE', 'Heidelberg Materials AG': 'HEI.DE', 'Symrise AG': 'SY1.DE',
            'HelloFresh SE': 'HFG.DE', 'Mercedes-Benz Group AG': 'MBG.DE', 'HELLA GmbH & Co. KGaA': 'HLE.DE', 'Brenntag SE': 'BNR.DE',
            'Acerinox, S.A.': 'ACX.MC', 'ACS, Actividades de Construcción y Servicios, S.A.': 'ACS.MC',
            'Aena S.M.E., S.A.': 'AENA.MC', 'Almirall, S.A.': 'ALM.MC', 'Amadeus IT Group, S.A.': 'AMS.MC',
            'Acciona, S.A.': 'ANA.MC', 'Banco Bilbao Vizcaya Argentaria, S.A.': 'BBVA.MC',
            'Bankinter, S.A.': 'BKT.MC', 'CaixaBank, S.A.': 'CABK.MC', 'Cellnex Telecom, S.A.': 'CLNX.MC', 'Inmobiliaria Colonial, SOCIMI, S.A.': 'COL.MC',
            'Endesa, S.A.': 'ELE.MC', 'Enagás, S.A.': 'ENG.MC', 'Ferrovial SE': 'FER.MC', 'Grifols, S.A.': 'GRF.MC',
            'International Consolidated Airlines Group S.A.': 'IAG.MC', 'Iberdrola, S.A.': 'IBE.MC', 'Industria de Diseño Textil, S.A.': 'ITX.MC', 'Meliá Hotels International, S.A.': 'MEL.MC',
            'ArcelorMittal S.A.': 'MTS.MC', 'Naturgy Energy Group, S.A.': 'NTGY.MC',
            'Pharma Mar, S.A.': 'PHM.MC', 'Redeia Corporación, S.A.': 'RED.MC', 'Repsol, S.A.': 'REP.MC', 'Laboratorios Farmaceuticos Rovi, S.A.': 'ROVI.MC',
            'Banco de Sabadell, S.A.': 'SAB.MC', 'Banco Santander, S.A.': 'SAN.MC', 'Solaria Energía y Medio Ambiente, S.A.': 'SLR.MC', 'Telefónica, S.A.': 'TEF.MC'
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
    indices[st.session_state['country']][3],  # Populate based on the selected country
    index=indices[st.session_state['country']][3].index(st.session_state['ticker']) if st.session_state['ticker'] in indices[st.session_state['country']][3] else 0
)

# Button to confirm selections and move to the next step
if st.button("Submit"):
    ticker_company = st.session_state['ticker']
    ticker = company_tickers[ticker_company]
    company = yf.Ticker(ticker)

    st.write("""
    ### Company Information
    """)
    
    st.write(f"Company's Name: {company.info['longName']}")
    st.write(f"Company's Ticker: {ticker}")
    st.write(f"Industry: {company.info['industry']}")
    st.write(f"Address: {company.info['address1']}, {company.info['city']}")
    st.write(f"Number of Employees: {company.info['fullTimeEmployees']}")
    
    st.write("""
    ### Fundamental Analysis
    """)
    
    st.write("Fundamental analysis involves evaluating a company's **financial statements** (ie., Income Statement, Balance Sheet, Cash Flow), economic factors, and overall business health to determine its **intrinsic value**. The goal is to **identify whether a stock is overvalued or undervalued** based on its fundamentals, and then make a **long-term investment** decision accordingly.")
    
    # Income Statement    
    income_stmt = company.income_stmt.reset_index()
    income_stmt = income_stmt.iloc[:, :5]
    income_stmt.columns = ['Income Statement','2023','2022','2021','2020']
    list_income_stmt = ['Total Revenue','Cost of Revenue','Gross Profit','Operating Income','Net Income','Diluted EPS']
    income_stmt = income_stmt[income_stmt['Income Statement'].isin(list_income_stmt)]
    income_stmt[['2023','2022','2021','2020']] = income_stmt[['2023','2022','2021','2020']].astype(float) 
    income_stmt['Income Statement'] = pd.Categorical(income_stmt['Income Statement'], categories=list_income_stmt, ordered=True)
    income_stmt = income_stmt.sort_values('Income Statement')
    income_stmt.reset_index(drop=True, inplace=True)
    st.dataframe(income_stmt, hide_index=True)
    # Balance Sheet
    balance_sheet = company.balance_sheet.reset_index()
    balance_sheet = balance_sheet.iloc[:, :5]
    balance_sheet.columns = ['Balance Sheet','2023','2022','2021','2020']
    list_balance_sheet = ['Current Assets','Total Assets','Current Liabilities','Long Term Debt And Capital Lease Obligation','Stockholders Equity']
    balance_sheet = balance_sheet[balance_sheet['Balance Sheet'].isin(list_balance_sheet)]
    balance_sheet[['2023','2022','2021','2020']] = balance_sheet[['2023','2022','2021','2020']].astype(float) 
    balance_sheet['Balance Sheet'] = pd.Categorical(balance_sheet['Balance Sheet'], categories=list_balance_sheet, ordered=True)
    balance_sheet = balance_sheet.sort_values('Balance Sheet')
    balance_sheet.reset_index(drop=True, inplace=True)
    balance_sheet['Balance Sheet'] = balance_sheet['Balance Sheet'].replace('Long Term Debt And Capital Lease Obligation', 'Long Term Debt')
    st.dataframe(balance_sheet, hide_index=True)
    # Cash Flow
    cash_flow = company.cashflow.reset_index()
    cash_flow = cash_flow.iloc[:, :5]
    cash_flow.columns = ['Cash Flow','2023','2022','2021','2020']
    list_cash_flow = ['Operating Cash Flow','Investing Cash Flow','Financing Cash Flow','Free Cash Flow']
    cash_flow = cash_flow[cash_flow['Cash Flow'].isin(list_cash_flow)]
    cash_flow[['2023','2022','2021','2020']] = cash_flow[['2023','2022','2021','2020']].astype(float) 
    cash_flow['Cash Flow'] = pd.Categorical(cash_flow['Cash Flow'], categories=list_cash_flow, ordered=True)
    cash_flow = cash_flow.sort_values('Cash Flow')
    cash_flow.reset_index(drop=True, inplace=True)
    st.dataframe(cash_flow, hide_index=True)
    
    
    st.write("""
    ### Technical Analysis
    """)
    
    st.write("Technical analysis, on the other hand, involves analyzing **historical price** data and trading **volume** to predict future stock movements. It focuses on price patterns and market trends rather than the underlying value of the company. Typically used by traders for **short-term** trades but can also be applied to medium-term and long-term investments.")
    
    st.write(f"The two graphs below show the **closing price** and **trading volume** of {ticker}")
    
    # Download Historical Data
    data_tickers = yf.Tickers(ticker)
    df = data_tickers.tickers[ticker].history(period='1y')
    st.line_chart(df.Close)
    st.line_chart(df.Volume)
    
    
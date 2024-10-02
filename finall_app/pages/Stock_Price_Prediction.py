import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import itertools
from statsmodels.tsa.arima.model import ARIMA
import statsmodels.tsa.stattools as adfuller
import statsmodels.api as sm
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.stats import boxcox
from scipy.special import inv_boxcox
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

st.set_page_config(page_title="FinAll")

st.write("""
# Stock Price Prediction
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
    
    st.header("Short-Term")
    st.write(f"This is a short-term prediction of {ticker} stock price using ARIMA model.")
    
    # Download Historical Data
    data = yf.download(ticker, period='1mo')

    # Make the variance stationary
    data["Adj Close Log"] = np.log(data["Adj Close"])

    # Finding the best parameter for ARIMA model

    # Define p, d, and q ranges
    p = range(0, 5)
    d = range(0, 2)
    q = range(0, 5)

    # Generate all combinations of p, d, q
    pdq = list(itertools.product(p, d, q))
    best_aic = float('inf')
    best_order = None

    # Loop through all combinations of (p, d, q)
    for param in pdq:
        try:
            model = sm.tsa.ARIMA(data['Adj Close Log'], order=param)
            results = model.fit()
            if results.aic < best_aic:
                best_aic = results.aic
                best_order = param
        except:
            continue
    # Build ARIMA model and inverse the log form
    model = ARIMA(data['Adj Close Log'], order=(best_order)).fit()
    log_forecasts = model.forecast(len(test)+5)
    forecasts = np.exp(log_forecasts)
    forecasts = forecasts.to_frame('forecasts')
    df = data.merge(forecasts, how='outer', left_index=True, right_index=True)

    # Plot Data, Forecast in plotly
    fig = go.Figure()

    # Add traces for each column (line for each stock)
    fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], mode='lines', name='Adj Close', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df.index, y=df['forecasts'], mode='lines', name='Forecasts', line=dict(color='green')))

    # Customize the layout
    fig.update_layout(title='Stock Price Forecast',
                      xaxis_title='Date',
                      yaxis_title='Price',
                      template='plotly_dark')


    # Plot the historical prices
    #fig1 = px.line(data, x=data.index, y=data['Adj Close'], title = ticker)
    st.plotly_chart(fig)
    
    
import pandas as pd
import numpy as np
import yfinance as yf

def industry(country):
    # Define the ticker symbols for the indices
    indices = {
        "France" : "^FCHI",
        "Germany" : "^GDAXI",
        "Spain" : "^IBEX"
    }

    # CAC 40 (^FCHI) index tickers
    cac40_tickers = ['AIR.PA', 'ALO.PA', 'ORA.PA', 'BNP.PA', 'EN.PA', 'VIE.PA', 'ENGI.PA', 'CA.PA', 
                     'BN.PA', 'ACA.PA', 'SGO.PA', 'LR.PA', 'RMS.PA', 'RI.PA', 'SAN.PA', 'AI.PA',
                     'CAP.PA', 'SU.PA', 'DSY.PA', 'EDF.PA', 'VIV.PA', 'KER.PA', 'MC.PA', 'MT.PA',
                     'OR.PA', 'PUB.PA', 'SAF.PA', 'STM.PA', 'FTI.PA', 'DG.PA', 'HO.PA', 'ML.PA',
                     'FR.PA', 'WLN.PA', 'CS.PA', 'FP.PA', 'TT.PA', 'SG.PA', 'URW.PA', 'VK.PA']

    # IBEX 35 (^IBEX) index tickers
    ibex35_tickers = ['ACX.MC', 'ACS.MC', 'AENA.MC', 'ALM.MC', 'AMS.MC', 'ANA.MC', 'BBVA.MC', 'BKT.MC',
                      'CABK.MC', 'CLNX.MC', 'COL.MC', 'ELE.MC', 'ENG.MC', 'FER.MC', 'GRF.MC', 'IAG.MC',
                      'IBE.MC', 'ITX.MC','MEL.MC', 'MTS.MC', 'NTGY.MC', 'PHM.MC', 'RED.MC', 'REP.MC', 'ROVI.MC',
                      'SAB.MC', 'SAN.MC', 'SGRE.MC', 'SLR.MC', 'TEF.MC']

    # DAX 40 (^DAX) index tickers
    dax40_tickers = ['ADS.DE','AIR.DE','ALV.DE', 'BAS.DE', 'BAYN.DE', 'BEI.DE', 'BMW.DE', 'CON.DE',
                     '1COV.DE', 'DHER.DE', 'DTE.DE', 'DPW.DE', 'DB1.DE', 'DBK.DE', 'ENR.DE', 'FRE.DE',   
                     'FME.DE', 'HEN3.DE', 'HNR1.DE', 'IFX.DE', 'LIN.DE', 'MRK.DE', 'MTX.DE', 'MUV2.DE',
                     'PUM.DE', 'RWE.DE', 'SAP.DE', 'SHL.DE', 'SIE.DE', 'VNA.DE', 'VOW3.DE', 'ZAL.DE',
                     'HEI.DE', 'BAYN.DE', 'SY1.DE', 'HFG.DE', 'MBG.DE', 'HLE.DE', 'BNR.DE', 'TYO.DE' ]
    
    # Define the ticker symbols for the indices
    indices_tickers = {
        "France" : cac40_tickers,
        "Germany" : ibex35_tickers,
        "Spain" : dax40_tickers
    }
    
    index_tickers = indices_tickers[country]

    # Create an empty list to hold company information
    company_data = []

    # Loop through each ticker and fetch the required data
    for ticker in index_tickers:
        stock = yf.Ticker(ticker)

        # Get the stock info for each company
        stock_info = stock.info

        # Extract relevant information
        company_name = stock_info.get('longName', 'N/A')  # Company Name
        industry = stock_info.get('industry', 'N/A')      # Industry
        market_cap = stock_info.get('marketCap', 'N/A')   # Market Capitalization

        # Append the data to the list
        company_data.append([ticker, company_name, industry, market_cap])

    # Create a DataFrame from the list
    df = pd.DataFrame(company_data, columns=['Ticker', 'Company Name', 'Industry', 'Market Cap'])

    df = df[df["Market Cap"]!="N/A"]
    df["Market Cap"] = pd.to_numeric(df["Market Cap"])
    df = df.sort_values(by="Market Cap", ascending=False)
    
    return df
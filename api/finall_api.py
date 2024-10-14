from flask import Flask, jsonify, request
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Data
stock_market_index = pd.read_csv('../data/stock_market_index.csv')
index_compositions = pd.read_csv('../data/index_compositions.csv')
company_details = pd.read_csv('../data/company_details.csv')
financial_statements = pd.read_csv('../data/financial_statements.csv')
daily_stock_price = pd.read_csv('../data/daily_stock_price.csv')

# Home route
@app.route('/')
def home():
    return """<html>
    <h1>Welcome to the FinAll API!</h1>
    <p> To use this FinAll API, please use the information below. </p>
    <h2>Base URL:</h2>
    <p>http://127.0.0.1:8080/</p>
    <h2>Description:</h2>
    <p>This API provides access to <b>five different datasets</b>. Each dataset can be accessed via specific endpoints. You can retrieve all data or filter it by specific fields.
    <h3>1. Stock Market Index</h3> 
    <p><b>/stock_market_index</b> : To retrieve all stock market index dataset</p>
    <h3>2. Index Compositions</h3>
    <p><b>/index_compositions</b> : To retrieve all index compositions dataset</p>
    <p><b>/index_compositions/{index}</b> : To retrieve index compositions dataset in a particular index (ie., CAC 40, DAX 40, IBEX 35)</p>
    <p>Note: In URLs, spaces are represented as %20. Therefore, type CAC%2040 in the url instead of CAC 40.</p>
    </html>
    <h3>3. Company details</h3>
    <p><b>/company_details</b> : To retrieve all company details dataset</p>
    <p><b>/company_details/{ticker}</b> : To retrieve a particular company details by stock symbol (ticker) (eg., MC.PA, ADS.DE)</p>
    <h3>4. Financial Statements</h3>
    <p><b>/financial_statements</b> : To retrieve all financial statements dataset</p>
    <p><b>/financial_statements/{ticker}</b> : To retrieve financial statements of a particular stock (ticker) (eg., MC.PA, ADS.DE)</p>
    <h3>5. Daily Stock Price</h3>
    <p><b>/daily_stock_price</b> : To retrieve all daily stock price dataset</p></p>
    <p><b>/daily_stock_price/{ticker}</b> : To retrieve daily stock price of a particular stock (ticker) (eg., MC.PA, ADS.DE)</p>
    
    
    </html>
    """

# Endpoint to get stock market index list
@app.route('/stock_market_index', methods=['GET'])
def get_data1():
    # Convert the DataFrame to a dictionary and return it as JSON
    return jsonify(stock_market_index.to_dict(orient='records'))

# Endpoint to get index compositions dataset
@app.route('/index_compositions', methods=['GET'])
def get_data2():
    # Convert the DataFrame to a dictionary and return it as JSON
    return jsonify(index_compositions.to_dict(orient='records'))

# Endpoint to get a specific index compositions dataset by index shortname
@app.route('/index_compositions/<Index_Shortname>', methods=['GET'])
def get_data2_by_index(Index_Shortname):
    # Filter the DataFrame by Index_Shortname
    result = index_compositions[index_compositions['Index_Shortname'] == Index_Shortname]
    
    # Check if the result is empty
    if result.empty:
        return jsonify({'error': 'Data not found'}), 404
    
    # Convert to dictionary and return as JSON
    return jsonify(result.to_dict(orient='records'))

# Endpoint to get company details dataset
@app.route('/company_details', methods=['GET'])
def get_data3():
    # Convert the DataFrame to a dictionary and return it as JSON
    return jsonify(company_details.to_dict(orient='records'))

# Endpoint to get a company details by ticker
@app.route('/company_details/<Ticker>', methods=['GET'])
def get_data3_by_ticker(Ticker):
    # Filter the DataFrame by Index_Shortname
    result = company_details[company_details['Ticker'] == Ticker]
    
    # Check if the result is empty
    if result.empty:
        return jsonify({'error': 'Data not found'}), 404
    
    # Convert to dictionary and return as JSON
    return jsonify(result.to_dict(orient='records'))

# Endpoint to get financial statements dataset
@app.route('/financial_statements', methods=['GET'])
def get_data4():
    # Convert the DataFrame to a dictionary and return it as JSON
    return jsonify(financial_statements.to_dict(orient='records'))

# Endpoint to get a specific financial_statements dataset by ticker
@app.route('/financial_statements/<Ticker>', methods=['GET'])
def get_data4_by_ticker(Ticker):
    # Filter the DataFrame by Index_Shortname
    result = financial_statements[financial_statements['Ticker'] == Ticker]
    
    # Check if the result is empty
    if result.empty:
        return jsonify({'error': 'Data not found'}), 404
    
    # Convert to dictionary and return as JSON
    return jsonify(result.to_dict(orient='records'))

# Endpoint to get daily stock price dataset
@app.route('/daily_stock_price', methods=['GET'])
def get_data5():
    # Convert the DataFrame to a dictionary and return it as JSON
    return jsonify(daily_stock_price.to_dict(orient='records'))

# Endpoint to get a specific daily_stock_price dataset by ticker
@app.route('/daily_stock_price/<Ticker>', methods=['GET'])
def get_data5_by_ticker(Ticker):
    # Filter the DataFrame by Index_Shortname
    result = daily_stock_price[daily_stock_price['Ticker'] == Ticker]
    
    # Check if the result is empty
    if result.empty:
        return jsonify({'error': 'Data not found'}), 404
    
    # Convert to dictionary and return as JSON
    return jsonify(result.to_dict(orient='records'))

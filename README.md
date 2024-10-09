# Stock Market Analysis Tool

This application offers a comprehensive tool for analyzing the stock market using both classical linear regression and a modern LSTM (Long Short-Term Memory) machine learning model. Users can fetch historical stock data and visualize predictions for future prices based on the company’s past performance.

## Features

- Data Collection
  Fetches stock price history for any given ticker from Yahoo Finance, covering periods from 1 day to 5 years.

- Stock Analysis
  **Linear Regression** : Uses Sklearn to analyze and predict future stock prices.
  **LSTM Prediction** : Employs TensorFlow to train LSTM models for advanced time-series forecasting.

- Visualizations: Utilizes Matplotlib to display historical stock prices and predictions.

- Live Search: Easily search for company tickers using live search functionality.
- User Interaction: Customers can either select a company from a database or enter the ticker manually to analyze stock data.

## Technologies Used

- Backend: Python Flask
- Frontend: JavaScript, HTML, CSS
- Libraries:

* Sklearn for linear regression analysis.
* TensorFlow for LSTM models.
* Pandas for data manipulation.
* Matplotlib for visualizations.
* YFinance for fetching stock data from Yahoo Finance.
* Tkinter for a GUI (in the desktop version).

## Installation

- 1 Clone the repository

  ```bash
  git clone https://github.com/your-repo-url
  cd stock-market-analysis
  ```

- 2 Install required dependencies:
  ` pip install -r requirements.txt`
  _Note: If you need to generate your own `requirements.txt`, use:_

```bash
pip freeze > requirements.txt
```

- 3 Run the Flask app:
  `flask run`

## Usage

- 1 Input a company name or ticker symbol to fetch stock data.
- 2 View and analyze historical data, using either linear regression or LSTM for future predictions.
- 3 Visualize results with detailed graphs and save them for further reference.

# BOOTSTRAP FOR FLASK

You do not need to install boostrap manually. here is flask version of bootstrap.

- 1 download and add package

```bash
pip install -U bootstrap-flask
```

- 2 added to `__init__.py` under app folder

```bash
from flask import Flask,render_template,request,jsonify,Response

from flask_bootstrap import Bootstrap5



def create_app():
    app=Flask(__name__,template_folder="templates")

    boostrap=Bootstrap5(app)


    from .routes import main
    app.register_blueprint(main)


    return app
```

- 3 added to header

```bash
<!--head for css and js -->
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{{ title }}</title>
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}" />
{{ bootstrap.load_css() }}

```

about_text="""
Stock Market Analysis Tool

This program offers a tool for analyzing the stock market using both classical linear regression and a modern LSTM (Long Short-Term Memory) machine learning model:

Imported Modules: The program employs various external libraries like:

tkinter for GUI creation.
matplotlib for plotting data.
pandas for data manipulation.
sklearn for linear regression.
yfinance to fetch stock data.
tensorflow for LSTM-based stock prediction.
PIL for image manipulation (probably used for company logos).
Data Collection:

fetch_data: Fetches the stock price history for a given ticker symbol for a specified period from Yahoo Finance. If the ticker does not exist or has been delisted, an error message is displayed.
Stock Price Analysis:

analyze_data: Uses simple linear regression to forecast the next day's closing price. It also computes the R-squared value (which indicates how well the model fits the data) and the F-statistic (to test the overall significance of the model).
LSTM-Based Stock Price Prediction:

train_lstm_model: This function uses an LSTM neural network model to predict the next day's closing price. The LSTM model is a type of recurrent neural network (RNN) popular for time-series data prediction.
GUI Functions:

on_lstm_analyze, on_analyze, and on_submit: These functions respond to GUI events to fetch data, analyze it, and display predictions or error messages.
plot_data and plot_last_month: These functions display stock price data over a year and the last month, respectively.
on_treeview_double_click: Reacts to a double-click event on a tree view (probably a list of companies) and fills an entry box with the selected company's name.
plot_placeholder: Plots a placeholder image/graph in a given frame.
show_historical_data: Displays a historical view of a stock's data over the past five years.
Additional Features:

display_logo: Although the function's implementation hasn't been provided, it's reasonable to assume from its usage that it displays the logo of a given company based on its ticker symbol.
exit_app: Closes the application.
save_option: Although the complete implementation isn't visible, it probably saves certain data or options based on the name and how it's being used.
Initialization:

A CSV file, companies.csv, containing company names and their ticker symbols is loaded at the start.
Usage:

Users can input a company name, and the program fetches and displays the company's stock data, predictions, and other relevant information.
It seems that users can view a list of companies, possibly select one, and then get detailed information about that company.
The GUI likely has sections for displaying linear regression and LSTM-based predictions, the latest stock data, company logos, and a couple of plots visualizing historical stock prices.
In summary, this is a comprehensive stock market analysis tool that lets users visualize historical stock prices, get statistical insights through linear regression, and predict future prices using LSTM.

2023 Devrim Savas Yilmaz
"""



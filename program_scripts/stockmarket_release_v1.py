
#import necessary modules 
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import font

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from scipy.stats import f
import numpy as np
import yfinance as yf
import requests
from PIL import Image,ImageTk
import os

#lstm analyzes
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
#about text
from about_stock_market_program import about_text
import io



#change link for back-end 
# Use the absolute path for the CSV file
csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'companies.csv')

# Load the CSV into a pandas DataFrame
df_companies = pd.read_csv(csv_path)

#collect data get company name and ticker from csv file and retrieve info from internet. 
def fetch_data(ticker, period): #period="1mo"
    try:
        stock = yf.Ticker(ticker)
        #test 
        company_info=stock.info
        print(company_info["address1"])
        
        
        
        data = stock.history(period=period)
        # Check if data is empty or contains a message about delisting
        if data.empty or "No data found, symbol may be delisted" in data.to_string():
            return {"error": f"No data found for {ticker}. The symbol may be delisted."}, pd.DataFrame()
        return None, data.reset_index()[['Date', 'Close']],company_info
    except Exception as e:
        return {"error": f"Failed to fetch data for {ticker}. Please check your connection or the symbol."}, pd.DataFrame()
    

##get some company information 
def get_company_summary(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_data = stock.info  # Get the company information from yfinance
        
        # Check if the data is empty
        if not stock_data:
            return None, {"error": f"No data found for {ticker}. The symbol may be delisted."}
        
        return stock_data, None  # Return the data and no error
    except Exception as e:
        return None, {"error": f"Failed to fetch data for {ticker}. Error: {str(e)}"}




#skilearn analyze: for whole data set 
def analyze_data(data,prediction_days):
    x = np.array(range(len(data))).reshape(-1, 1)  # Days since start
    y = data['Close'].values
    
    #fit linear regression
    reg = LinearRegression().fit(x, y)
    y_pred = reg.predict(x)
    mse = mean_squared_error(y, y_pred)
    
    n = len(data)
    p = 1  # We're using only one feature, i.e., the day
    
    r2 = reg.score(x, y)
    f_stat = (r2 / p) / ((1 - r2) / (n - p - 1))
    
    next_day = len(data)+prediction_days
    prediction = reg.predict([[next_day]])
    
    return prediction[0], r2, f_stat


#lstm machine learning model 

def train_lstm_model(data, window_size):
    # Transform data for LSTM
    data_lstm = data['Close'].values.reshape(-1, 1)
    
    # Normalize the dataset
    scaler = MinMaxScaler(feature_range=(0, 1))
    data_lstm = scaler.fit_transform(data_lstm)

    # Create a data structure with the specified window_size time-steps and 1 output
    X_train = []
    y_train = []
    for i in range(window_size, len(data_lstm)):
        X_train.append(data_lstm[i-window_size:i, 0])
        y_train.append(data_lstm[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

    # Set up the LSTM model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(tf.keras.layers.LSTM(units=50))
    model.add(tf.keras.layers.Dense(units=1))
    
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(X_train, y_train, epochs=50, batch_size=32)

    # Making prediction for next day
    inputs = data_lstm[len(data_lstm) - window_size:].reshape(-1, 1)
    inputs = scaler.transform(inputs)

    X_test = []
    for i in range(window_size, window_size + 1):
        X_test.append(inputs[i-window_size:i, 0])
    X_test = np.array(X_test)
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
    
    predicted_stock_price = model.predict(X_test)
    predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
    return predicted_stock_price[0][0]



def on_lstm_analyze():
    lstm_result_text.delete(1.0, tk.END)
    lstm_result_text.insert(tk.END, "Analyzing...")
    
    user_input = entry.get()
    matching_company = df_companies[df_companies['company_name'].str.contains(user_input, case=False)]
    
    window_size = int(lstm_window_spin.get())  # Get the selected window size (days)
    
    if not matching_company.empty:
        ticker = matching_company['ACT'].values[0]
        data = fetch_data(ticker)
        
        if not data.empty:
            prediction_lstm = train_lstm_model(data, window_size=window_size)
            
            lstm_result_text.delete(1.0, tk.END)
            lstm_result_text.insert(tk.END, f"Predicted stock price using LSTM for the next day: ${prediction_lstm:.2f}")
        else:
            lstm_result_text.delete(1.0, tk.END)
            lstm_result_text.insert(tk.END, "Failed to fetch data. Cannot predict with LSTM.")
    else:
        lstm_result_text.delete(1.0, tk.END)
        lstm_result_text.insert(tk.END, "Company not found. Cannot predict with LSTM.")


def on_analyze():
    user_input = entry.get()
    matching_company = df_companies[df_companies['company_name'].str.contains(user_input, case=False)]
    
    if not matching_company.empty:
        ticker = matching_company['ACT'].values[0]
        data = fetch_data(ticker)
        prediction, r2, f_stat = analyze_data(data) 
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Predicted stock price for the next day: ${prediction:.2f}")
        
        result_text.insert(tk.END, f"\n\nR-squared value: {r2:.4f}")
        if r2 > 0.7:
            result_text.insert(tk.END, "\nThe model explains a large portion of the variance in stock prices.")
        elif 0.5 <= r2 <= 0.7:
            result_text.insert(tk.END, "\nThe model explains a moderate portion of the variance in stock prices.")
        else:
            result_text.insert(tk.END, "\nThe model doesn't explain much of the variance in stock prices.")
        
        result_text.insert(tk.END, f"\n\nF-statistic: {f_stat:.4f}")
        if f_stat > 10:
            result_text.insert(tk.END, "\nThe model is likely a good fit for the data.")
        else:
            result_text.insert(tk.END, "\nThe model might not be a good fit for the data.")

        last_3_days = data.tail(3)['Close'].values
        result_text.insert(tk.END, f"\n\nLast 3 days' prices: {last_3_days[0]:.2f}, {last_3_days[1]:.2f}, {last_3_days[2]:.2f}")        
    


def on_submit():
    user_input = entry.get()
    matching_company = df_companies[df_companies['company_name'].str.contains(user_input, case=False)]
    
    if not matching_company.empty:
        company = matching_company['company_name'].values[0]
        ticker = matching_company['ACT'].values[0]
        data = fetch_data(ticker)
        plot_data(data)
        plot_last_month(data)
        
        company_text.delete(1.0, tk.END)
        company_text.insert(tk.END, f"Company Name: {company}\nTicker Symbol: {ticker}")
                    #try to get logo here
        display_logo(logo_canvas, ticker)


        # Extracting and displaying the latest date and its corresponding closing price
        if not data.empty:
            latest_date = data.iloc[-1]['Date'].strftime('%Y-%m-%d')  # formatting the date
            latest_close_price = data.iloc[-1]['Close']
            latest_data_text.delete(1.0, tk.END)
            latest_data_text.insert(tk.END, f"Latest Date: {latest_date}\nClosing Price: ${latest_close_price:.2f}")

def plot_data(data):
    for widget in frame_plot.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(data['Date'], data['Close'], label='Closing Price')
    ax.set_title("Stock Data Over a Year")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

def plot_last_month(data):
    for widget in frame_last_month_plot.winfo_children():
        widget.destroy()

    last_month_data = data.tail(30)  

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(last_month_data['Date'], last_month_data['Close'], label='Closing Price', color='blue')
    ax.set_title("Stock Data Over the Last Month")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=frame_last_month_plot)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)


#treeview function get info
def on_treeview_double_click(event):
    item = tree.selection()[0]  # Get the selected item
    company_name = tree.item(item, "values")[0]
    entry.delete(0, tk.END)  # Clear the entry
    entry.insert(0, company_name)  # Insert the company name into the entry

def plot_placeholder(frame, title="Placeholder"):
    for widget in frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.axis('off')  # Hide the axes
    ax.text(0.5, 0.5, title, ha='center', va='center',
            transform=ax.transAxes, fontsize=14, color='gray')
    
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

def show_historical_data():
    user_input = entry.get()
    matching_company = df_companies[df_companies['company_name'].str.contains(user_input, case=False)]
    
    if not matching_company.empty:
        ticker = matching_company['ACT'].values[0]
        
        # Fetch 5 years of data for the historical view
        data = fetch_data(ticker, period="5y") #5y can be changed for example period=10y

        
        if not data.empty:
            hist_window = tk.Toplevel(root)  # Creates a new window
            hist_window.title(f"Historical Data for {matching_company['company_name'].values[0]}")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data['Date'], data['Close'], label='Closing Price')
            ax.set_title("5-Year Historical Stock Data")
            ax.set_xlabel("Date")
            ax.set_ylabel("Price")
            ax.legend()

            canvas = FigureCanvasTkAgg(fig, master=hist_window)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
            
        else:
            messagebox.showerror("Error", "Failed to fetch historical data.")
    else:
        messagebox.showerror("Error", "Company not found. Cannot display historical data.")


def fetch_data_by_ticker():
    ticker = ticker_entry.get().strip().upper()
    if not ticker:
        messagebox.showerror("Error", "Please enter a valid ticker symbol.")
        return
    
    data = fetch_data(ticker)  # Using the existing fetch_data function

    plot_data(data)
    plot_last_month(data)

    # Since the company name and description might not be available, just display the ticker
    company_text.delete(1.0, tk.END)
    company_text.insert(tk.END, f"Ticker Symbol: {ticker}")

    if not data.empty:
        latest_date = data.iloc[-1]['Date'].strftime('%Y-%m-%d')
        latest_close_price = data.iloc[-1]['Close']
        latest_data_text.delete(1.0, tk.END)
        latest_data_text.insert(tk.END, f"Latest Date: {latest_date}\nClosing Price: ${latest_close_price:.2f}")


def fetch_data_and_description(ticker, period="1y"):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        if data.empty or "No data found, symbol may be delisted" in data.to_string():
            messagebox.showerror("Error", f"No data found for {ticker}. The symbol may be delisted.")
            return pd.DataFrame(), "Description not available."  # return an empty dataframe and default description

        description = stock.info.get("longBusinessSummary", "Description not available.")


        return data.reset_index()[['Date', 'Close']], description
    

    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch data for {ticker}. Please check your connection or the symbol.")
        return pd.DataFrame(), "Description not available."  # return an empty dataframe and default description


def exit_app():
    root.destroy()

def save_option():
    user_input = entry.get()
    matching_company = df_companies[df_companies['company_name'].str.contains(user_input, case=False)]
    
    if not matching_company.empty:
        company = matching_company['company_name'].values[0]
        ticker = matching_company['ACT'].values[0]
        data = fetch_data(ticker)
        
        if not data.empty:
            try:
                filename = f"{company}.csv"
                data.to_csv(filename, index=False)
                messagebox.showinfo("Info", f"Data saved successfully to {filename}")
            except:
                messagebox.showerror("Error", "Failed to save data to CSV.")
        else:
            messagebox.showerror("Error", "Failed to fetch data. Cannot save to CSV.")
    else:
        messagebox.showerror("Error", "Company not found. Cannot save data to CSV.")


def about_window():
    # Create a new top-level window
    about_win = tk.Toplevel(root)
    about_win.geometry("600x800")
    about_win.title("About")
    about_win.config(bg="lightgray")

    #since text is long i imported from other file
    info_text = tk.Text(about_win, height=30, width=70, wrap=tk.WORD, bg="lightgray", font=("Arial", 12))
    info_text.pack(padx=20, pady=20)
    info_text.insert(tk.END, about_text)
    info_text.config(state=tk.DISABLED)




def get_logo_url(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    website_url = stock.info.get("website", None)
    
    if website_url:
        domain = website_url.split("//")[-1].split("/")[0]
        logo_url = f"https://logo.clearbit.com/{domain}"
        return logo_url
    else:
        return None

def display_logo(canvas, ticker_symbol):
    try:
        logo_url = get_logo_url(ticker_symbol)
        if logo_url:
            response = requests.get(logo_url)
            if response.status_code == 200:
                logo = Image.open(io.BytesIO(response.content))
                logo = logo.resize((190, 190))
                logo_tk = ImageTk.PhotoImage(logo)
                canvas.image = logo_tk
                canvas.create_image(5, 5, anchor=tk.NW, image=logo_tk)
            else:
                canvas.create_text(100, 100, text="No logo found", fill="red", font=('Helvetica', 12, 'bold'))
        else:
            canvas.create_text(100, 100, text="No logo found", fill="red", font=('Helvetica', 12, 'bold'))
    except Exception as e:
        print("Error:", e)
        canvas.create_text(100, 100, text="Error loading logo", fill="red", font=('Helvetica', 12, 'bold'))


#TK GUI 

if __name__== "__main__":

    root = tk.Tk()
    root.geometry('1000x900')
    #root.iconbitmap("pro_icon.ico")
    root.title("Stock Data Viewer and Analyzer")
    root.config(bg="lightgray")
    root.state('zoomed')
    #colors
    # Change the background colors for frames
    frame_tree_bg_color = "#FFDAB9"  # Peach color
    frame_right_bg_color = "#B0E0E6"  # Powder blue
    frame_plot_bg_color = "lightgray"  #"#DDA0DD"  # Plum color
    frame_last_month_plot_bg_color = "#98FB98"  # Pale green

    #tree style
    style = ttk.Style()

    style.theme_use('clam') #preset styles: winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'). 



    frame_tree = tk.Frame(root)
    frame_tree.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10, expand=True)


    frame_tree.config(bg=frame_tree_bg_color)

    tree = ttk.Treeview(frame_tree, columns=('Company Name', 'Ticker Symbol'),style="Treeview")
    tree.heading('#0', text='')
    tree.heading('Company Name', text='Company Name')
    tree.heading('Ticker Symbol', text='Ticker Symbol')
    tree.column('#0', stretch=tk.NO, width=0)
    tree.column('Company Name', anchor=tk.W, width=150)
    tree.column('Ticker Symbol', anchor=tk.W, width=50)

    tree.bind("<Double-1>", on_treeview_double_click)

    # Create the Scrollbar
    scrollbar = tk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    #  Scrollbar with the Treeview
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)



    for _, row in df_companies.iterrows():
        tree.insert('', tk.END, values=(row['company_name'], row['ACT']))

    frame_right = tk.Frame(root,borderwidth=3)
    frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10, expand=True)

    frame_right.config(bg=frame_right_bg_color)


    label_entry = ttk.Label(frame_right, text="Enter Company Name:",font=("Arial",16),style=style.theme_use('clam'))
    label_entry.place(x=10,y=10)

    entry = ttk.Entry(frame_right, width=50,font=("Arial",14))

    entry.place(x=10,y=50)

    btn_submit = ttk.Button(frame_right, text="Submit", command=on_submit)

    btn_submit.place(x=10,y=90)

    company_text = tk.Text(frame_right, height=5, width=60,font=('Arial',12),bg="lightgray")

    company_text.place(x=10,y=140)

    btn_analyze = ttk.Button(frame_right, text="Analyze with sklearn", command=on_analyze)

    btn_analyze.place(x=10,y=240)

    #some differnt font
    large_font=font.Font(size=14)

    result_text = tk.Text(frame_right, height=16, width=50,font=large_font,bg="lightgray")

    result_text.place(x=10,y=280)

    #LSTM button and text
    btn_lstm=ttk.Button(frame_right,text="LSTM Model Prediction", command=on_lstm_analyze)
    btn_lstm.place(x=10, y=650)

    lstm_result_text=tk.Text(frame_right,height=16,width=50,font=large_font,bg="lightgray")
    lstm_result_text.place(x=10,y=680)


    frame_plot = tk.Frame(root)
    frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10, expand=True)
    plot_placeholder(frame_plot, "Yearly Stock Data will appear here")
    frame_plot.config(bg=frame_plot_bg_color)

    frame_last_month_plot = tk.Frame(root)
    frame_last_month_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=5, expand=True)
    frame_last_month_plot.config(bg=frame_last_month_plot_bg_color)
    plot_placeholder(frame_last_month_plot, "Last Month's Stock Data will appear here")



    #analyse day selector
    lstm_label=tk.Label(frame_right,text="Choose LSTM window size",font=("Arial",12))
    lstm_label.place(x=200,y=650)
    lstm_window_spin=tk.Spinbox(frame_right,from_=10, to=360, increment=1, width=5, font=("Arial",12))
    lstm_window_spin.place(x=410,y=650)

    #historical data button
    btn_hist=ttk.Button(frame_right,text="Show Historical Data",command=show_historical_data)
    btn_hist.place(x=10,y=1050)

    # New Text widget for displaying latest date and closing price
    latest_data_text = tk.Text(frame_right, height=2, width=30, font=large_font)
    latest_data_text.place(x=210, y=1050)  # Adjust y coordinate as needed to place the widget at a suitable location

    #manual ticker entry
    ticker_label=tk.Label(frame_right,text="Enter a Ticker Directly",bg="lightgray",font=("Arial",12))
    ticker_label.place(x=10,y=1120)
    ticker_entry=tk.Entry(frame_right,width=30)
    ticker_entry.place(x=10,y=1160)
    ticker_button=ttk.Button(frame_right,text="Data Using Ticker",command=fetch_data_by_ticker)
    ticker_button.place(x=10,y=1190)

    #menu bar
    # Creating the main menu bar
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    # Creating a 'File' menu and adding it to the menu bar
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)

    # Adding 'Save' and 'Exit' options to 'File' menu
    file_menu.add_command(label="Save", command=save_option)
    file_menu.add_command(label="Exit", command=exit_app)

    # Creating an 'About' menu and adding it to the menu bar
    about_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="About", menu=about_menu)

    # Add a command or text for the 'About' menu

    about_menu.add_command(label="About this App", command=about_window)

    #company logo if exits
    logo_canvas=tk.Canvas(frame_right,width=200,height=200)
    logo_canvas.place(x=210,y=1110)
    #display_logo(logo_canvas, "AAN")
    root.mainloop()

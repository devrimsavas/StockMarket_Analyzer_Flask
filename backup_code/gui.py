#TK GUI 

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

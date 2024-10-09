import base64
from io import BytesIO
import os

from flask import Blueprint,render_template, jsonify,request,url_for
from matplotlib.figure import Figure

#import functions from source program 
import sys 
#added program scripts folder 
script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'program_scripts'))
sys.path.append(script_path)

from program_scripts.stockmarket_release_v1 import fetch_data
from program_scripts.stockmarket_release_v1 import df_companies
from program_scripts.stockmarket_release_v1 import analyze_data
from program_scripts.stockmarket_release_v1 import get_logo_url
from program_scripts.stockmarket_release_v1 import train_lstm_model
from program_scripts.stockmarket_release_v1 import get_company_summary

main=Blueprint('main',__name__)


#need to define data to use in learning models 
data={}

@main.route('/') 
def index():
    title=""

    return render_template('index.html',title=title)



##post gets from front end and returns company time series

@main.route('/getcompanyinfo',methods=['GET','POST'])
def getcompanyinfo():

    if request.method=='GET':
        title="Company Stock Analysis and Future Prediction"
        tick=""
        allcompanies=df_companies.to_dict(orient='records')
        #print(allcompanies)
        highest_price=0 #data['Close'].max()
        lowest_price=0 #data['Close'].min()
        img_data_url = url_for('static', filename='img/generic_logo.jpg')  # Correct static image path
        
        return render_template('getcompanyinfo.html',title=title,tick=tick,allcompanies=allcompanies, highest_price=highest_price,lowest_price=lowest_price,company_logo_url=img_data_url)
    #POST 
    if request.method=='POST':
        
        data=request.get_json()
        tickinput=data.get('tickinput')
        periodinput=data.get('periodinput')
        print(f" ticker: ${tickinput } and  period input ${periodinput}")
        #return jsonify({'tickinput':tickinput, 'periodinput':periodinput})

        error,data,company_info=fetch_data(tickinput,periodinput) 
        if error:
            return jsonify({error:error["error"]})
        data_dict=data.to_dict(orient='records')
        dates = data['Date'].dt.strftime('%Y-%m-%d').tolist()  # Format dates
        closing_prices = data['Close'].tolist()

        ##try to get company logo 
        company_logo_url=get_logo_url(tickinput)
        print(f"company logo url ${company_logo_url}")

        #company info route debug
        print(f"****************+it is route side companyinfo ${company_info['address1']}")
        #all company info 
        #print(company_info)
        
        

        ##generate the Matplotlib figure 
        fig = Figure(figsize=(10,6))
        ax = fig.subplots()
        ax.plot(dates, closing_prices)
        ax.set_title(f'{tickinput} Stock Prices period: {periodinput}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price')
        ax.grid(False)

        # Save the figure to a BytesIO buffer
        buf = BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)

        # Encode the image as base64
        image_data = base64.b64encode(buf.getvalue()).decode('ascii')

        #calculate highest closing_prices in given period 
        highest_price=max(closing_prices)
        lowest_price=min(closing_prices)
        print (f"highest price-------- {highest_price} and lowest price {lowest_price} in given period {periodinput}")

        highest_price_index=closing_prices.index(highest_price)
        lowest_price_index=closing_prices.index(lowest_price)
        #get dates 
        highest_price_date = dates[highest_price_index]
        lowest_price_date = dates[lowest_price_index]

        print(lowest_price_date)


        return jsonify({'data':data_dict,
                        'dates':dates,
                        'closing_prices':closing_prices,
                        'image_data':image_data,
                        'tick':tickinput,
                        'highest_price': highest_price,
                        'lowest_price':lowest_price,
                        'highest_price_date':highest_price_date,
                        'lowest_price_date':lowest_price_date,
                        'company_logo_url':company_logo_url,
                        'company_info':company_info
                        })


@main.route('/skilearn',methods=['POST'])

def skilearn():


    
    data=request.get_json()
    tickinput=data.get("tickinput") 
    periodinput=data.get("periodinput")
    predictioninput=int(data.get("predictioninput")) 

    print(f"whole data from json  ${data}")

    #stock data 

    # it gets data from tick and time period
    error,stock_data,company_info=fetch_data(tickinput,periodinput)
    if error:
        return jsonify({"error":error["error"]}),400
    
    if stock_data.empty:
        return jsonify({"error":"No Stock data found"}),400 

    prediction,r2,f_stat=analyze_data(stock_data,predictioninput)

    print(f"------------back end tickinput ${tickinput} periodinput ${periodinput} data ${data}")
    #create data now 
    
    


    #sample json out 
    return jsonify({
        
        "tickinput":tickinput,
        "periodinput":periodinput,
        "prediction":prediction,
        "predictioninput":predictioninput,
        
        "r2":r2,
        "f_stat":f_stat
    })

@main.route('/lstmmodel',methods=["POST"])
def lstmmodel():
    # Get form data
    data = request.get_json()
    tickinput = data.get('tickinput')
    periodinput = data.get('periodinput')
    predictioninput = int(data.get("predictioninput"))
    
    # Get stock data
    error, stock_data,company_info = fetch_data(tickinput, periodinput)
    if error:
        return jsonify({"error": error["error"]}), 400
    
    # Validate that predictioninput is not greater than the length of available data
    if predictioninput > len(stock_data):
        return jsonify({"error": "Prediction window is too large for the available data"}), 400
    
    # Train LSTM model and get prediction
    predicted_stock_price = train_lstm_model(stock_data, predictioninput)

    # Convert float32 to Python float before returning it
    return jsonify({
        "tickinput": tickinput,
        "periodinput": periodinput,
        "predictioninput": predictioninput,
        "predicted_stock_price": float(predicted_stock_price)  # Convert here
    })




@main.route('/getsummary', methods=["POST"])
def getsummary():
    data = request.get_json()
    tickinput = data.get('tickinput')

    # Fetch company summary
    stock_data, error = get_company_summary(tickinput)
    
    if error:
        return jsonify(error), 400  # Return error if any

    # Return the stock_data dictionary directly as JSON
    ##print(stock_data['address1'])
    return jsonify({
        "data": stock_data
    })

    


@main.route('/searchcompany',methods=["POST"])
def searchcompany():
    #all data 
    data=request.get_json()
    searchinput=data.get('searchinput') # get search box 
    allcompanies=df_companies.to_dict(orient='records')

    if searchinput:
        filtered_companies=[
            company for company in allcompanies
            if searchinput in company['ACT'].lower() or searchinput in company['company_name'].lower()
        ]
    else:
        filtered_companies=allcompanies

    


    return jsonify({
        
        "allcompanies":filtered_companies
    })




@main.route('/samplepage2')
def samplepage2():
    title="Second Sample Page"
    #test for matplot 
    fig=Figure()
    ax=fig.subplots()
    ax.plot([1,2,3,4,6,1,12])
    #save it to temporary buffer
    buf=BytesIO()
    fig.savefig(buf,format="png")
    data=base64.b64encode(buf.getbuffer()).decode("ascii")
    

    return render_template('secondsamplepage.html',title=title,image_data=data)

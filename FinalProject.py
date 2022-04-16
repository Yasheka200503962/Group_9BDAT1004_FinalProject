from yaml import FlowMappingStartToken
from flask import Flask
from pymongo import MongoClient
import pymongo
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello Everyone"


def db_connection():
    con = "mongodb+srv://yasheka1996v:Bharath96@cluster0.fnqkv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    client = MongoClient(con)
    return client["PythonProject"]["Crypto"]
    
def get_all_data():
    cl = db_connection()
    data = cl.find({})
    return data

@app.route("/piechart")
def piechart():
    data = get_all_data()
    labels=[]
    values =[]
    for j in data:
        d=j["data"]
        for i in d:
            labels.append(i["name"])
            values.append(i["total_supply"])
    return render_template('piechart.html',labels = labels,values=values)

@app.route("/BarChart")
def PriceBarChart():
    data = get_all_data()
    labels=[]
    values =[]
    for j in data:
        d=j["data"]
        for i in d:
            labels.append(i["name"])
            values.append(i["quote"]["USD"]["price"])
    return render_template("PriceBarChart.html",labels=labels, values=values)

@app.route("/LineChart")
def LineChart():
    data = get_all_data()
    labels=["1 Hour","1 Day","7 Days","30 Days","60 Days","90 Days"]
    values =[]
    for j in data:
        d=j["data"][0]
        values =[d["quote"]["USD"]["percent_change_1h"],d["quote"]["USD"]["percent_change_24h"],d["quote"]["USD"]["percent_change_7d"],d["quote"]["USD"]["percent_change_30d"],d["quote"]["USD"]["percent_change_60d"],d["quote"]["USD"]["percent_change_90d"]]
        return render_template("linechart.html",labels=labels, values=values)

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)

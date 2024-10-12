from flask import Flask, render_template, request
from pymongo import MongoClient, server_api
app = Flask(__name__, static_url_path="", static_folder="static", template_folder="templates")
import datetime
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
import re

# set up mongodb database connection
mongo_host = os.getenv("MONGO_HOST")
db_name = os.getenv("MONGO_DBNAME")

client = MongoClient(mongo_host, server_api=server_api.ServerApi('1'))
client.admin.command('ping')
db = client[db_name]
requests_collection = db.requests
appliance_collection = db.appliances

appliance_collection.insert_one({'code': 1234, 'building':"CIWW", 'floor':2, 'applianceName':'Water Fountain'})

reports = ["Vending machine", "Water fountain", "Door hinge"]
fakeCodes = [{'code': 1234, 'building':"CIWW", 'floor':2, 'applianceName':'Water Fountain'}]

# Request logging
@app.before_request
def log_request_info():
    print("Request Method:", request.method)
    print("Request URL:", request.url)
    print("Request Headers:", request.headers)
    print("Request Data:", request.get_data())

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def list():
    return render_template("list.html", reports=reports)

@app.route("/request", methods=["GET", "POST"])
def makeRequest(code=None):
    entry = None
    if(request.method == 'GET'):
        # If code is not empty and is 4 numbers
        if ((code := request.args.get('code')) != '' and code is not None and re.match(r'^[0-9]{4}$', code)):
            code = int(code)
            # If code exists, retrieve data as entry and display it 
            entry = appliance_collection.find_one({'code': code})
        else:
            entry = None
    if(request.method == 'POST'):
        # If code is not empty and is 4 numbers
        pass

    return render_template("request.html", applianceInfo=entry)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
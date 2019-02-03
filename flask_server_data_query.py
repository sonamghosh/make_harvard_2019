import pymongo
from pymongo import MongoClient
from flask import Flask, request, send_file

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World"

# HTTP GET for last 20 seconds of heart rate data
@app.route("/getGood")
def getData():
    return send_file('output.txt')

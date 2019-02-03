import pymongo
import signal
import sys
import datetime
from pymongo import MongoClient
from flask import Flask, request, send_file
app = Flask(__name__)


# Setup MongoDB:
client = MongoClient()
db = client.heartrate
collection = db.user


def signal_handler(sig, frame):
    client.close()
    print("Exiting...")
    sys.exit(0)


@app.route("/")
def hello():
    write_to_file_path = "hrData.txt"
    output_file = open(write_to_file_path, "w+")
    data = collection.find({'time': {'$lt': datetime.datetime.now(), '$gt': datetime.datetime.now()- datetime.timedelta(seconds=20)}})
    totalData = ""
    for item in data:
        line = (str(item['hr1']) + " " + str(item['hr2']) + "\n")
        output_file.write(line)
        print(line)
        totalData += line
    print(totalData)
    output_file.close()
    return send_file('hrData.txt', as_attachment=True, attachment_filename='hrData.txt')


# HTTP GET for last 20 seconds of heart rate data
@app.route("/getGood")
def getData():
    return send_file('output.txt', as_attachment=True, attachment_filename='output.txt')

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
    write_to_file_path = "hrData.txt";
    output_file = open(write_to_file_path, "w+")
    data = collection.find({'time': {'$lt':datetime.datetime.now(), '$gt': datetime.datetime.now()- datetime.timedelta(seconds=20)}})
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

# Serve ARjs
@app.route("/arjs")
def arjs():
    return send_file('./ReactLiveChart/ARjs.html')

# Serve data
@app.route("/dat")
def data():
    read_file_path = "hrData.txt"
    giantDataDump = []
    with open(read_file_path, "r") as input_file:
        for index, line in enumerate(input_file):
            hr1 = float(line.split(' ')[0].rstrip())
            hr2 = float(line.split(' ')[1].rstrip())
            entry1 = {"x": index/10, "y": hr1, "z": 0, "size": 0.1, "color": "#ff0000"}
            entry2 = {"x": index/10, "y": hr2, "z": 0, "size": 0.1, "color": "#00ff00"}
            giantDataDump.append(entry1)
            giantDataDump.append(entry2)
            print(str(index/10) + " " + str(hr1) + " " + str(hr2))
    input_file.close()
    print("CLOSED INPUT FILE")
    write_to_file_path = "./ReactLiveChart/dat.json"
    output_file = open(write_to_file_path, "w+")
    print("OPENED OUTPUT FILE")
    print(str(giantDataDump))
    output_file.write(str(giantDataDump))
    print("Wrote TO OUTPUT FILE")
    output_file.close()
    return send_file('./ReactLiveChart/dat.json')

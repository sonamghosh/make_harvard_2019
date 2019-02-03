##############
## Halmon Lui
## Script listens to serial port and writes contents into a file
## Content also stored into MongoDB
##############
## requires pySerial to be installed
import serial
import pymongo
import signal
import sys
from datetime import datetime
from pymongo import MongoClient

# Setup MongoDB:
client = MongoClient()
db = client.heartrate
collection = db.user

# Setup Arduino port and baud rate
serial_port = 'COM8';
baud_rate = 250000; #In arduino, Serial.begin(baud_rate)
write_to_file_path = "output.txt";

output_file = open(write_to_file_path, "w+");
ser = serial.Serial(serial_port, baud_rate)

def signal_handler(sig, frame):
    client.close()
    print("Exiting...")
    sys.exit(0)

while True:
    line = ser.readline();
    line = line.decode("utf-8") #ser.readline returns a binary, convert to string
    print(line);
    if line:
        hr1 = float(line.split(',', 1)[0])  # maxsplit = 1;
        hr2 = float(line.split(',', 1)[1].rstrip()) # 2nd half of data, remove newline
        post = {"time": datetime.now(), "hr1": hr1, "hr2": hr2}
        confirmation = collection.insert_one(post).inserted_id
        print(confirmation)
        output_file.write(str(hr1) + " " + str(hr2) + "\n");

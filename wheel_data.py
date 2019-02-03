import urllib
import requests
import flask_server_data_query as fs
from pathlib import Path
import pickle
import wget

data = requests.get('http://carboi.serveo.net/getGood')
print(data)
print(data.content)


filename = wget.download('http://carboi.serveo.net/getGood')

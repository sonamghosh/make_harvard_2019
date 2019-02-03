import urllib
import requests
import flask_server_data_query as fs
from pathlib import Path
import pickle
import wget
import os

# Grabs Data
data = requests.get('http://carboi.serveo.net/getGood')
print(data)
print(data.content)

raw_dir = Path('dataset', 'driverheart', 'raw')
raw_dir.mkdir(parents=True, exist_ok=True)


# Downloads File
def get_data(save=True):
    if save:
        filename = wget.download('http://carboi.serveo.net/getGood')
        os.rename('./output.txt', './dataset/driverheart/raw/output.txt')
    else:
        pass

get_data(save=True)

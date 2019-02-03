import urllib
import requests
import flask_server_data_query as fs
from pathlib import Path
import pickle
import wget
import os
from shutil import unpack_archive

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

#get_data(save=True)

# Label Data
for filepath in raw_dir.glob('*.txt'):
    with open(str(filepath)) as f:
        labeled_data = []
        for i, line in enumerate(f):
            tokens = [float(token) for token in line.split()]
            if filepath.name == 'output.txt':
                if 817 < i < 842 or 1439 < i < 1470:
                    tokens.append(1.0)
                else:
                    tokens.append(0.0)
            else:
                pass
            labeled_data.append(tokens)
        # save dataset
        labeled_whole_dir = raw_dir.joinpath('labeled', 'whole')
        labeled_whole_dir.mkdir(parents=True, exist_ok=True)
        with open(str(labeled_whole_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
            pickle.dump(labeled_data, pkl)

        # training and test set
        labeled_train_dir = raw_dir.parent.joinpath('labeled', 'train')
        labeled_train_dir.mkdir(parents=True, exist_ok=True)
        labeled_test_dir = raw_dir.parent.joinpath('labeled', 'test')
        labeled_test_dir.mkdir(parents=True, exist_ok=True)

        if filepath.name == 'output.txt':
            with open(str(labeled_train_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
                pickle.dump(labeled_data[1500:3800], pkl)
            with open(str(labeled_test_dir.joinpath(filepath.name).with_suffix('.pkl')), 'wb') as pkl:
                pickle.dump(labeled_data[:1499], pkl)
                

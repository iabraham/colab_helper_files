import os, pickle
from pathlib import Path
from EMG import EMG


def load(f):
    with open(f, 'rb') as stream:
        instances = pickle.load(stream)
    return instances

subjects = [ "AS001", "AS002", "AS004", "AS005", "AS006", "AS007", "AS008",
             "AS009", "AS011", ]


files = ['pickles'/Path(x) for x in os.listdir("pickles") if x.split(".")[0] in
         subjects]

flatten = lambda t: [item for sublist in t for item in sublist]

all_data = flatten(load(f) for f in files)


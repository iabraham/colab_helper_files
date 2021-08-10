import os, pickle
from EMG import EMG
from numpy import hstack
from pathlib import Path
from functools import partial 
from func_helpers import pairwise, flatten


def make_stacked_instance(ramps_ofa_kind, slc):
    attribs = ["name", "side", "part", "activity"]
    data_attribs = ["time", "emgs", "forcemoments"]
    all_ramps = sorted(ramps_ofa_kind, key=lambda x:x.rampnum)[slc]
    inst = EMG(*[getattr(all_ramps[0], x) for x in attribs])
    inst.rampnum = str(slc)
    for d_attr in data_attribs:
        temp = hstack(map(partial(mgetattr, d_attr), all_ramps))
        setattr(inst, d_attr, temp)
    return inst


def pairwise_attribs(mx_inst):
    paired = [pairwise(getattr(mx_inst, da)) for da in D_ATTRIBS]
    return paired


def make_mxinstance(moves):
    ms1, _ = moves
    attribs = ["name", "side", "part"]
    s_moves = [sorted(item, key=lambda x:x.rampnum) for item in moves]
    inst = EMG(*[getattr(ms1[0], x) for x in attribs], "mixed")
    for d_attr in D_ATTRIBS:
        temp = [list(map(partial(mgetattr, d_attr), m)) for m in s_moves]
        weaved = list(zip(*temp))
        setattr(inst, d_attr, weaved)
    return inst


def load(f):
    with open(f, 'rb') as stream:
        instances = pickle.load(stream)
    return instances


mgetattr = lambda x,y: getattr(y,x)
D_ATTRIBS = ["time", "emgs", "forcemoments"]
subjects = [ "AS001", "AS002", "AS004", "AS005", "AS006", "AS007", "AS008",
             "AS009", "AS011", ]

files = ['pickles'/Path(x) for x in os.listdir("pickles") if x.split(".")[0] in
         subjects]

all_data = flatten(load(f) for f in files)


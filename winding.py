import pandas as pd
import numpy as np
from io import StringIO


def read_cam_orientation(folder):
    readint = lambda x : int(x) if x!='None' else 0
    with open(folder/'cameraOrientationInfo.txt') as stream:
        content = [x.strip() for x in stream.readlines()]

    return {x.split(":")[0].upper(): readint(x.split(':')[1]) for x in content}


def read_pos_ascii(folder):
    df = pd.read_csv(folder/"Pos.p.ascii", names=["Timestamp", "X", "Y", "D"],
                 index_col="Timestamp")
    idx_start, idx_stop = np.loadtxt(folder/"sessionEpochInfo.txt",
                                     dtype=np.int64, delimiter=',')
    start = df.index.get_loc(idx_start, method='nearest')
    stop = df.index.get_loc(idx_stop, method='nearest')

    return df[start:stop]


def pre_process(folder):
    corrections = read_cam_orientation(folder)
    df = read_pos_ascii(folder)

    for k, v in corrections.items():
        if v != 0:
            df.loc[:, k] = v - df[k]

    valid = df[(0 < df['X']) & (df['X'] < 640) &\
               (0 < df['Y']) & (df['Y'] < 480)]

    return valid


def get_centers(R859):
    centers = list()
    for block in R859.cityBlocks:
        start, *rest = block
        _, *dimensions = np.unique(np.abs(np.diff(rest, axis=0)))
        centers.append(start + np.asarray(dimensions)/2)

    return centers


def sign_to_node(row):
    mapper = {(1.0, 1.0) : "A", (-1.0, 1.0) : "B"}
    return mapper.get((row.X, row.Y), "C")


def read_cl(filepath):
    
    with open(filepath) as stream:
        lines = [x.strip() for x in stream.readlines()]
    
    header = lines[8].split(",")
    idx_start, idx_stop = map(int, lines[11:13])
    
    df = pd.read_csv(StringIO("\n".join(lines[13:])), names=header, index_col="Timestamp")
    start = df.index.get_loc(idx_start, method='nearest')
    stop = df.index.get_loc(idx_stop, method='nearest')

    return df[start:stop]

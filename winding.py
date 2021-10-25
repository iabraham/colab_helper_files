import pandas as pd
import numpy as np
from io import StringIO
from collections import deque
import pudb


def read_cam_orientation(folder):
    """Open a Path() with data in it and read the camera orientation data."""

    readint = lambda x : int(x) if x!='None' else 0
    with open(folder/'cameraOrientationInfo.txt') as stream:
        content = [x.strip() for x in stream.readlines()]

    return {x.split(":")[0].upper(): readint(x.split(':')[1]) for x in content}


def read_pos_ascii(folder):
    """Open a Path() with data in it and read the position ascii file."""

    df = pd.read_csv(folder/"Pos.p.ascii", names=["Timestamp", "X", "Y", "D"],
                 index_col="Timestamp")
    idx_start, idx_stop = np.loadtxt(folder/"sessionEpochInfo.txt",
                                     dtype=np.int64, delimiter=',')
    start = df.index.get_loc(idx_start, method='nearest')
    stop = df.index.get_loc(idx_stop, method='nearest')

    return df[start:stop]


def pre_process(folder):
    """Open a Path() with data in it and read camera/position data"""
    corrections = read_cam_orientation(folder)
    df = read_pos_ascii(folder)

    for k, v in corrections.items():
        if v != 0:
            df.loc[:, k] = v - df[k]

    valid = df[(0 < df['X']) & (df['X'] < 640) &\
               (0 < df['Y']) & (df['Y'] < 480)]

    return valid


def get_centers(R859):
    """ Get the center/centroid location for each of the cityblocks in maze"""
    centers = list()
    for block in R859.cityBlocks:
        start, *rest = block
        _, *dimensions = np.unique(np.abs(np.diff(rest, axis=0)))
        centers.append(start + np.asarray(dimensions)/2)

    return centers


def sign_to_node(row):
    "Map quadrant to node"""
    mapper = {(1.0, 1.0) : "A", (-1.0, 1.0) : "B"}
    return mapper.get((row.X, row.Y), "C")


def read_cl(filepath):
    """Read a CSV file for data, especially Pos.p.ascii file."""
    
    with open(filepath) as stream:
        lines = [x.strip() for x in stream.readlines()]
    
    header = lines[8].split(",")
    idx_start, idx_stop = map(int, lines[11:13])
    
    df = pd.read_csv(StringIO("\n".join(lines[13:])), names=header, 
                     index_col="Timestamp")
    start = df.index.get_loc(idx_start, method='nearest')
    stop = df.index.get_loc(idx_stop, method='nearest')

    return df[start:stop]


# def pop_until(dq, elem):
#     """Pop elements from a deque object until elem is seen"""
#     while dq[-1] != elem:
#         yield dq.pop()


def split(sequence, sep, key=lambda x: x):
    """ Split a list based on a seperator like str.split()"""
    chunk = []
    for val in sequence:
        if key(val) == sep:
            yield chunk
            chunk = []
        else:
            chunk.append(val)
    yield chunk


def is_rotation(s1, s2):
    """Check if one string is a rotation of the other."""
    return len(s1)==len(s2) and s1 in 2*s2


def is_same_loop(l1, l2):
    """Check if two loops are the same"""
    return is_rotation(l1[:-1], l2[:-1])


node = lambda x: x[1]
class itaDeque(deque):
    """Modifies collections.deque for our use/"""

    def __init__(self, *args):
        super(itaDeque, self).__init__(*args)

    def pop_until(self, elem):
        while node(self[-1]) != elem:
            yield self.pop()

    def __contains__(self, elem):
        return elem in [node(x) for x in self]


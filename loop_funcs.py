import numpy as np 
import pandas as pd
import networkx as nx 
from functools import partial
import matplotlib.pyplot as plt
import matplotlib.gridspec as gs
from string import ascii_uppercase
from func_helpers import pairwise, flatten
from collections import defaultdict, Counter
from winding import split, itaDeque, is_same_loop


def triplewise(iterable):
    "Return overlapping triplets from an iterable"
    # triplewise('ABCDEFG') -> ABC BCD CDE DEF EFG
    for (a, _), (b, c) in pairwise(pairwise(iterable)):
        yield a, b, c


def get_direction(node_pos, loop):
    val = 0.0
    while val==0.0:
        for triplet in triplewise(loop):
            x, y = zip(*[node_pos[n] for n in triplet])
            arr = np.asarray([[1,1,1], x, y]).T
            val = np.linalg.det(arr)
            if val != 0.0:
                break

    return ('X' if val > 0 else 'C')


def walk_path(path):
    """ Walk a path and count loops encountered. """
    dq, loops = itaDeque(), defaultdict(list)
    for time, node in path:
        if node in dq:
            _, body = zip(*dq.pop_until(node))
            loop = node + "".join(reversed(body)) + node
            loops[loop] += [(dq[-1][0], time)]
            _ = dq.pop()
        dq.append((time, node))

    return loops

def get_path_string(timepath):
    return reversed(list(map(lambda x:x[1], timepath)))

def retraces_in_path(path):
    """ Walk a path and count retraces encountered. """
    dq, flag = itaDeque(), False
    flag, retrace, retraces = False, list(), list()

    for time, node in path:
        if node in dq and node in dq[-2]:
            flag = True 
            retrace.append(dq.pop())
        else:
            if flag:
                retrace.append(dq.pop())
                retraces.append("".join(get_path_string(retrace)))
                retrace, flag = [], False
            dq.append((time, node))

    return Counter(retraces)


def visualize_loop(loop, node_pos, weight=1.0, ax = None):
    """Visualize a loop in a (3,4) grid graph"""

    if ax is None:
        fig, ax = plt.subplots(111)

    gg = nx.grid_2d_graph(3, 4, create_using=nx.DiGraph)
    mapper = dict(zip(gg.nodes, list(ascii_uppercase[:12])))
    graph = nx.create_empty_copy(nx.relabel_nodes(gg, mapper))
    graph.add_edges_from(pairwise(list(loop)))
    nx.draw_networkx_nodes(graph, pos=node_pos, ax=ax)
    nx.draw_networkx_labels(graph, node_pos, ax=ax, font_color="white")
    nx.draw_networkx_edges(graph, node_pos, ax=ax, width=weight)

    return ax


def plot_walks(graph, node_pos, edges, weights, ax):
    """Function to plot a nx graph really. """
    nx.draw_networkx_nodes(graph, ax=ax, pos=node_pos)
    nx.draw_networkx_labels(graph, node_pos, ax=ax, font_color='white')
    nx.draw_networkx_edges(graph, ax=ax, pos=node_pos, edgelist=edges, 
                         width=weights)
    ax.set_aspect('equal')
    return ax

def eliminate_trivials(loops_list):
    """Given a bunch of loops and (start, stop) intervals, eliminate the 
       trivial loops and coalesce the rotated ones; while preserving the
       individual start and stop times"""

    nontrivials = dict()
    for loops in loops_list:
        feasible = {loop:times for loop, times in loops.items() if len(loop)>3}
        for loop, times in feasible.items():
            if loop in nontrivials:
                nontrivials[loop] += times 
            elif any(map(partial(is_same_loop, loop), nontrivials.keys())):
                key, = [k for k in nontrivials.keys() if is_same_loop(k, loop)]
                nontrivials[key] += times
            else:
                nontrivials[loop] = times

    return nontrivials

# %% More helper functions

def make_paths(df):
    """Generate contigous walks on graph from the given CSV/dataframe"""

    # For each intersection associate timestamp 
    times = df['Ts exit'] + (df['Ts entry'] - df['Ts exit'])/2
    *temp, = zip(times.tolist(), df['Inter'].tolist())
    
    # Get intersections the rat visits, eliminating repeats
    times_nodes = [(time,node) for i, (time,node) in enumerate(temp) 
                   if i==0 or node!=temp[i-1][1]]
    
    # Split whenever localization is lost and ignore trivial splits
    all_sub_walks = [x for x in split(times_nodes, '0', key=lambda x:x[1])]
    *sub_walks, = filter(lambda x: len(x)>3, all_sub_walks)

    return sub_walks

def make_plot_params(ntvs):
    """ Helper function to plot loops/cumulative counts etc.""" 

    ntv_count = Counter({k:len(v) for k,v in ntvs.items()})
    major = {k: v for k, v in ntv_count.most_common() if v > 1}
    
    sqrt_nax = np.sqrt(sum(1 for _ in major.items()))
    rounded = int(np.round(sqrt_nax))
    M, N = [rounded]*2
    N = (N + 1) if rounded < sqrt_nax else N
    idxs = [(i,j) for i in range(M) for j in range(N)]
    major = Counter(major)
    max_weight = sum(c for _,c in major.most_common())

    return (M, N), idxs, major, max_weight


def pad_array(arr, estart, efinish, scale=True):
    """Pad with a beginning and ending for intervals wrt
       session epoch data"""
    b, e = arr[0,0], arr[-1, -1]
    beginning = [0, 0.99999*b ], 
    if scale:
        ending = [1.0001*e,  (efinish-estart)/6e7]
    else:
        ending = [1.0001*e,  efinish-estart]
    return np.vstack((beginning, arr, ending))


def adjust_times(times, estart, efinish):
    """Adjust time data to pad it as well as to make it in minutes"""
    raw_times = (np.asarray(sorted(times, key=lambda x:x[0]))-estart)
    adj_times = raw_times / 6e7
    aug_times = pad_array(adj_times, estart, efinish)

    genlist = [0] + list(range(len(adj_times)+1)) + [len(adj_times)]
    yvals = flatten(list(pairwise(genlist)))

    return raw_times, adj_times, (aug_times.flatten(), yvals)

def make_figs_grids(rowcols, size):
    """Auxiliary function, nothing special"""
    m, _ = size
    figs = [plt.figure(figsize=size, constrained_layout=True) for _ in range(3)]
    grids = [gs.GridSpec(*rowcols, figure=fig) for fig in figs]
    figs.append(plt.figure(figsize=(m , m/3), constrained_layout=True))

    return figs, grids

def read_files(name, csv):
    """Read the turns csv file and the corresponding session epoch data"""
    turn_df = pd.read_csv(csv)
    
    with open("/".join([".", name, "sessionEpochInfo.txt"])) as stream:
        *sessionEpoch, = map(int, stream.readline().split(","))

    return turn_df, sessionEpoch

def perturb_times(times):
    newtimes = []
    for i1, i2 in pairwise(times):
        if i1[1] == i2[0]:
            adder = [i1[0], i1[1]*0.999]
        else:
            adder = i1
        newtimes.extend(adder)
    
    newtimes.extend(i2)
    return newtimes

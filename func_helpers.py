import requests
import numpy as np
from heapq import merge
from functools import partial
from scipy.signal import find_peaks
from itertools import combinations, tee, groupby


def gaussian(x, mu, b=0, k=1):
    """Evaluate a unit variance gaussian with mean k*mu with noise b*rand().

    Parameters
    ----------
    x
        Plotting or evaluation variable
    mu
        Fundamental mean value
    b
        Spread of random noise around the mean value
    k
        Higher offsets of mean value
    """
    randval = np.random.rand()
    return (mu, b, k, randval), np.exp(-(x-mu*k+b*randval)**2/2)


def sensed_gaussian(x, params, dist):
    """Evaluate a unit variance gaussian with mean k*mu with noise b*rand().

    Parameters
    ----------
    params
        A tuple consisting of mu, b, k from the gaussian method that generated
        the pulse
    dist
        Distance of the sensor node from source node
    """
    mu, b, k, randval = params
    return np.exp(-(x-dist-mu*k+b*randval)**2/2)


def find_nearest(array, value):
    """Find the element in 1-D array that is closest to value.

    Parameters
    ----------
    array
        A 1-D numpy array
    value
        The value to look for in array
    """
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


def flatten(regular_list):
    """Flattens a list using list comprehensions.

    Parameters
    ----------
    regular_list:
        A singly nested list to flatten.
    """
    return [item for sublist in regular_list for item in sublist]


def download_file_from_google_drive(id, destination):
    """Download a drive from Google Drive give id from shareable link.

    Parameters
    ----------
    id:
        The file identifier from a shareable link
    destination:
        The filename to save as on local disk
    """
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    """ Function to filter out some Cookie business from Google and
        extract the actual data

    Parameters
    ----------
    response:
        The return value from a requests GET request
    """
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    """ Function to open write the proper response content from a
        requests GET response to local disk.

    Parameters
    ----------
    response:
        The filtered return value from a requests GET request
    destination:
        A filename or file object denoting where to save file on
        local disk
    """
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


def intify(arr):
    """Convert array into list of ints excepting nans in array.

    Parameters
    ----------
    arr:
        array to intify
    """
    return list(map(lambda x: x if np.isnan(x) else int(x), arr))


def zero_all_but(arr, n):
    """Zero out everything in an array except the value "n".

    Parameters
    ----------
    arr:
        array to modify
    n:
        value to leave unchanged.
    """
    return list(map(lambda z: z if z == n else 0, arr))


def prune(x, y):
    """Given two (possibly repeating) time stamped sequences 'prune' them.

    Parameters
    ----------
    x
        A tuple of (timestamps, data)
    y
        A tuple of (timestamps, data)
    """
    # Tag them so we know who-is-who after merge
    *xbar, = zip(*x, np.ones(len(x[0])))
    *ybar, = zip(*y, -np.ones(len(y[0])))

    # Merge/sort-merge them
    times, mixed_seq, labels = zip(*merge(xbar, ybar, key=lambda x: x[0]))
    *seperated_labels, = map(partial(zero_all_but, labels), [1, -1])

    # Detect repeats and changes
    changes = np.abs(np.diff(labels, append=labels[-1]))/2
    *seperation_masks, = map(partial(np.multiply, changes), seperated_labels)
    *mixed_seq_idxs, = map(np.nonzero, seperation_masks)

    # Extract pruned version
    xvals, yvals = map(lambda z: np.asarray(mixed_seq)[z], mixed_seq_idxs)
    N = min(map(len, [xvals, yvals]))

    return xvals[:N], yvals[:N]


def make_pairs(data):
    """Make pruned pairs from a list of data."""
    return [prune(*pair) for j, pair in enumerate(combinations(data, 2))]


def pairwise(iterable):
    """Iterate over an iterable two elements at a time."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def moving_average(n, x):
    """ Calculate the n-point moving averge along x."""
    return np.convolve(x, np.ones(n), 'valid') / n


def splitvec(vec):
    """Split an integer vector at points of discontinuity"""
    return [[next(v)] + list(v)[-1:]
            for k,v in groupby(vec, lambda x,c=count(): x-next(c))]


def largest_contigous(arr, op, horz=True):
    """ Return largest/longest increasing/decreasing contigous sequence in
        array."""

    zeros = np.where(op(np.diff(arr),0))
    x_split = np.asarray([x for x in splitvec(zeros[0]) if len(x)>1])
    x_lens = np.asarray(list(map(np.ptp, x_split)))
    x_biggest = x_split[x_lens.argmax()]

    y_lens = np.asarray(list(map(np.ptp, [arr[s] for s in x_split])))
    y_biggest = x_split[y_lens.argmax()]

    if horz:
        return x_biggest, arr[slice(*x_biggest)]
    else:
        return y_biggest, arr[slice(*y_biggest)]

    
def clean_ramps(arr, peak_locs, mod, op):
    """Function to iterate over peaks identified in an array
    and clean them up.
    """

    onsets = []
    for prev, curr in pairwise(np.hstack((1,peak_locs))):
        search = -1*mod*arr[prev:curr]
        start, _ = find_peaks(search, height=min(search) + 0.7*np.ptp(search))
        onsetQ = start[-1] + prev
        idx, _ = largest_contigous(arr[onsetQ:curr], op=op, horz=True)
        onsets.append(idx+onsetQ)

    return onsets

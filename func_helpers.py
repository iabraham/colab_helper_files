import numpy as np


def gaussian(x, mu, b=0, k=1):
    """Evaluate a unit variance gaussian with mean k*mu with 
       random noise b*rand()

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
    """Evaluate a unit variance gaussian with mean k*mu with 
       random noise b*rand()

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
    """ Find the element in 1-D array that is closest to value.

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


import numpy as np
import scipy as sp
from random import random
from functools import partial

def ou_process(mu, sigma, theta, T, N, x0=None):
    """Simulate the Ornstein-Uhlenbeck process. 

    Parameters
    ----------
    mu, sigma, theta
        The usual suspects
    T
        The time to simulate until
    N 
        The number of steps to take.
    x0
        Initial condition optional 
    """ 

    t = np.linspace(0, T, N)
    dt = np.mean(np.diff(t))
    x = np.zeros(N)

    if x0 is None:
        x[0] = np.random.normal(loc=0.0, scale=1.0)
    else:
        x[0] = x0

    drift = lambda x, t: theta * (mu - x)
    diffusion = lambda x, t: sigma
    d_wiener = np.random.normal(loc=0.0, scale=np.sqrt(dt), size=N)

    for i in range(1, N):
        x[i] = x[i-1] + drift(x[i-1], i*dt)*dt + \
                diffusion(x[i-1], i*dt) * d_wiener[i]

    return t, x


def gbm(mu, sigma, T, N, x0=None):
    """ Simulate the Geometric Brownian Motion 

    Parameters
    ----------
    mu, sigma
        The usual suspects
    T
        The time to simulate until
    N 
        The number of steps to take.
    x0
        Initial condition optional 
    """ 

    t = np.linspace(0, T, N)
    dt = np.mean(np.diff(t))
    x = np.zeros(N)

    if x0 is None:
        x[0] = np.random.normal(loc=0.0, scale=1.0)
    else:
        x[0] = x0

    drift = lambda x, t : mu * x
    diffusion = lambda x, t: sigma * x
    d_wiener = np.random.normal(loc=0.0, scale=1, size=N) *np.sqrt(dt)

    for i in range(1, N):
        x[i] = x[i-1] + drift(x[i-1], i*dt)*dt + \
                diffusion(x[i-1], i*dt) * d_wiener[i]

    return t, x


def multiplex(N, empty_model, integer=False):
    time_series = list()
    for i in range(N):
        if integer:
            x0 = np.random.randint(33)
        else:
            x0 = np.random.rand()
        mu = np.random.rand()
        sigma = abs(np.random.rand())
        partial_model = partial(empty_model, mu=mu, sigma=sigma, x0=x0)
        _, val = partial_model()
        time_series.append(val)
    return time_series


def brownian(x0, N, T, delta):
    """ Generate Brownian motion"""

    # Calculate time step and make sure x0 is array
    dt = T / N
    x0 = np.asarray(x0)

    # For each element of x0, generate a sample of n numbers from a
    # normal distribution.
    r = norm.rvs(size=x0.shape + (N,), scale=delta * np.sqrt(dt))
    out = np.empty(r.shape)

    # This computes the Brownian motion by forming the cumulative
    # sum of the random samples
    np.cumsum(r, axis=-1, out=out)
    out += np.expand_dims(x0, axis=-1)

    return out


def make_random_walk(N, init=None):
    """ Simulate a random walk. 

    Parameters
    ----------
    N
        Number of steps
    init
        Initial condition 

    """
    random_walk = list()
    if init is None:
        random_walk.append(-1 if random() < 0.5 else 1)
    else:
        random_walk.append(int(init))

    for i in range(1, N):
        movement = -1 if random() < 0.5 else 1
        value = random_walk[i - 1] + movement
        random_walk.append(value)

    return random_walk


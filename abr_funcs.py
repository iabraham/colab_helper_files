from collections import deque
import numpy as np

def fm(series):
    """ function fm computes the 0-persistence with output lines
    [local min value, local min position, local max value, local max position,
    where recorded] for each bar"""

    # find max
    mx=np.max(series)

    # make the time series well-like, ending with a bang
    tser=np.concatenate(([np.inf, mx+10], series, [mx+10, np.inf]))

    # here we'll store bars and two stacks, for minima and maxima
    pers, stackn, stackx =[deque() for _ in range(3)]

    # initially, the time series is function decreasing
    up=-1
    for pos, tp in enumerate(tser[:-1]):
        if (up>0)&(len(stackx)>0):
            for _ in range(sum(map(lambda x: x[0]<=tp, stackx))):
                pers.append([*stackn.pop(), *stackx.pop(), pos])
        if (up<0)&(len(stackn)>0):
            for _ in range(sum(map(lambda x: x[0]>=tp, stackn))):
                pers.append([*stackn.pop(), *stackx.pop(), pos])
        if (up*(tser[pos+1]-tp)<0):
            if (up>0):
                #Recall we prepended 2 elements so shift pos by 2
                stackx.append([tser[pos], pos-2])
            else:
                stackn.append([tser[pos], pos-2])
            up=-up
    
    # Pair the leftover global minimum with a nan/inf etc. 
    # nan preferred so we can use np.nanmax or np.nanmin later
    pers.append([*stackn.pop(), np.nan, 0, pos-1])
    
    return pers


def get_n_farthest(N, output):
    """Get N points farthest from the diagonal in the PD"""
    b, _, d, *_ = zip(*output)
    bmin, dmax = np.nanmin(b), np.nanmax(d)
    vals = [area_triangle([bmin]*2, [dmax]*2, p) for p in zip(b,d)]

    # Since bmin, dmax are fixed, area of triangle maximized for
    # points furthest from the diagonal 

    ind = np.argpartition(np.asarray(vals), -N)[-N:]

    return [output[i] for i in ind]



def area_triangle(a, b, p):
    """Computes the area of the triangle formed by points a, b and p"""
    (xp, xb, xp), (ya, yb, yp) = zip(a, b, p)
    return (1/2)* abs((xp - xp)*(yb - ya) - (xp - xb)*(yp - ya))

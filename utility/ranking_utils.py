import pandas as pd
from scipy.stats import norm
import numpy as np


def multirank(df, highisgood=[], lowisgood=[], axis=0):
    hlist = list(highisgood)
    llist = list(lowisgood)

    if axis == 1:
        hrank = df.loc[hlist].rank(axis=axis, ascending=False)
        lrank = df.loc[llist].rank(axis=axis, ascending=True)
    else:
        hrank = df[hlist].rank(axis=axis, ascending=False)
        lrank = df[llist].rank(axis=axis, ascending=True)

    rank = pd.concat([hrank, lrank])
    return rank.sum(axis=1-axis).rank(ascending=True)


# Bad Math :)
def vect_2_zquantiles(vect, n=5, mean=None, std=None):
    mean = vect.mean() if mean is None else mean
    std = vect.std() if std is None else std
    bins = np.linspace(0, 1, n + 1)[1:]
    return np.digitize(norm.cdf((vect - mean) / std), bins, right=True) + 1
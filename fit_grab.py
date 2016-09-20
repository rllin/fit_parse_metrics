from collections import defaultdict
import numpy as np
from fitparse import FitFile


def nan_helper(y):
    """Helper to handle indices and logical indices of NaNs.

    Input:
        - y, 1d numpy array with possible NaNs
    Output:
        - nans, logical indices of NaNs
        - index, a function, with signature indices= index(logical_indices),
          to convert logical indices of NaNs to 'equivalent' indices
    Example:
        >>> # linear interpolation of NaNs
        >>> nans, x= nan_helper(y)
        >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
    """
    #y = np.array(y, dtype=np.float)
    y = np.array(map(lambda x: np.nan if type(x) == str or x == None else x, y))
    return y, np.isnan(y), lambda z: z.nonzero()[0]

def grab_data(filename, target_units=[]):
    fitfile = FitFile(filename)
    results = defaultdict(list)
    for record in fitfile.get_messages('record'):
        for record_data in record:
            if len(target_units) > 0 and record_data.name not in target_units:
                continue
            results[record_data.name].append(record_data.value)
    return results

def interpolate_data(y):
    y, nans, x = nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    return y

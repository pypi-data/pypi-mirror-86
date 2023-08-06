#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


def extend1D(arr, direction, exlen=0):
    """ Extend array along one direction in 1D.

    **Parameters**\n
    arr: 1D array
        Array for extension.
    direction: str
        Direction to extend array.
    exlen: int | 0
        Length of extension.
    """

    exlen = int(exlen)

    if exlen >= 1:
        if direction == 'after':
            edge_spacing = arr[-1] - arr[-2]
            end = arr[-1] + exlen*edge_spacing
            ext = np.arange(arr[-1], end+edge_spacing, edge_spacing)
            arrext = np.concatenate((arr, ext[1:]))
        
        elif direction == 'before':
            edge_spacing = arr[1] - arr[0]
            start = arr[0] - exlen*edge_spacing
            ext = np.arange(start, arr[0]+edge_spacing, edge_spacing)
            arrext = np.concatenate((ext[:-1], arr))
    
        return arrext
    
    elif exlen == 0:
        return arr


def within_range(val, vrange):
    """ Check if a value is within a range.

    **Parameters**\n
    val: numeric
        Value to check within range.
    vrange: tuple/list
        Range of values.
    """
    
    if (val >= vrange[0] and val <= vrange[-1]) or (val <= vrange[0] and val >= vrange[-1]):
        return True
    else:
        return False


def extend1D_until(arr, direction, vterm, step=5):
    """ Extend an array until a terminal value (vterm).

    **Parameters**\n
    arr: 1D array
        Array for extension.
    direction: str
        Direction of extension ('before' or 'after').
    vterm: numeric
        Terminal value for the extension.
    step: int | 5
        Number of steps to extend each time.
    """
    
    arrtmp = arr.copy()
    
    while not(within_range(vterm, arrtmp)):
        arrtmp = extend1D(arrtmp, direction, exlen=step)
        
    return arrtmp
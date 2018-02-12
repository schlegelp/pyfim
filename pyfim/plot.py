#    This code is part of pymaid (http://www.github.com/schlegelp/pyfim).
#    Copyright (C) 2017 Philipp Schlegel
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

import pyfim.core

import numpy as np

import matplotlib.pyplot as plt 

import math

def plot_parameters(coll, param=None, **kwargs):
    """ Plots a set of parameters from a pyFIM Collection.

    Parameters
    ----------
    coll :  pyFIM.Collection
    param : {str, list of str, None}, optional
            Parameters to plot. If None, will plot a default selection of 
            parameters: acc_dst, dst_to_origin, head_bends, bending_strength,
            peristalsis_frequency, peristalsis_efficiency, stops, pause_turns,
            velocity
            
    **kwargs
            Will be passed to pandas.DataFrame.plot

    Returns
    -------
    matplotlib.Axes

    """

    if not isinstance(coll, pyfim.core.Collection):
        raise TypeError('Need Collection, got {0}'.format(type(coll)))

    if param == None:
        param = ['acc_dst', 'dst_to_origin', 'head_bends', 'bending_strength',
            'peristalsis_frequency', 'peristalsis_efficiency', 'stops', 
            'pause_turns', 'velocity']
    elif not isinstance(param, (list, np.ndarray, set)):
        param = [ param ]

    # How many rows and columns
    n_cols = min(len(param), 3)
    n_rows = math.ceil( len(param) / n_cols  )

    # Generate figure
    fig, axes = plt.subplots( n_rows, n_cols, sharex=True )

    for i, p in enumerate(param):
        data = getattr(coll, p)
        this_row = math.floor( i / n_cols ) 
        this_col = i - this_row * n_cols 

        if n_rows > 1:
            ax = axes[this_row][this_col]
        elif len(param) == 1:
            ax = axes
        else:
            ax = axes[this_col]

        # Set defaults and incorporate kwargs
        defaults = dict( 
                         kind = 'box',
                         ax = ax
                            )
        defaults.update(kwargs)

        # Plot data 
        data.plot( **defaults )

        # Some make over
        ax.set_ylabel(p.replace('_',' '))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)                

    plt.tight_layout()    

    return axes



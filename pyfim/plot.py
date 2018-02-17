#    This code is part of pyFIM (http://www.github.com/schlegelp/pyfim), a
#    package to analyze FIMTrack data (fim.uni-muenster.de). For full  
#    acknowledgments and references, please see the GitHub repository.
#
#    Copyright (C) 2018 Philipp Schlegel
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

    if isinstance(param, type(None)):
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
        # Get data
        data = getattr(coll, p)

        # Calculate position in grid
        this_row = math.floor( i / n_cols ) 
        this_col = i - this_row * n_cols 

        # Get correct axis
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


def plot_tracks(exp, obj=None, ax=None, plot='head', **kwargs):
    """ Plots traces of tracked objects.

    Notes
    -----
    Uses "spinepoint_2" to plot objects center.

    Parameters
    ----------
    exp :   pyFIM.Experiment
    obj :   {str, list of str, None}
            Name of object(s) to plot. If None, will plot all objects in
            Experiment.
    ax :    matplotlib.Axes, optional
            Ax to plot on. If not provided, will create a new one.            
    plot :  {'center','head'}
            Which part of the object to plot.
    **kwargs
            Will be passed to ax.plot()

    Returns
    -------
    matplotlib.Axes

    """
    PERM_ARGS = ['center','head']
    if plot not in PERM_ARGS:
        raise ValueError('Unexpected "plot" argument. Please use either {0}'.format(','.join(PERM_ARGS)))

    if not isinstance(exp, pyfim.core.Experiment):
        raise TypeError('Need pyfim.Experiment, got {0}'.format(type(exp)))

    if isinstance( obj, type(None) ):
        obj = exp.objects

    if not isinstance( obj, (list, np.ndarray) ):
        obj = [ obj ]

    # Make sure objects actually exists
    for ob in obj:
        if ob not in exp.objects:
            raise ValueError('"{0}" not found in Experiment'.format(ob))

    # Make figure
    if not ax:
        fig, ax = plt.subplots()
        ax.set_aspect('equal')

    # Prepare default colors
    colors = plt.get_cmap('tab10').colors 
    # Multiply palette if necessary
    colors *= math.ceil( len(obj) / len(colors) )

    # Plot objects
    for i, ob in enumerate( [ exp[ob] for ob in obj ] ):
        defaults_lin = dict(
                            c=colors[i]
                            )
        defaults_lin.update(kwargs)

        if plot == 'head':
            x = ob.head_x
            y = ob.head_y
        elif plot == 'center':
            x = ob.spinepoint_2_x
            y = ob.spinepoint_2_y

        # Plot trace
        ax.plot(x, 
                y, 
                **defaults_lin)

        """
        # Indicate start with an "s"
        ax.text( x.dropna().iloc[0],
                 y.dropna().iloc[0],
                 'S',
                 color=defaults_lin['c']
                )
        """

    return ax


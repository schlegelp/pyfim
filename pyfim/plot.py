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

import math

import numpy as np

import matplotlib.pyplot as plt

from matplotlib.collections import LineCollection


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

        # Rotate xticklabels
        ax.set_xticklabels( ax.get_xticklabels(), rotation=35, ha='right' )

    plt.tight_layout()

    return axes


def plot_tracks(exp, obj=None, ax=None, **kwargs):
    """ Plots traces of tracked objects.


    Parameters
    ----------
    exp :   pyFIM.Experiment
    obj :   {str, list of str, None}
            Name of object(s) to plot. If None, will plot all objects in
            Experiment.
    ax :    matplotlib.Axes, optional
            Ax to plot on. If not provided, will create a new one.
    **kwargs
            Will be passed to ax.plot()

    Returns
    -------
    matplotlib.Axes

    """

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
                            color=colors[i],
                            linewidth=.5,
                            )
        defaults_lin.update(kwargs)

        # Subset to relevant parameters and drop empty frames
        ob = ob[[
                 'head_x','head_y',
                 'spinepoint_1_x','spinepoint_1_y',
                 'spinepoint_2_x','spinepoint_2_y',
                 'spinepoint_3_x','spinepoint_3_y',
                 'tail_x','tail_y',
                 ]].dropna(how='any', axis=0)

        # Extract x coordinates for each frame
        lines_x = ob[['tail_x',
                      'spinepoint_3_x',
                      'spinepoint_2_x',
                      'spinepoint_1_x',
                      'head_x']].values

        # Extract y coordinates for each frame
        lines_y = ob[['tail_y',
                      'spinepoint_3_y',
                      'spinepoint_2_y',
                      'spinepoint_1_y',
                      'head_y']].values

        # Merge x and y coordinates
        lines_xy = [ list(  zip(l_x,l_y) ) for l_x,l_y in zip(lines_x,lines_y) ]

        # Turn all lines into a collection
        lc = LineCollection( lines_xy, **defaults_lin )

        # Addd line collection to axis
        ax.add_collection(lc)

        """
        # Indicate start with an "s"
        ax.text( x.dropna().iloc[0],
                 y.dropna().iloc[0],
                 'S',
                 color=defaults_lin['c']
                )
        """

    ax.autoscale()

    return ax


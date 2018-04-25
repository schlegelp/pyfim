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


import math

import numpy as np
import pandas as pd

import peakutils

from pyfim import core, config
defaults = config.default_parameters

# Default analyses
__all__ = ['stops','pause_turns','bending_strength',
           'head_bends', 'peristalsis_efficiency',
           'peristalsis_frequency', 'stop_duration' ]

# Define two-choice analyses here
__two_choice__ = ['PI_over_time','preference_index']

def preference_index(exp):
    """ Calculates the preference index (PI) for a two choice experiment:

                    `PI = (exp-control)/(exp+control)`

    with `exp` and `control` being the number of objects on the experimental
    and the control side, respectively.

    Based on code by Sebastian Hueckesfeld (University of Bonn, Germany).

    Notes
    -----
    This function counts the number of objects in rolling windows of 10s on either side of a boundary.
    You can finetune this behaviour by adjusting the following parameters in
    the config file:
        - `TC_PARAM`: parameter used to split data (e.g. "mom_x" for split along x-axis)
        - `TC_BOUNDARY`: boundary between control and experiment
        - `TC_CONTROL_SIDE`: defines which side is the control
        - `TC_COUNT_WINDOW`: rolling window (in frames) over which to count max objects
        - `TC_SMOOTHING_WINDOW` : rolling window (in frames) over which to smooth PI
        - `TC_CUT_HEAD`: set to ignore the first X frames for PI calculation. Can be fraction (e.g. 0.75) of total frames.
        - `TC_CUT_TAIL`: set to ignore the last X frames for PI calculation. Can be fraction (e.g. 0.1) of total frames.

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Returns
    -------
    PI : float

    """

    # Check if PI over time has already been computed
    PI = getattr(exp, 'PI_over_time', None)

    # If necessary, calculate PI over time from scratch
    if isinstance(PI, type(None)):
        PI = PI_over_time(exp)

    # Remove head and tail frames if applicable
    if defaults['TC_CUT_HEAD']:
        # If fraction
        if defaults['TC_CUT_HEAD'] < 1:
            lower_bound = PI.shape[0] * defaults['TC_CUT_HEAD']
        else:
            lower_bound = defaults['TC_CUT_HEAD']
    else:
        lower_bound = 0

    if defaults['TC_CUT_TAIL']:
        # If fraction
        if defaults['TC_CUT_TAIL'] < 1:
            upper_bound = PI.shape[0] - PI.shape[0] * defaults['TC_CUT_TAIL']
        else:
            upper_bound = PI.shape[0] - defaults['TC_CUT_TAIL']
    else:
        upper_bound = PI.shape[0]

    PI = PI.iloc[ int(lower_bound) : int(upper_bound) ]

    return PI.PI.mean()

def PI_over_time(exp):
    """ Calculates the preference index (PI) for a two choice experiment over time:

                    `PI = (exp-control)/(exp+control)`

    with `exp` and `control` being the number of objects on the experimental
    and the control side, respectively.

    Based on code by Sebastian Hueckesfeld (University of Bonn, Germany).

    Notes
    -----
    This function counts the number of objects in rolling windows of 10s on either side of a boundary.
    You can finetune this behaviour by adjusting the following parameters in
    the config file:
        - `TC_PARAM`: parameter used to split data (e.g. "mom_x" for split along x-axis)
        - `TC_BOUNDARY`: boundary between control and experiment
        - `TC_CONTROL_SIDE`: defines which side is the control
        - `TC_COUNT_WINDOW`: rolling window (in frames) over which to count max objects
        - `TC_SMOOTHING_WINDOW` : rolling window (in frames) over which to smooth PI

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Returns
    -------
    PI over time : pandas.DataFrame

    """

    # Get parameter by which to split data
    tc_param = getattr(exp, defaults['TC_PARAM'])

    # Get count for below and above the boundary
    lower = (tc_param <= defaults['TC_BOUNDARY']).sum(axis=1).to_frame()
    upper = (tc_param > defaults['TC_BOUNDARY']).sum(axis=1).to_frame()

    # Sort into control and exp
    if defaults['TC_CONTROL_SIDE'] == 0:
        control, experiment = lower, upper
    elif defaults['TC_CONTROL_SIDE'] == 1:
        control, experiment = upper, lower
    else:
        raise ValueError('TC_CONTROL_SIDE must be either 0 or 1, not {0}'.format(defaults['TC_CONTROL_SIDE']))

    # Apply rolling window if applicable
    if defaults['TC_COUNT_WINDOW'] not in [None, 0, 1]:
        control = control.rolling(window=defaults['TC_COUNT_WINDOW']).max()
        experiment = experiment.rolling(window=defaults['TC_COUNT_WINDOW']).max()

    # Calculate PI
    PI = (experiment-control)/(experiment+control)
    PI.columns=['PI']

    # Apply smoothing if applicable
    if defaults['TC_SMOOTHING_WINDOW'] not in [None, 0, 1]:
        PI = PI.rolling(window=defaults['TC_SMOOTHING_WINDOW']).mean()

    return PI

def stop_duration(exp):
    """ Calculates mean duration of a stop. This analysis is based on MatLab
    code by Dimitri Berh (University of Muenster, Germany).

    Notes
    -----
    This function measures the average length of phases in which `go_phase` is
    zero. You can finetune this behaviour by adjusting the following parameter
    in the config file:
        - `MIN_STOP_PHASE`: minimum number of frames for a stop

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Returns
    -------
    Mean stop duration [Frames] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_duration = []

    # Iterate over all objects
    for obj in exp.go_phase:
        # Find stop and go phases
        stop_phases = binary_phases( exp.go_phase[obj].values,
                                      mode='OFF',
                                      min_len=defaults['MIN_STOP_PHASE'] )

        if len(stop_phases) > 0:
            # Add mean duration
            mean_duration.append( sum([ p[1]-p[0] for p in stop_phases ]) / len(stop_phases) )
        else:
            mean_duration.append( np.nan )

    return pd.Series(mean_duration, index=exp.go_phase.columns)


def stops(exp):
    """ Calculates frequency of stops [Hz] for each object. This analysis is
    based on MatLab code by Dimitri Berh (University of Muenster, Germany).

    Notes
    -----
    This function counts the phases in which `go_phase` is zero. You can
    finetune this behaviour by adjusting the following parameter in the
    config file:
        - `MIN_STOP_PHASE`: minimum number of frames for a stop-phase

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Returns
    -------
    Stop frequency [Hz] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_freq = []

    # Iterate over all objects
    for obj in exp.go_phase:
        # Find stop and go phases
        stop_phases = binary_phases( exp.go_phase[obj].values,
                                      mode='OFF',
                                      min_len=defaults['MIN_STOP_PHASE'] )
        # Add mean frequency
        mean_freq.append( len(stop_phases) / ( exp.go_phase[obj].dropna().shape[0] / defaults['FPS'] ) )

    return pd.Series(mean_freq, index=exp.go_phase.columns)


def pause_turns(exp):
    """ Calculates the frequency of pause-turns [Hz] for each object. This
    analysis is based on MatLab code by Dimitri Berh (University of Muenster,
    Germany).

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Notes
    -----
    This function counts the number of pause-turns by (1) finding pauses and
    (2) determining if the movement direction before and after the pause
    differs sufficiently. You can finetune this behaviour by changing the
    following parameters in the config file:
        - `MIN_STOP_TIME`: minimum number of frames for a pause to be counted as one.
        - `MIN_GO_TIME`: minimum frames before and after the pause to be counted as pause-turn.
        - `TURN_ANGLE_THRESHOLD`: minimum angular difference in movement direction before and after the pause.

    Returns
    -------
    Pause-Turn frequency [Hz] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_freq = []

    # Smooth moving direction using the median over X frames
    smoothed_mov = exp.mov_direction.rolling( defaults['DIRECTION_SMOOTHING'] ).median()

    # Iterate over all objects
    for obj in exp.mov_direction:
        # Find stop and go phases
        go_phases = binary_phases( exp.go_phase[obj].values, mode='ON' )

        turns = 0
        # Go over pairs of consecutive go phases
        for this_go, next_go in zip( go_phases, go_phases[1:] ):
            # Skip if go time too short
            if ( this_go[1] - this_go[0] ) < defaults['MIN_GO_TIME']:
                continue
            if ( next_go[1] - next_go[0] ) < defaults['MIN_GO_TIME']:
                continue

            # Skip if pause too short
            if ( next_go[0] - this_go[1] ) < defaults['MIN_STOP_TIME']:
                continue

            # Get directions before and after pause
            dir_before = smoothed_mov.loc[ this_go[1] - 1 , obj]
            dir_after = smoothed_mov.loc[ next_go[0] + 1 , obj]

            if math.fabs( dir_before - dir_after ) >= defaults['TURN_ANGLE_THRESHOLD']:
                turns +=1

        # Add mean frequency
        mean_freq.append( turns / ( exp.mov_direction[obj].dropna().shape[0] / defaults['FPS'] ) )

    return pd.Series(mean_freq, index=exp.mov_direction.columns)


def bending_strength(exp, during=None):
    """ Calculates the median (!) bending strength for each object. This
    analysis is based on MatLab code by Dimitri Berh (University of Muenster,
    Germany).

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.
    during :    {'stop','go', None}, optional
                Use to restrict to stop or go-phases.

    Notes
    -----
    This function determines the bending strength by (1) taking all bending
    angles, (2) thresholding them and (3) getting the median bending angle.
    You can finetune this behaviour using the following parameter in the
    config file:
        - `BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH`: minimum bending angle

    Returns
    -------
    Median bending strengths [angle] : pandas.DataFrame
                Returns NaN if no bends.

    """

    PERM_MODES = ['go','stop', None]

    if during not in PERM_MODES:
        raise ValueError('Unknown values for "during". Please use {0}'.format(PERM_MODES))

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    bend_strength = []

    # Iterate over all objects
    for obj in exp.bending:
        if during == 'go':
            this_bend = exp.bending[obj][ ( exp.go_phase[obj] == 1 ) & ( ~exp.bending[obj].isnull() ) ]
        elif during == 'stop':
            this_bend = exp.bending[obj][ ( exp.go_phase[obj] == 0 ) & ( ~exp.bending[obj].isnull() ) ]
        else:
            this_bend = exp.bending[obj]

        # Get absolute bending angles and remove NaNs
        abs_bend = ( this_bend - 180 ).abs().dropna()

        # Filter to above threshold bendings
        abs_bend = abs_bend[ abs_bend >= defaults['BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH'] ]

        # Add median frequency
        bend_strength.append( np.median( abs_bend ) )

    return pd.Series(bend_strength, index=exp.bending.columns)


def head_bends(exp):
    """ Calculates the head bend frequency [Hz] for each object. This analysis
    is based on MatLab code by Dimitri Berh (University of Muenster, Germany).

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Notes
    -----
    This function determines the number of head bends by (1) taking all
    bending angles, (2) thresholding them and (3) counting the number of
    bending phases of a given minimum length. You can finetune this behaviour
    using the following parameters in the config file:
        - `BENDING_ANGLE_THRESHOLD`: minimum bending angle
        - `MIN_BENDED_PHASE`: minimum consecutive number of frames above angle threshold

    Returns
    -------
    Mean head bending frequencies [Hz] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_freq = []

    # Iterate over all objects
    for obj in exp.bending:
        # Get absolute bending angles and remove NaNs
        abs_bend = ( exp.bending[obj] - 180 ).abs().dropna()

        # Get above threshold bendings
        is_bend = abs_bend >= defaults['BENDING_ANGLE_THRESHOLD']

        # Extract bending phases
        bend_phases = binary_phases( is_bend, mode='ON', min_len=defaults['MIN_BENDED_PHASE'] )

        # Add mean frequency
        mean_freq.append( len(bend_phases) / ( abs_bend.shape[0] / defaults['FPS'] ) )

    return pd.Series(mean_freq, index=exp.bending.columns)


def peristalsis_efficiency(exp):
    """ Calculates the peristalsis efficiency for each object. The unit is
    depending on the input data: [pixel/peristalsis] or [mm/peristalsis].
    This analysis is based on MatLab code by Dimitri Berh (University of
    Muenster, Germany).

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Notes
    -----
    This function determines the number of peristalses by performing peak
    detection of the object's area in its go-phases. The efficieny is the
    distance (in pixel or mm) per peristalsis. You can finetune this behaviour
    using the following parameters in the config file:
        - `MIN_GO_PHASE`: minimum length of the go phases
        - `MIN_PEAK_DIST`: minimal distance in frames between peristalses

    Returns
    -------
    Mean peristalsis efficiency [Hz] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_eff = []

    # Here, we are filling in missing distances - for unknown reasons these values
    # are just missing sometimes
    acc_dst_filled = exp.acc_dst.fillna(method='ffill')

    # Iterate over all objects
    for obj in exp.area:
        # Filter down to frames in which we have go_phase, area and acc_dst
        filt = ( ~exp.area[obj].isnull() ) & ( ~exp.go_phase[obj].isnull() ) & ( ~exp.acc_dst[obj].isnull() )
        area = exp.area[obj][ filt ].reset_index(drop=True)
        go_phase = exp.go_phase[obj][ filt ].reset_index(drop=True)
        acc_dst = exp.acc_dst[obj][ filt ].reset_index(drop=True)

        # Get go phases
        go_phases = binary_phases( go_phase.values, mode='ON', min_len=defaults['MIN_GO_PHASE'] )

        # Turn go phases into list of frames
        go_frames = np.array( [ f for l in [ np.arange( s,e ) for s,e in go_phases ] for f in l ] )

        # Get area in go-phases (also make sure there is area measured)
        go_area = area.iloc[ go_frames ]

        if len(go_area) > 0:
            # Detect peaks
            indexes = peakutils.indexes( go_area.values, min_dist=defaults['MIN_PEAK_DIST'] )

            # Get distances travelled per go phase
            go_acc_dist = sum( [  acc_dst_filled.loc[ e-1, obj ] -  acc_dst_filled.loc[ s, obj ] for s,e in go_phases ] )

            # Get mean frequency
            mean_eff.append( len(indexes) / go_acc_dist )
        else:
            mean_eff.append( np.nan )

    return pd.Series(mean_eff, index=exp.area.columns)


def peristalsis_frequency(exp):
    """ Calculates the peristalsis frequency [Hz] for each object. This
    analysis is based on MatLab code by Dimitri Berh (University of Muenster,
    Germany).

    Parameters
    ----------
    exp     :   pyfim.Experiment
                Experiment holding the raw data.

    Notes
    -----
    This function determines the number of peristalses by performing peak
    detection of the object's area in its go-phases. You can finetune this
    behaviour using the following parameters in the config file:
        - `MIN_GO_PHASE`: minimum length of the go phases
        - `MIN_PEAK_DIST`: minimal distance in frames between peristalses

    Returns
    -------
    Mean peristalsis frequencies [Hz] : pandas.DataFrame

    """

    if not isinstance(exp, core.Experiment):
        raise TypeError('Need pyfim.Experiment, not {0}'.format(type(exp)))

    mean_freq = []

    # Iterate over all objects
    for obj in exp.area:
        # Filter down to frames in which we have go_phase, area and acc_dst
        filt = ( ~exp.area[obj].isnull() ) & ( ~exp.go_phase[obj].isnull() )
        area = exp.area[obj][ filt ].reset_index(drop=True)
        go_phase = exp.go_phase[obj][ filt ].reset_index(drop=True)

        # Get go phases
        go_phases = binary_phases( go_phase.values, mode='ON', min_len=defaults['MIN_GO_PHASE'] )

        # Turn go phases into list of frames
        go_frames = np.array( [ f for l in [ np.arange( s,e ) for s,e in go_phases ] for f in l ] )

        # Get area in go-phases (also make sure there is area measured)
        go_area = area.loc[ go_frames ]

        # Make sure there is area measures available
        go_area = go_area[ ~go_area.isnull() ]

        if len(go_area) > 0:
            # Detect peaks
            indexes = peakutils.indexes( go_area.values, min_dist=defaults['MIN_PEAK_DIST'] )

            # Get mean frequency
            mean_freq.append( len(indexes) / ( go_area.shape[0] / defaults['FPS'] ) )
        else:
            mean_freq.append( np.nan )

    return pd.Series(mean_freq, index=exp.area.columns)


def binary_phases(x, mode='ON', min_len=1):
    """ Low-level function: Extracts phases from binary indicators such as
    "go_phase" or "is_coiled".

    Parameters
    ----------
    x :         (list, np.ndarray, pd.Series)
                Must be consist of True/False or 0/1. E.g. [0,0,0,1,1,1,0,1,1]
    mode :      {'ON','OFF','ALL'}, optional
                Phases to return. For above example:
                  - 'ON', will return [(3,6),(7,9)]
                  - 'OFF', will return [(0,3),(6,7)]
                  - 'ALL' will return [(0,3),(3,6),(6,7),(7,9)]
    min_len :   int, optional

    Returns
    -------
    Indices of phases

    """

    # Important: do NOT add this to __all__ -> otherwise this will be run as analysis

    PERM_MODES = ['ON','OFF','ALL']
    if mode not in PERM_MODES:
        raise ValueError('Unknown values for "min_len". Please use {0}'.format(PERM_MODES))

    if isinstance(x, (list, set)):
        x = np.array(x)
    elif isinstance(x, pd.Series):
        x = x.values

    if not isinstance(x, np.ndarray):
        raise ValueError('Expect a numpy array, got {0}'.format(type(x)))

    # Make sure we're working on a copy
    x = x.copy()

    # Set NaNs to OFF
    #x [ np.isnan(x) ] = 0

    # Drop NaNs
    x = x[ ~np.isnan(x) ]

    if x.ndim != 1:
        raise ValueError('Can only process 1-dimensional data, got {0}'.format(x.ndim))

    # Make sure we're working on zeroes and ones
    x = x.astype(int)

    # Find start and end of phases using the first derivative
    deriv = np.diff( x )
    all_cuts = np.where( deriv != 0 )[0] + 1

    # Make sure we have start and end of the array covered
    if 0 not in all_cuts:
        all_cuts = np.insert( all_cuts, 0, 0)

    if len(x) not in all_cuts:
        all_cuts = np.append( all_cuts, len(x) )

    # List of all phases
    all_phases = list( zip( all_cuts, all_cuts[1:]  ) )

    # Separate on and of phases based on what the array started with
    if x[0] == 1:
        on_phases = all_phases[::2]
        off_phases = all_phases[1::2]
    else:
        off_phases = all_phases[::2]
        on_phases = all_phases[1::2]
    all_phases = list( zip(all_cuts[:-1], all_cuts[1:]) )

    if mode == 'ON':
        return np.array( [ (a,b) for a,b in on_phases if b-a >= min_len ] )
    elif mode == 'OFF':
        return np.array( [ (a,b) for a,b in off_phases if b-a >= min_len ] )
    elif mode == 'ALL':
        return np.array( [ (a,b) for a,b in all_phases if b-a >= min_len ] )




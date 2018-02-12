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


from io import IOBase
import os

import pandas as pd
import numpy as np

from tqdm import tqdm

# Load analysis scripts
from pyfim import analysis as fim_analysis
from pyfim import plot as fim_plot

# Load default values
from pyfim import config
defaults = config.default_parameters

import logging
module_logger = logging.getLogger('pyfim')
module_logger.setLevel(logging.INFO)
if len( module_logger.handlers ) == 0:
    # Generate stream handler
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    # Create formatter and add it to the handlers
    formatter = logging.Formatter(
                '%(levelname)-5s : %(message)s (%(name)s)')
    sh.setFormatter(formatter)
    module_logger.addHandler(sh)

class Collection:
    """ Collection of experiments. This allows you to easily collect and plot
    data from multi experiments.

    Examples
    --------
    >>> # Initialise two experiments from CSVs in a folder
    >>> exp1 = pyfim.Experiment( 'users/data/genotype1' )
    >>> exp2 = pyfim.Experiment( 'users/data/genotype2' )
    >>> # Initialise collection and add data
    >>> c = pyfim.Collection()
    >>> c.add_data( exp1, 'Genotype I')
    >>> c.add_data( exp2, 'Genotype II')
    >>> # Get a summary
    >>> c
    ... <class 'pyfim.core.Collection'> with 2 experiments: 
    ... name  n_objects  n_frames
    ... 0  exp_1         47      1800
    ... 1  exp_2         46      1800 
    ... Available parameters: mom_y, perimeter, peristalsis_frequency, 
    ... radius_3, pause_turns, spinepoint_2_x, acc_dst, ...
    >>> # Access analyses
    >>> c.peristalsis_frequency
    >>> # Plot as boxplot
    >>> ax = c.peristalsis_frequency.plot(kind='box')
    >>> plt.show()
    """

    def __init__(self):
        self.experiments = []
        pass

    def add_data(self, x, label=None, keep_raw=False):
        """ Add an data (e.g. a genotype) to this analysis.

        Parameters
        ----------
        x :         {filename, folder, file object, list thereof, pyfim.Experiment}
                    Provide either:
                        - a CSV file name
                        - a CSV file object
                        - list of the above
                        - single folder
                        - single pyfim.Experiment object
                    Lists of files will be merged and larva will be renumbered.
        label :     str, optional
                    Label of this data set.
        keep_raw :  bool, optional
                    If False, will not keep .csv raw data. Saves memory.

        Returns
        -------
        Nothing.
        """
        if not label:
           label = 'exp_{0}'.format( len( self.experiments ) + 1 )

        if not isinstance( x, Experiment ):
            exp = Experiment(x, keep_raw=keep_raw)
        else:
            exp = x

        setattr(self, label, exp )

        self.experiments.append(label)

        self.extract_data()

    def summary(self):
        """ Gives a summary of the data in this analysis.
        """

        to_summarize = ['n_objects','n_frames']

        return pd.DataFrame( [ [exp] + [ getattr( getattr(self, exp), p ) for p in to_summarize ] for exp in self.experiments ],
                             columns=['name']+to_summarize )

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{0} with {1} experiments: \n {2} \n Available parameters: {3}'.format(type(self), 
                                                                                     len(self.experiments), 
                                                                                     str(self.summary()),
                                                                                     ', '.join(self.parameters) )

    @property
    def parameters(self):
        """Returns parameters that all experiments have in common."""
        all_params = [ set( getattr(self, exp).parameters ) 
                                for exp in self.experiments ]
        if all_params:
            return np.array( list(all_params[0].union(*all_params) ) )
        else:
            return []

    def extract_data(self):
        """ Get the mean over all parameters.
        """

        # Get basic parameter from raw data
        for param in self.parameters:
            data = [ ]
            for e in self.experiments:
                # Collect data
                exp = getattr(self, e)
                values = getattr( exp, param )
                if values.ndim == 1:
                    means = values.values
                else:
                    means = values.mean().values
                data.append( means )
            df = pd.DataFrame( data, index= self.experiments ).T
            setattr(self, param, df)   

    def plot(self, param=None, **kwargs):
        """ Plots a set of parameters from this pyFIM Collection.

        Parameters
        ----------
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
        return fim_plot.plot_parameters(self, param, **kwargs)    


class Experiment:
    """ Class that holds raw data for a set of data.

    Parameters
    ----------
    f :         {filename, folder, file object, list thereof, pyfim.Experiment}
                    Provide either:
                        - a CSV file name
                        - a CSV file object
                        - list of the above
                        - single folder
                        - single pyfim.Experiment object
                Lists of files will be merged and larva will be renumbered.   
    keep_raw :  bool, optional
                If False, will not keep .csv raw data. Saves memory.


    Examples
    --------
    >>> # Generate an experiment from all csv files in one folder
    >>> folder = 'users/downloads/genotype1'
    >>> exp = pyfim.Experiment( folder )
    >>> # See available analysis
    >>> exp.parameters
    ... ['acc_dst', 'acceleration', 'area', 'bending',...
    >>> # Access data
    >>> exp.dst_to_origin.head()
    ...    object_1  object_13  object_15  object_18  object_19  \
    ... 0   0.00000    0.00000        NaN        NaN        NaN   
    ... 1   2.23607    0.00000        NaN        NaN        NaN   
    ... 2   3.60555    1.41421        NaN        NaN        NaN   
    ... 3   3.60555    2.82843        NaN        NaN        NaN   
    ... 4   4.47214    4.24264        0.0        NaN        NaN   
    >>> # Plot data individual objects over time
    >>> ax = exp.dst_to_origin.plot()
    >>> plt.show()
    >>> # Get mean of all values
    >>> exp.mean()
    """

    def __init__(self, f, keep_raw=False):  
        # Make sure we have files or filenames
        f = _parse_files(f)

        # Get the data from each individual file
        data = [ pd.read_csv(fn, sep=defaults['DELIMITER'], index_col=0) for fn in tqdm(f, desc='Reading files', leave=False) ]

        # Merge - make sure the indices match up
        self.raw_data = pd.concat( data, axis=1, ignore_index=False )
        self.raw_data.columns = [ 'object_{0}'.format(i) for i in range( self.raw_data.shape[1] ) ]

        self.extract_data() 

        if not keep_raw:
            del self.raw_data

    def extract_data(self):
        """ Extracts parameters from .csv file.
        """

        if isinstance( getattr(self, 'raw_data', None) , type(None) ):
            raise ValueError('No raw data to analyze found.')

        # Find all parameters
        self.parameters = sorted (set( [ p[ : p.index('(') ] for p in self.raw_data.index ] ) )

        # Go over all parameters
        for p in tqdm( self.parameters, desc='Extracting data', leave=False ):
            # Extract values
            values = self.raw_data.loc[ [ p in i for i in self.raw_data.index ] ]

            # Change the index to frames
            values.index = list(range( values.shape[0] ))

            # Add data as attribute
            setattr(self, p, values )
        
        # Perform data clean up
        self.clean_data()        
        
        # Perform additional, "higher-level" analyses
        for param in tqdm(fim_analysis.__all__, desc='Performing additional analyses', leave=False):
            func = getattr( fim_analysis, param )
            setattr(self, param, func( self ) )
            self.parameters.append( param )

        self.parameters = sorted( self.parameters ) 
        

    @property
    def objects(self):
        """ Returns the tracked objects in this experiment. Please note that
        the order is not as in the DataFrames.
        """
        all_cols = []
        for p in self.parameters:
            values = getattr(self, p )
            if isinstance(values, pd.DataFrame):
                all_cols.extend( values.columns.values )        

        return sorted( list( set(all_cols ) ) ) 

    @property
    def n_objects(self):
        """ Returns the number of objects tracked in this experiment.
        """

        return getattr(self, self.parameters[0] ).shape[1]

    @property
    def n_frames(self):
        """ Returns the number of frames in this experiment.
        """

        return getattr(self, self.parameters[0] ).shape[0]

    def clean_data(self):
        """ Cleans up the data.
        """
        frames_before = self.n_frames
        obj_before = self.n_objects

        # Get objects that have a at least a single all nan table
        has_all_nans = [ obj for obj in self.objects if 0 in self[obj].count().values ]

        # Will use the "head_x" parameter to determine track length 
        # -> some other parameters (e.g. "go_phase") vary in length   
        long_enough = [ obj for obj in self.objects if 
                        getattr(self, 'head_x')[obj].count() >= defaults['MIN_TRACK_LENGTH'] 
                        and obj not in has_all_nans]
        

        for p in tqdm(self.parameters, desc='Cleaning data', leave=False):
            values = getattr(self, p)

            # Drop objects that have all nans
            values = values.drop( has_all_nans, axis=1 )

            # Remove object (columns) too few data points
            if defaults['MIN_TRACK_LENGTH']:                              
                # Remove columns with fewer than minimum values
                values = values.loc[:, long_enough ]

            # Remove first X entries
            if defaults['CUT_TABLE_HEAD']:
                values = values.iloc[ defaults['CUT_TABLE_HEAD'] : ]

            # Remove last X entries
            if defaults['CUT_TABLE_TAIL']:
                values = values.iloc[ : defaults['CUT_TABLE_TAIL'] ]

            # Convert to mm/mm^2
            if defaults['PIXEL2MM']:
                if p in defaults['SPATIAL_PARAMS']:
                    values *= defaults['PIXEL_PER_MM']                    
                elif p in defaults['AREA_PARAMS']:
                    values = np.sqrt(values) * defaults['PIXEL_PER_MM']

            # Interpolate gaps (i.e. a sub-threshold gap between two above
            # threshold stretches) in thresholded parameters
            if defaults['FILL_GAPS'] and p in defaults['THRESHOLDED_PARAMS']:
                # Keep track of zeros
                zeros = values == 0.0
                # Set zeros to "NaN"
                values[ values == 0.0 ] = np.nan
                # Fill gaps with previous value ("forward fill")
                values = values.fillna( method='ffill',
                                        axis=0,
                                        limit=defaults['MAX_GAP_SIZE'])
                # Set zeros that stayed zeros back to zero
                values[ (zeros) & ( values.isnull() ) ] = 0.0

            setattr( self, p, values )

        module_logger.info('Data clean-up dropped {0} objects and {1} frames'.format( obj_before-self.n_objects, frames_before-self.n_frames ))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '{0} with: {1} objects; {2} frames. Available parameters: {3}'.format(type(self), self.n_objects, self.n_frames, ', '.join(self.parameters) )

    def analyze(self, p):
        """ Returns analysis for given parameter.
        """
        return getattr(self, p).describe()

    def mean(self, p=None ):
        """ Return mean of given parameter over given parameter. If no 
        parameter is given return means vor all parameters.
        """
        if p == None:
            all_means = []
            for p in self.parameters:
                values = getattr(self, p)
                if values.ndim == 1:
                    all_means.append(values.values)
                else:
                    all_means.append(values.mean(axis=0).values)
            return pd.DataFrame(  all_means,
                                  index=self.parameters,
                                  columns=self.objects,
                                   )                   
        else:
            values = getattr(self, p)
            if values.ndim == 1:
                return values
            else:
                return values.mean(axis=0)

    def sanity_check(self):
        """ Does a sanity check of all attached data.
        """
        errors_found = False

        # Test if we have the same number of frames/objects for each parameter
        shapes = [ set( getattr(self, p).shape ) for p in self.parameters ]
        intersect = shapes[0].intersection( *shapes )
        if len(intersect) > 2:
            module_logger.warning('Found varying numbers of frames: {0}'.format(intersect))
            errors_found = True

        # Test if we have the same columns labels for all parameters
        c_labels = [ set( getattr(self, p).columns ) for p in self.parameters if isinstance(getattr(self, p), pd.DataFrame) ]
        union = c_labels[0].union( *c_labels )
        if False in [ l in getattr(self, p) for p in self.parameters for l in union if isinstance(getattr(self, p), pd.DataFrame) ]:
            module_logger.warning('Found mismatches in names of objects.')
            errors_found = True

        # Test if we have any empty columns
        for p in self.parameters:
            if isinstance( getattr(self, p), pd.DataFrame ):
                if True in ( getattr(self, p).count(axis=0) == 0):
                    module_logger.warning('Found empty columns for parameter "{0}"'.format(p))
                    errors_found = True

        if not errors_found:
            module_logger.info('No errors found - all good!')

    def __getitem__(self, key):
        """ Retrieves data for a SINGLE object. Please note that for 
        parameters with only a single data point per object (e.g. head_bends),
        this single parameter will be at frame 0 and the rest of the column
        will be NaN.
        """
        if key not in self.objects:
            raise ValueError('Object "{0}" not found.'.format(key))

        # Get data
        data = []
        for p in self.parameters:
            values = getattr(self, p)[key]
            if isinstance(values,float):
                values = pd.DataFrame([values])
            data.append(values)

        df = pd.concat( data, axis=1 ) 
        df.columns = self.parameters   

        return df


def _parse_files(x):
    """Parses input to filenames or file objects. Will always return a list!
    """
    if isinstance(x, (np.ndarray, list, set)):
        return [ e for f in x for e in _parse_files(f) ]
    elif isinstance(x, str):
            if os.path.isfile(x):
                return [ x ]
            elif os.path.isdir(x):
                return [ f for f in os.listdir(x) if f.endswith(defaults['FILE_FORMAT']) ]
            else:
                raise ValueError('Unable to intepret "{0}" - appears to be neither a file nor a folder'.format(x))
    elif isinstance( x, IOBase ):
        return [ x ]
    else:
        raise ValueError('Unable to intepret inputs of type {0}'.format(type(x)))


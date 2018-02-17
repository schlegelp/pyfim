Configuration
*************

When you initialize a :class:`~pyfim.Experiment`, raw data is extracted from
the .csv(s) and cleaned-up. Then, additional analyses are performed. You can
fine tune the clean up and the analyses by changing default parameters.

Upon importing pyfim, defaults are loaded from `config.py` in the pyFIM
directory. You can either change the defaults in the file which will affect
all subsequent sessions (persistent, does not work on-the-fly!) or change the
defaults in the current session (temporary, only for this session).

Making lasting changes
----------------------

First, you have to locate the pyFIM directory:

1. Open a Python session

2. Import pyFIM: 

>>> import pyfim

3. Get location: 

>>> pyfim.__file__

Next, navigate to the pyFIM directory, open `config.py` and make your changes.

Making temporary changes
------------------------

You can change defaults for the current session.

>>> import pyfim
>>> # Defaults are stored as dictionary
>>> pyfim.defaults
... {'AREA_PARAMS': ['area'],
... 'BENDING_ANGLE_THRESHOLD': 45,
... 'BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH': 20,
... 'CUT_TABLE_HEAD': False, ...
>>> # Change some parameter
>>> pyfim.defaults['MIN_STOP_TIME'] = 10


What is what
------------

The `config.py` is well documented and superseeds this document but here is a
list of relevant parameters:

.. csv-table:: Config parameters
   :file: conf_param.csv
   :widths: 20, 30, 50
   :header-rows: 1

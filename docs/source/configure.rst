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
2. Import pyFIM: `import pyfim`
3. Get location: `pyfim.__file__`

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

FILE_FORMAT : File format to search for
DELIMITER : Delimiter in CSV file

PIXEL2MM : If True, pixel coords are converted to mm or mm^2
PIXEL_PER_MM : Adjust this according to your setup
SPATIAL_PARAMS : List parameters that can be converted to mm
AREA_PARAMS : List parameters that can be converted to mm^2

FPS : Frames per second -> used to calculate Hz

CUT_TABLE_HEAD : Set to e.g. 10 to cut off the first 10 frames
CUT_TABLE_TAIL : Set to e.g. 10 to cut off the last 10 frames

REMOVE_NANS : Remove objects without any values

MIN_TRACK_LENGTH : Minimum track length in frames

FILL_GAPS : Fill sub-threshold gaps within thresholded columns, e.g. [0,1,1,0,0,1,1] -> [0,1,1,1,1,1,1] 
MAX_GAP_SIZE : Max gap size...
THRESHOLDED_PARAMS : Parameters to fill gaps in

BENDING_ANGLE_THRESHOLD : Minimum angle to be counted as bend
MIN_BENDED_PHASE : Minimum consecutive frames spend bent

MIN_STOP_PHASE : Minimum number of frames for a stop

MIN_PEAK_DIST : Minimum frames between peristalses

MIN_STOP_TIME : Minimum length of pause in frames
MIN_GO_TIME : Minimum frames of go phase before and after pause
TURN_ANGLE_THRESHOLD : Minimum anglular difference in movement direction before vs after pause
DIRECTION_SMOOTHING :Direction will be smoother over X frames

BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH : Minimum angle for bending strength
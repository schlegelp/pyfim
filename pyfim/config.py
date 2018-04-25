""" Set default parameters here.
"""

default_parameters = dict(

# Input files
FILE_FORMAT               = '.csv', # File format to search for
DELIMITER                 = ',',    # Delimiter in CSV file

# Spatial resolution
PIXEL2MM                  = False,  # If True, pixel coords are converted to mm or mm^2
PIXEL_PER_MM              = 150,    # Adjust this according to your setup
SPATIAL_PARAMS            = ['acc_dst',
                             'acceleration',
                             'dst_to_origin',
                             'head_x',
                             'head_y',
                             'mom_dst',
                             'mom_x',
                             'mom_y',
                             'perimeter',
                             'radius_1',
                             'radius_2',
                             'radius_3',
                             'spine_length',
                             'spinepoint_1_x',
                             'spinepoint_1_y',
                             'spinepoint_2_x',
                             'spinepoint_2_y',
                             'spinepoint_3_x',
                             'spinepoint_3_y',
                             'tail_x',
                             'tail_y',
                             'velocity'],
AREA_PARAMS               = ['area'],

# Temporal resolution
FRAMES2MIN                = True, # Not implemented yet
FPS                       = 10,   # Frames per second -> used to calculate Hz

# Remove N first/last entries of results table
CUT_TABLE_HEAD            = False, # Set to e.g. 10 to cut off the first 10 rows
CUT_TABLE_TAIL            = False,

# Remove objects (columns) without any values
REMOVE_NANS               = True, # Not doing this is actually a bad idea!

# Remove objects (columns) with less N tracked frames
MIN_TRACK_LENGTH          = 600,  # Minimum track length in frames

# Fill sub-threshold gaps within thresholded columns
# e.g. [0,1,1,0,0,1,1] -> [0,1,1,1,1,1,1]
FILL_GAPS                 = True,
MAX_GAP_SIZE              = 3,
THRESHOLDED_PARAMS        = ['left_bended',
                             'right_bended',
                             'go_phase',
                             'is_coiled',
                             'is_well_oriented'],

# Parameters for head bending
BENDING_ANGLE_THRESHOLD   = 45, # Minimum angle to be counted as bend
MIN_BENDED_PHASE          = 4,  # Minimum consecutive frames spend bent

# Parameter for stop counting
MIN_STOP_PHASE            = 5,  # Minimum number of frames for a stop

# Parameters for area peak (peristalsis) analysis
MIN_PEAK_DIST             = 5,  # Minimum frames between peristalses
MIN_GO_PHASE              = 30, # Not yet implemented

# Parameters for pause-turns
MIN_STOP_TIME             = 4,  # Minimum length of pause in frames
MIN_GO_TIME               = 20, # Minimum frames of go phase before and after pause
TURN_ANGLE_THRESHOLD      = 30, # Minimum anglular difference in movement direction before vs after pause
DIRECTION_SMOOTHING       = 10, # Direction will be smoother over X frames

# Parameter for bending strength
BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH   = 20, # Minimum angle for bending strength

# Parameters for two-choice preference index (PI)
TC_PARAM                  = 'mom_x', # Parameter used to split data (e.g. "mom_x" for split along x-axis)
TC_BOUNDARY               = 1000,    # Boundary between control and experiment. Has to be in mm if `PIXEL2MM` is True, else in pixel.
TC_CONTROL_SIDE           = 0,       # Defines which side is the control: 0 = lower than ("left of") `TC_BOUNDARY`, 1 = higher than ("right of") `TC_BOUNDARY`
TC_COUNT_WINDOW           = 30,      # Rolling window (in frames) over which to count objects on either side.
TC_SMOOTHING_WINDOW       = 30,      # Rolling window (in frames) over which to smooth PI.
TC_CUT_HEAD               = 0.75,    # Set to ignore the first X frames for PI calculation. Can be fraction (e.g. 0.75) of total frames.
TC_CUT_TAIL               = False,   # Set to ignore the last X frames for PI calculation. Can be fraction (e.g. 0.75) of total frames.

)
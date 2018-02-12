""" Set default parameters here.
"""

default_parameters = dict(

# Few settings for the input files
FILE_FORMAT               = '.csv', # Set file format to search for
DELIMITER                 = ',',    # Delimiter in CSV file

# Spatial resolution fo video
PIXEL2MM                  = False,  # If True, Pixel coords are converted to mm or mm^2
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

# Remove X first/last entries of results table
CUT_TABLE_HEAD           = False, # Set e.g. to 10 to cut off the first 10 rows
CUT_TABLE_TAIL            = False,

# Remove objects (columns) without any values
REMOVE_NANS               = True, # Not doing this is actually a bad idea!

# Remove objects (columns) with less than this values
MIN_TRACK_LENGTH          = 600,  # Minimum track length in frames

# Fill NaN gaps within thresholded columns
# e.g. [0,1,1,NaN,1,0,0,1] -> [0,1,1,1,1,0,0,1]
FILL_GAPS                 = True,
MAX_GAP_SIZE              = 3,
THRESHOLDED_PARAMS        = ['left_bended','right_bended','go_phase',
                             'is_coiled', 'is_well_oriented'],

# Parameters for head bending
BENDING_ANGLE_THRESHOLD   = 45, # Minimum angle to be counted as bend
MIN_BENDED_PHASE          = 4,  # Minimum consecutive frames spend bent

# Parameter for stop counting
MIN_STOP_PHASE            = 5,  # Minimum number of frames for a stop to be counted

# Parameter for area peak (peristalsis) analysis
MIN_PEAK_DIST             = 5,  # Minimum frames between peristalses
MIN_GO_PHASE              = 30, # Not yet implemented

# Parameters for pause-turns
MIN_STOP_TIME             = 4,  # Minimum length of pause in frames
MIN_GO_TIME               = 20, # Minimum frames of go phase before and after pause
TURN_ANGLE_THRESHOLD      = 30, # Minimum anglular difference in movement direction before vs after pause
DIRECTION_SMOOTHING       = 10, # Direction will be smoother over X frames

# Parameter for bending strength
BENDING_ANGLE_THRESHOLD_FOR_BENDING_STRENGTH   = 20 # Minimum angle for bending strength

)
pyFIM
=====

Python 3 toolbox for analysing [FIM](https://www.uni-muenster.de/PRIA/en/FIM/) data:

1. Read .csv files produced by [FIMTrack](https://www.uni-muenster.de/PRIA/en/FIM/download.shtml)
2. Merge individual files into experiments
3. Add experiments into collections
4. Analyse across experiments

FIMTrack CSV files contain a large selection of primary, secondary and
tertiary features (position, area, movement direction, length, etc). PyFIM
adds a few high-level analyses:

- pause-turn frequency
- stop frequency
- bending strength
- head bend frequency
- peristalsis frequency
- peristalsis efficiency

## Installation
I recommend using [Python Packaging Index (PIP)](https://pypi.python.org/pypi) to install pyFIM.
First, get [PIP](https://pip.pypa.io/en/stable/installing/) and then run in a terminal:

`pip install git+git://github.com/schlegelp/pyfim@master`

This command should also work to update the package.

If your default distribution is Python 2, you have to explicitly tell [PIP](https://pip.pypa.io/en/stable/installing/) to install for Python 3:

`pip3 install git+git://github.com/schlegelp/pyfim@master`

If you are behind a firewall try:

`pip install git+https://github.com/schlegelp/pyfim@master`

### Dependencies

Please make sure you have all these dependencies installed. They are all
available via PIP.

- [Pandas](http://pandas.pydata.org/) >= 0.21.0
- [Numpy](http://www.scipy.org) >= 1.13.3
- [peakutils](https://pypi.python.org/pypi/PeakUtils) >= 1.1.0
- [tqdm](https://pypi.python.org/pypi/tqdm) >= 4.15.0

## Quickstart

pyFIM consists only of two classes that do the all the data handling for you: 
`Experiment` and `Collection`.

- `Experiment` represents a set of cohesive experiments (e.g. from a single genotype)
- `Collection` constructs data tables across experiments

First things first: all data clean up (e.g. removing objects with too little 
data) and additional analyses (e.g. pause-turns or peristalsis frequency) are 
done the moment you initialise an `Experiment`. You can tune this by changing 
the defaults in `config.py`. Please note that changes to the `config.py` will 
only take effect if you restart your Python session. On the fly, you can 
change the defaults by e.g. `pyfim.defaults['PIXEL_PER_MM'] = 300`.

Data is generally stored as pandas DataFrames or Series. So you can use 
their fancy indexing, statistics and [visualisation](https://pandas.pydata.org/pandas-docs/stable/visualization.html).

Let's start off with a simple case: exploring a single `Experiment`.

```python
import pyfim
import matplotlib.pyplot as plt

# Initialise an experiment using a single CSV file
exp = pyfim.Experiment('/experiments/genotype1/exp1.csv')

# Get a summary and available parameters
print( exp )

# Access a data table. Please note that some data tables are 2 dimensional
# (e.g. velocity) while others are 1 dimensional (e.g. pause_turns)
velocity = exp.velocity
pause_turns = exp.pause_turns

# Get the mean over all objects tracked
mean_velocity = exp.mean('velocity')
# Alternatively (for 2 dimensional data tables)
mean_velocity = exp.velocity.mean(axis=0)

# The second way also lets you get other metrics
max_velocity = exp.velocity.max(axis=0)

# Get all means over all parameters
all_means = exp.mean()

# We can also access data by the object:
# Get a list of tracked objects
objects = exp.objects

obj1_data = exp['object_1']

# Plot data over time
ax = exp.velocity.plot()
plt.show()

# Plot some frequency parameters over all objects
param_to_plot = ['head_bends','pause_turns','peristalsis_frequency','stops']
ax = exp.means().loc[param_to_plot].T.plot(kind='box')
plt.show()
```

In the second example, we compare two `Experiments`:

```python
import pyfim
import matplotlib.pyplot as plt

# Load CSV files from two folders
exp1_folder = '/experiments/genotype1'
exp2_folder = '/experiments/genotype2'

exp1 = pyfim.Experiment(exp1_folder)
exp2 = pyfim.Experiment(exp2_folder)

# Initialise a Collection and add the Experiments
coll = pyfim.Collection()
coll.add_data(exp1, label='genotypeI')
coll.add_data(exp2, label='genotypeII')

# Get a summary of the Collection
print( coll )

# Get and plot a single parameter
mean_acc_dst = coll.acc_dst
ax = mean_acc_dst.plot(kind='box')
plt.show()

# Collections have a built-in plotting function that 
# lets you plot multiple parameters as boxplots
ax = coll.plot(['head_bends','pause_turns','stops'])
plt.show()

```

## Acknowledgments
Big thanks to Dimitri Berh, Benjamin Risse and Nils Otto for sharing their 
original MatLab code for the additional analyses!


## FIM Publications

Risse B, Berh D, Otto N, Klämbt C, Jiang X. FIMTrack: An open source tracking and locomotion analysis software for small animals. Poisot T, ed. PLoS Computational Biology. 2017;13(5):e1005530. doi:10.1371/journal.pcbi.1005530.

Risse B, Otto N, Berh D, Jiang X, Klämbt C. FIM Imaging and FIMtrack: Two New Tools Allowing High-throughput and Cost Effective Locomotion Analysis. Journal of Visualized Experiments : JoVE. 2014;(94):52207. doi:10.3791/52207.

Risse B, Thomas S, Otto N, et al. FIM, a Novel FTIR-Based Imaging Method for High Throughput Locomotion Analysis. Gilestro GF, ed. PLoS ONE. 2013;8(1):e53963. doi:10.1371/journal.pone.0053963.

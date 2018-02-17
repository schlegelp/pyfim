.. _example:

Introduction
************
This section will teach you the basics of how to use pyFIM. 

Experiments and Collections
---------------------------
Everython in pyFIM is done by two basic classes: :class:`~pyfim.Experiment` and :class:`~pyfim.Collection`. 

:class:`~pyfim.Experiment` extracts data from .csv files, does analyses and
helps you access each parameter. The idea is that you divide data from e.g.
different genotypes into an Experiment each. 

:class:`~pyfim.Collection` keep track of your Experiments. Their job is to
generate data tables from attached Experiments collapsing data into 
means per larva.

Both these classes simply juggle data stored as pandas DataFrames or Series. 
So you can use pandas fancy indexing, statistics and [visualisation](https://pandas.pydata.org/pandas-docs/stable/visualization.html).

All data clean up (e.g. removing objects with too little data) and additional
analyses (e.g. pause-turns or peristalsis frequency) are done the moment you
initialise an `Experiment`. You can fine tune how this is done by changing the
defaults in `config.py`. Please note that changes to the `config.py` will only
take effect if you restart your Python session. On the fly, you can change the
defaults by e.g. `pyfim.defaults['PIXEL_PER_MM'] = 300`. See Configuration 
section.

Learning by doing
-----------------
Let's start off with a simple case: exploring a single `Experiment`.

>>> import pyfim
>>> import matplotlib.pyplot as plt
>>> # Initialise an experiment using a single CSV file
>>> exp = pyfim.Experiment('/experiments/genotype1/exp1.csv')

>>> # Get a summary and available parameters
>>> print( exp )
... <class 'pyfim.core.Experiment'> with: 48 objects; 1800 frames. Available parameters: acc_dst, acceleration, area, bending, bending_strength, dst_to_origin, go_phase, head_bends, head_x, head_y, is_coiled, is_well_oriented, left_bended, mom_dst, mom_x, mom_y, mov_direction, pause_turns, perimeter, peristalsis_efficiency, peristalsis_frequency, radius_1, radius_2, radius_3, right_bended, spine_length, spinepoint_1_x, spinepoint_1_y, spinepoint_2_x, spinepoint_2_y, spinepoint_3_x, spinepoint_3_y, stops, tail_x, tail_y, velocity

>>> # Plot traces over time
>>> ax = exp.plot_tracks()
>>> plt.show()

.. image:: img/tracks.png
   :width: 400px
   :alt: Tracks
   :align: left

>>> # Access a data table. Please note that some data tables are 2 dimensional
>>> # (e.g. velocity) while others are 1 dimensional (e.g. pause_turns)
>>> velocity = exp.velocity
>>> pause_turns = exp.pause_turns

>>> # Get the mean over all objects tracked
>>> mean_velocity = exp.mean('velocity')

>>> # Alternatively (for 2 dimensional data tables)
>>> mean_velocity = exp.velocity.mean(axis=0)

>>> # The second way also lets you get other metrics
>>> max_velocity = exp.velocity.max(axis=0)

>>> # Get all means over all parameters
>>> all_means = exp.mean()

>>> # We can also access data by objects
>>> # Get a list of tracked objects
>>> objects = exp.objects
>>> obj1_data = exp['object_1']

>>> # Get velocity for the 5 objects
>>> vel = exp.velocity.iloc[:,:5]
>>> # Smooth over 20 frames
>>> vel = vel.rolling(window=20).mean()
>>> # Plot over time
>>> ax = vel.plot(legend=False)
>>> ax.set_xlabel('frames')
>>> ax.set_ylabel('velocity')
>>> plt.show()

.. image:: img/velocity.png
   :width: 400px
   :alt: Velocity over time
   :align: left

>>> # Plot some frequency parameters over all objects
>>> param_to_plot = ['head_bends','pause_turns','stops']
>>> ax = exp.mean().loc[param_to_plot].T.plot(kind='box')
>>> ax.set_ylabel('freq [Hz]')
>>> plt.show()

.. image:: img/param_box.png
   :width: 400px
   :alt: Box plot of parameters
   :align: left

Next, lets have a look at `Collections`:

>>> import pyfim
>>> import matplotlib.pyplot as plt

>>> # Load CSV files from two folders
>>> exp1_folder = '/experiments/genotype1'
>>> exp2_folder = '/experiments/genotype2'

>>> exp1 = pyfim.Experiment(exp1_folder)
>>> exp2 = pyfim.Experiment(exp2_folder)

>>> # Initialise a Collection and add the Experiments
>>> coll = pyfim.Collection()
>>> coll.add_data(exp1, label='genotypeI')
>>> coll.add_data(exp2, label='genotypeII')

>>> # Get a summary of the Collection
>>> coll
... <class 'pyfim.core.Collection'> with 3 experiments: 
...          name  n_objects  n_frames
... 0   genotypeI         46      1800
... 1   genotypeI         46      1800
... 2  genotypeII         47      1800 
... Available parameters: tail_x, mom_dst, acc_dst, is_well_oriented, spinepoint_3_y, spine_length, right_bended, spinepoint_1_x, radius_2, peristalsis_frequency, radius_1, acceleration, spinepoint_1_y, area, head_bends, spinepoint_2_y, mom_y, go_phase, peristalsis_efficiency, bending_strength, spinepoint_2_x, tail_y, spinepoint_3_x, velocity, perimeter, pause_turns, head_x, mov_direction, left_bended, dst_to_origin, bending, head_y, is_coiled, radius_3, mom_x, stops

>>> # Get and plot a single parameter
>>> mean_acc_dst = coll.acc_dst
>>> ax = mean_acc_dst.plot(kind='box')
>>> ax.set_ylabel('accumulated distance')
>>> plt.show()

.. image:: img/acc_dst.png
   :width: 400px
   :alt: Box plot of parameters
   :align: left

>>> # Collections have a built-in plotting function that lets you plot  
>>> # multiple parameters as boxplots
>>> ax = coll.plot(['head_bends','pause_turns','stops'])
>>> plt.show()

.. image:: img/multi_box.png
   :width: 600px
   :alt: Box plot of parameters
   :align: left

Reference
=========

.. autosummary::
    :toctree: generated/

    ~pymaid.Experiment
    ~pymaid.Collection
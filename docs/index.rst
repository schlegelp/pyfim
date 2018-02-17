pyFIM
=====

:Release: |version|
:Date: |today|

pyFIM is a Python 3 package for analysis of `FIMTrack <https://www.uni-muenster.de/PRIA/en/FIM/download.shtml>`_ data. It extracts parameters 
from .csv files produced by FIMTrack, performs additional analyses and 
facilitates comparison of experiments. 

FIMTrack is an object tracker developed by Risse et al. (University of Muenster, Germany). From their Github `repository <https://github.com/i-git/FIMTrack>`_:

   "FIMTrack is a larval tracking program to acquire locomotion trajectories and conformation information of Drosophila melanogaster larvae. It is optimized for FIM images. FIM is an acronym for FTIR-based Imaging Method, whereby FTIR is the short form for Frustrated Total Internal Reflection."


Core Features
-------------

* import of .csv files
* extraction of FIMTrack parameters
* built-in additional high-level analyses
* easy handling and comparison of experiments 

Contribute
----------

Source Code: https://github.com/schlegelp/pyfim  

Issue Tracker: https://github.com/schlegelp/pyfim/issues

Support
-------

If you are having issues, drop me a message: pms70[AT]cam[DOT]ac[DOT]uk

License
---------

pyFIM is licensed under the GNU GPL v3+ license

Acknowledgments
---------------

Big thanks to Dimitri Berh, Benjamin Risse, Nils Otto and Christian Klämbt for 
sharing their MatLab code.

FIMTrack References
-------------------

Risse B, Berh D, Otto N, Klämbt C, Jiang X. FIMTrack: An open source tracking and locomotion analysis software for small animals. PLoS Computational Biology. 2017;13(5):e1005530. doi:10.1371/journal.pcbi.1005530.

Risse B, Otto N, Berh D, Jiang X, Klämbt C. FIM Imaging and FIMtrack: Two New Tools Allowing High-throughput and Cost Effective Locomotion Analysis. Journal of Visualized Experiments : JoVE. 2014;(94):52207. doi:10.3791/52207.

Risse B, Thomas S, Otto N, et al. FIM, a Novel FTIR-Based Imaging Method for High Throughput Locomotion Analysis. PLoS ONE. 2013;8(1):e53963. doi:10.1371/journal.pone.0053963.

Table of Contents
-----------------

.. toctree::
   :maxdepth: 1 
   
   source/install
   source/introduction   
   source/analysis   
   source/configure


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


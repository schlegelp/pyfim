Install
=======

Requirements
------------
pyFIM requires Python 3.3 or higher. 

Please make sure you have all these dependencies installed. They are all
available via PIP.

- `Pandas <http://pandas.pydata.org/>`_ >= 0.21.0
- `Numpy <http://www.scipy.org>`_ >= 1.13.3
- `PeakUtils <https://pypi.python.org/pypi/PeakUtils>`_ >= 1.1.0
- `tqdm <https://pypi.python.org/pypi/tqdm>`_ >= 4.15.0

.. note::
   If you are on Windows, it is probably easiest to install a scientific
   Python distribution such as
   `Anaconda <https://www.continuum.io/downloads>`_,
   `Enthought Canopy <https://www.enthought.com/products/canopy/>`_,
   `Python(x,y) <http://python-xy.github.io/>`_,
   `WinPython <https://winpython.github.io/>`_, or
   `Pyzo <http://www.pyzo.org/>`_.
   If you use one of these Python distribution, please refer to their online
   documentation.

Installation
------------

pyFIM is not listed in the Python Packaging Index but you can install
the current version directly from `Github <https://github.com/schlegelp/pyfim>`_ using:

::

   pip install git+git://github.com/schlegelp/pyfim@master

See `here <https://pip.pypa.io/en/stable/installing/>`_ how to get PIP.

Depending on your default Python version you may have to specify that you want
pyFIM to be installed for Python 3:

::

   pip3 install git+git://github.com/schlegelp/pyfim@master


Installing from source
----------------------

Alternatively, you can install pyFIM from source:

1. Download the source (tar.gz file) from
 https://github.com/schlegelp/pyfim/tree/master/dist

2. Unpack and change directory to the source directory
 (the one with setup.py).

3. Run :samp:`python setup.py install` to build and install


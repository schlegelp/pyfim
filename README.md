pyFIM
=====

Python 3 toolbox for analysing [FIM](http://fim.uni-muenster.de) data:

1. Read .csv files produced by [FIMTrack](https://www.uni-muenster.de/PRIA/en/FIM/download.shtml)
2. Merge individual files into experiments
3. Add experiments into collections
4. Analyse across experiments

FIMTrack CSV files contain a large selection of primary, secondary and
tertiary features (position, area, movement direction, length, etc). PyFIM
adds a few high-level analyses based on MatLab scripts by Dimitri Berh.

- pause-turn frequency
- stop frequency
- bending strength
- head bend frequency
- peristalsis frequency
- peristalsis efficiency

## Documentation

pyFIM is on [ReadTheDocs](http://pyfim.readthedocs.io)

## Acknowledgments
Big thanks to Dimitri Berh, Benjamin Risse, Nils Otto and Christian Klämbt for 
sharing their MatLab code.

## FIMTrack References
Risse B, Berh D, Otto N, Klämbt C, Jiang X. FIMTrack: An open source tracking and locomotion analysis software for small animals. PLoS Computational Biology. 2017;13(5):e1005530. doi:10.1371/journal.pcbi.1005530.

Risse B, Otto N, Berh D, Jiang X, Klämbt C. FIM Imaging and FIMtrack: Two New Tools Allowing High-throughput and Cost Effective Locomotion Analysis. Journal of Visualized Experiments : JoVE. 2014;(94):52207. doi:10.3791/52207.

Risse B, Thomas S, Otto N, et al. FIM, a Novel FTIR-Based Imaging Method for High Throughput Locomotion Analysis. PLoS ONE. 2013;8(1):e53963. doi:10.1371/journal.pone.0053963.

# RGASP3 coverage statistics pipeline

This repository contains the pipeline used for gathering and visualising feature coverage statistics for the [RGASP3](http://www.gencodegenes.org/rgasp/rgasp3.html) project. The pipeline is built around a modified version of the [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package.

## Files

## Dependencies

* A UNIX environment with standard GNU tools and make
* [python](http://www.python.org/) (>= 2.7.1)
* The modified [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package ([download](https://github.com/sbotond/paper-rgasp3-cov/blob/master/tools/HTSeq-0.5.3p3-rgasp3.tar.gz?raw=true)).
* [numpy](http://pypi.python.org/pypi/numpy/) (>= 1.6.1)
* [matplotlib](http://pypi.python.org/pypi/matplotlib/) (>= 1.1.0)

## Notes

* The logic for parsing the stranded paired-end reads (human datasets) is hard-coded in the parser class.


# RGASP3 coverage statistics pipeline

This repository contains the pipeline used for gathering and visualising feature coverage statistics for the [RGASP3](http://www.gencodegenes.org/rgasp/rgasp3.html) project. The pipeline is built around a modified version of the [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package.

## Files

* **bin** - scripts build directory.
* **config** - files with tab separated fields specifying the style and content of the generated plots.
* **lib/*.py** - python classes used by the scripts under bin/
* **plots** - plots output directory.
* **tools/HTSeq-0.5.3p3-rgasp3.tar.gz** - the modifed HTSeq python package used by the scripts.
* **Makefile** - makefile containing utility targets.
* **analysis.mk** - makefile containing analysis targets.
* **sr_*.py** - main tool source files.

## Dependencies

* A UNIX environment with standard [GNU tools](http://www.gnu.org/software/coreutils/manual/) and [make](http://www.gnu.org/software/make)
* [python](http://www.python.org/) (>= 2.7.1)
* The modified [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package ([download](https://github.com/sbotond/paper-rgasp3-cov/blob/master/tools/HTSeq-0.5.3p3-rgasp3.tar.gz?raw=true)).
* [numpy](http://pypi.python.org/pypi/numpy/) (>= 1.6.1)
* [matplotlib](http://pypi.python.org/pypi/matplotlib/) (>= 1.1.0)

## Building and using the tools

The following tools are being built under *bin/* by issuing *make*:

### annoparse
```
usage: annoparse [-h] -g gtf -l chromlens -p pickle_name [-s]
Parse and pickle annotation.
optional arguments:
  -h, --help      show this help message and exit
  -g gtf          Annotation in GFF format.
  -l chromlens    Chromosome list file (lengths ignored).
  -p pickle_name  Output pickle file.
  -s              Toggle stranded mode.
```

## Notes

* The logic for parsing the stranded paired-end reads (human datasets) is hard-coded in the parser class.


# RGASP3 coverage statistics pipeline

This repository contains the pipeline used for gathering and visualising feature coverage statistics for the [RGASP3](http://www.gencodegenes.org/rgasp/rgasp3.html) project. The pipeline is built around a modified version of the [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package.

## Files

* **bin** - scripts build directory.
* **config** - files with tab separated fields specifying the style and content of the generated plots.
* **lib/*.py** - python classes used by the scripts under bin/
* **plots** - plots output directory.
* **tools/HTSeq-0.5.3p3-rgasp3.tar.gz** - the modified HTSeq python package used by the scripts.
* **Makefile** - makefile containing utility targets.
* **analysis.mk** - makefile containing analysis targets.
* **sr_*.py** - main tool source files.

## Dependencies

* A UNIX environment with standard [GNU tools](http://www.gnu.org/software/coreutils/manual/) and [make](http://www.gnu.org/software/make)
* [python](http://www.python.org/) (>= 2.7.1)
* A modified version of the [HTSeq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html) package ([download](https://github.com/sbotond/paper-rgasp3-cov/blob/master/tools/HTSeq-0.5.3p3-rgasp3.tar.gz?raw=true)).
* [numpy](http://pypi.python.org/pypi/numpy/) (>= 1.6.1)
* [matplotlib](http://pypi.python.org/pypi/matplotlib/) (>= 1.1.0)
* The pipeline uses the Platform LSF workload manager to distribute the analysis between multiple compute nodes.

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

### covstat
```
usage: covstat [-h] [-g annot_pickle] [-p pickle_prefix] input file

Harness feature coverage statistics.

positional arguments:
  input file        Input BAM file.

optional arguments:
  -h, --help        show this help message and exit
  -g annot_pickle   Pickled annotation.
  -p pickle_prefix  Output directory.
```

### statvis
```
usage: statvis [-h] [-r report_pdf] -c color_file -m shape_file [-t title]
               [-vs vs_file] [-vc cross_file] [-vp pc_file] [-xvs]
               [input file [input file ...]]

Plot coverage statistics.

positional arguments:
  input file      Input pickled stats.

optional arguments:
  -h, --help      show this help message and exit
  -r report_pdf   Report PDF.
  -c color_file   Colors file.
  -m shape_file   Shapes file.
  -t title        Dataset title.
  -vs vs_file     Versus plots file.
  -vc cross_file  Cross plots file.
  -vp pc_file     Point correlation plots file.
  -xvs            Report list of valid stats.
```

### statdump
```
usage: statdump [-h] [-g global_stats_file] [-t tr_stats_file]
                [input file [input file ...]]

Dump primary alignment statistics.

positional arguments:
  input file            Input pickled stats.

optional arguments:
  -h, --help            show this help message and exit
  -g global_stats_file  Global stats file.
  -t tr_stats_file      Transcripts stats file.
```

## Using the pipeline

After setting the relevant parameters in *analysis.mk*, the pipeline can be run by calling the following make targets:
* **anno_parse** - parse and pickle alignments.
* **parse_sim** - parse simulated BAM files.
* **parse_mouse** - parse mouse BAM files.
* **parse_human** - parse human BAM files.
* **parse_human_stranded** - parse human BAM files in stranded mode.
* **plot_vs** - plot selected coverage statistics for all datasets.
* **plot_cross** - produce cross-dataset plots.
* **dump** - dump primary alignment statistics to tab separated files.

## Notes

* The logic for parsing the stranded paired-end reads (human datasets) is hard-coded in the parser class.


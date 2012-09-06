.PHONY: t

# Building tools:

tools: annoparse covstat statvis statdump

covstat: lib/* src_covstat.py
	@cat lib/preamble lib/*.py src_covstat.py > bin/covstat; chmod +x bin/covstat

annoparse: lib/* src_annoparse.py
	@cat lib/preamble lib/*.py src_annoparse.py > bin/annoparse; chmod +x bin/annoparse

t: covstat annoparse
	@bin/annoparse  -s -l t/test.sizes -g t/test.gtf -p t/annot.pk
	@bin/covstat -g t/annot.pk -p t t/test_1.bam 

tv: statvis
	@bin/statvis -vs config/vs_plots.tab -m config/style/methods.tab -c config/style/styles.tab -r t/test_report.pdf -t Test t/t-test_stranded_1.pk t/t-test_stranded_1.pk

td: statdump
	@bin/statdump t/t-test_stranded_1.pk t/t-test_stranded_1.pk

statvis: lib/* src_statvis.py
	@cat lib/preamble lib/*.py src_statvis.py > bin/statvis; chmod +x bin/statvis

statdump: lib/* src_statdump.py
	@cat lib/preamble lib/*.py src_statdump.py > bin/statdump; chmod +x bin/statdump

com:
	@git commit -a

include analysis.mk

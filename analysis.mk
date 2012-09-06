.PHONY: t

BASE			=/net/isilon4/research/bertone/external/RGASP3
REF_DIR			=$(BASE)/targets
PLOT_DIR		=plots

PICKLE_DIR		=$(BASE)/output/pickled_stats
LOG_DIR			=$(PICKLE_DIR)/log
HUMAN_PICK		=$(PICKLE_DIR)/human
S_HUMAN_PICK	=$(PICKLE_DIR)/human_stranded
MOUSE_PICK		=$(PICKLE_DIR)/mouse
SIM_PICK		=$(PICKLE_DIR)/sim

DATA_DIR		=/nfs/nobackup/research/bertone/external/RGASP3/resubm_std
BAM_DIR_NS		=$(DATA_DIR)/all_nameSorted
BAM_DIR_LS		=$(DATA_DIR)/all_locSorted

HUMAN_REF		=$(REF_DIR)/hg19.fa.gz
HUMAN_ANNOT		=$(REF_DIR)/Homo_sapiens.GRCh37.62.gtf.gz
HUMAN_SIZES		=$(REF_DIR)/hg19.sizes

HUMAN_ANNOT_PICK  	=$(PICKLE_DIR)/annot/human_annot.pk
S_HUMAN_ANNOT_PICK	=$(PICKLE_DIR)/annot/stranded_human_annot.pk

MOUSE_REF		=$(REF_DIR)/mm9.fa.gz
MOUSE_ANNOT		=$(REF_DIR)/Mus_musculus.NCBIM37.62.gtf.gz
MOUSE_ANNOT_PICK=$(PICKLE_DIR)/annot/mouse_annot.pk
MOUSE_SIZES		=$(REF_DIR)/mm9.sizes

SIM_BAMS		=$(shell find $(BAM_DIR_LS) -name "sim*.bam")
HUMAN_BAMS		=$(shell find $(BAM_DIR_LS) -name "LID*.bam")
MOUSE_BAMS		=$(shell find $(BAM_DIR_LS) -name "mouse*.bam")

SIM1_PICK       = $(shell find $(SIM_PICK) -name "*-sim1_*.pk")                                                                                                
SIM2_PICK       = $(shell find $(SIM_PICK) -name "*-sim2_*.pk")
HUMAN_PICK_LID16627 = $(shell find $(HUMAN_PICK) -name "*-LID16627_*.pk")
HUMAN_PICK_LID16628 = $(shell find $(HUMAN_PICK) -name "*-LID16628_*.pk")
HUMAN_PICK_LID8465  = $(shell find $(HUMAN_PICK) -name "*-LID8465_*.pk")
HUMAN_PICK_LID8466  = $(shell find $(HUMAN_PICK) -name "*-LID8466_*.pk")
HUMAN_PICK_LID8556  = $(shell find $(HUMAN_PICK) -name "*-LID8556_*.pk")
HUMAN_PICK_LID8557  = $(shell find $(HUMAN_PICK) -name "*-LID8557_*.pk")

S_HUMAN_PICK_LID16627 = $(shell find $(S_HUMAN_PICK) -name "*-LID16627_*.pk")
S_HUMAN_PICK_LID16628 = $(shell find $(S_HUMAN_PICK) -name "*-LID16628_*.pk")
S_HUMAN_PICK_LID8465  = $(shell find $(S_HUMAN_PICK) -name "*-LID8465_*.pk")
S_HUMAN_PICK_LID8466  = $(shell find $(S_HUMAN_PICK) -name "*-LID8466_*.pk")
S_HUMAN_PICK_LID8556  = $(shell find $(S_HUMAN_PICK) -name "*-LID8556_*.pk")
S_HUMAN_PICK_LID8557  = $(shell find $(S_HUMAN_PICK) -name "*-LID8557_*.pk")

DUMP_DIR_GLOB = $(BASE)/results/dumps/global
DUMP_DIR_TRS  = $(BASE)/results/dumps/trs_wise

ALL_PICKS	= $(shell find $(S_HUMAN_PICK) $(SIM_PICK) $(HUMAN_PICK) $(MOUSE_PICK) -name "*-*_*.pk")

CLUS			= research-rh6
PLT_ARGS		= -vs config/vs_plots.tab -m config/style/methods.tab -c config/style/styles.tab

anno_parse: tools
	bsub -q $(CLUS) "bin/annoparse  -l $(MOUSE_SIZES) -g $(MOUSE_ANNOT)    -p $(MOUSE_ANNOT_PICK)"
	bsub -q $(CLUS) "bin/annoparse  -l $(HUMAN_SIZES) -g $(HUMAN_ANNOT)    -p $(HUMAN_ANNOT_PICK)"
	bsub -q $(CLUS) "bin/annoparse  -l $(HUMAN_SIZES) -s -g $(HUMAN_ANNOT) -p $(S_HUMAN_ANNOT_PICK)"

parse_sim: $(SIM_BAMS) tools
	@for bam in $(SIM_BAMS);do bsub -M 30000 -R "rusage[mem=30000]" -q $(CLUS) -o /dev/null "bin/covstat -p $(SIM_PICK) -g $(HUMAN_ANNOT_PICK) $$bam 2>$(LOG_DIR)/`echo $$bam|sed 's|/|_|g'`.log" ; done

parse_human_stranded: $(HUMAN_BAMS) tools
	@for bam in $(HUMAN_BAMS);do bsub -M 30000 -R "rusage[mem=30000]" -q $(CLUS) -o /dev/null "bin/covstat -p $(S_HUMAN_PICK) -g $(S_HUMAN_ANNOT_PICK) $$bam 2>$(LOG_DIR)/`echo $$bam|sed 's|/|_|g'`_stranded.log" ; done

parse_human: $(HUMAN_BAMS) tools
	@for bam in $(HUMAN_BAMS);do bsub -M 30000 -R "rusage[mem=30000]" -q $(CLUS) -o /dev/null "bin/covstat -p $(HUMAN_PICK) -g $(HUMAN_ANNOT_PICK) $$bam 2>$(LOG_DIR)/`echo $$bam|sed 's|/|_|g'`.log" ; done

parse_mouse: $(MOUSE_BAMS) tools
	@for bam in $(MOUSE_BAMS);do bsub -M 30000 -R "rusage[mem=30000]" -q $(CLUS) -o /dev/null "bin/covstat -p $(MOUSE_PICK) -g $(MOUSE_ANNOT_PICK) $$bam 2>$(LOG_DIR)/`echo $$bam|sed 's|/|_|g'`.log" ; done

plot_human: $(HUMAN_PICK) tools
	@bin/statvis $(PLT_ARGS) -t LID16627 -r $(PLOT_DIR)/human_LID16627.pdf $(HUMAN_PICK_LID16627)	
	@bin/statvis $(PLT_ARGS) -t LID16628 -r $(PLOT_DIR)/human_LID16628.pdf $(HUMAN_PICK_LID16628)	
	@bin/statvis $(PLT_ARGS) -t LID8465  -r $(PLOT_DIR)/human_LID8465.pdf $(HUMAN_PICK_LID8465)	
	@bin/statvis $(PLT_ARGS) -t LID8466  -r $(PLOT_DIR)/human_LID8466.pdf $(HUMAN_PICK_LID8466)	
	@bin/statvis $(PLT_ARGS) -t LID8556  -r $(PLOT_DIR)/human_LID8556.pdf $(HUMAN_PICK_LID8556)	
	@bin/statvis $(PLT_ARGS) -t LID8557  -r $(PLOT_DIR)/human_LID8557.pdf $(HUMAN_PICK_LID8557)	

plot_human_stranded: $(HUMAN_PICK) tools
	@bin/statvis $(PLT_ARGS) -t LID16627_stranded -r $(PLOT_DIR)/human_LID16627_stranded.pdf $(S_HUMAN_PICK_LID16627)
	@bin/statvis $(PLT_ARGS) -t LID16628_stranded -r $(PLOT_DIR)/human_LID16628_stranded.pdf $(S_HUMAN_PICK_LID16628)
	@bin/statvis $(PLT_ARGS) -t LID8465_stranded  -r $(PLOT_DIR)/human_LID8465_stranded.pdf $(S_HUMAN_PICK_LID8465)
	@bin/statvis $(PLT_ARGS) -t LID8466_stranded  -r $(PLOT_DIR)/human_LID8466_stranded.pdf $(S_HUMAN_PICK_LID8466)
	@bin/statvis $(PLT_ARGS) -t LID8556_stranded  -r $(PLOT_DIR)/human_LID8556_stranded.pdf $(S_HUMAN_PICK_LID8556)
	@bin/statvis $(PLT_ARGS) -t LID8557_stranded  -r $(PLOT_DIR)/human_LID8557_stranded.pdf $(S_HUMAN_PICK_LID8557)

plot_sim: $(SIM_PICK) tools
	@bin/statvis  $(PLT_ARGS) -t "Simulated 1" -r $(PLOT_DIR)/sim1.pdf $(SIM1_PICK)	
	@bin/statvis  $(PLT_ARGS) -t "Simulated 2" -r $(PLOT_DIR)/sim2.pdf $(SIM2_PICK)	

plot_mouse: $(MOUSE_PICK) tools
	@bin/statvis  $(PLT_ARGS) -r $(PLOT_DIR)/mouse.pdf $(MOUSE_PICK)/*	

plot_vs: plot_sim plot_mouse plot_human plot_human_stranded

plot_cross: tools
	@bin/statvis -r $(PLOT_DIR)/cross_plots.pdf -vc config/cross_plots.tab -m config/style/methods.tab -c config/style/styles.tab $(ALL_PICKS)

PC_ARGS	= -vp config/pc_plots.tab -m config/style/methods.tab -c config/style/styles.tab

plot_pc: tools
	@bin/statvis -r $(PLOT_DIR)/pc_mouse.pdf 	$(PC_ARGS) 	$(MOUSE_PICK)/*
	@bin/statvis -r $(PLOT_DIR)/pc_sim1.pdf 	$(PC_ARGS)	$(SIM1_PICK)
	@bin/statvis -r $(PLOT_DIR)/pc_sim2.pdf 	$(PC_ARGS)	$(SIM2_PICK)
	@bin/statvis -r $(PLOT_DIR)/pc_LID16627.pdf $(PC_ARGS)	$(HUMAN_PICK_LID16627)
	@bin/statvis -r $(PLOT_DIR)/pc_LID16628.pdf $(PC_ARGS)	$(HUMAN_PICK_LID16628)
	@bin/statvis -r $(PLOT_DIR)/pc_LID8465.pdf 	$(PC_ARGS)	$(HUMAN_PICK_LID8465)
	@bin/statvis -r $(PLOT_DIR)/pc_LID8466.pdf 	$(PC_ARGS)	$(HUMAN_PICK_LID8466)
	@bin/statvis -r $(PLOT_DIR)/pc_LID8556.pdf 	$(PC_ARGS)	$(HUMAN_PICK_LID8556)
	@bin/statvis -r $(PLOT_DIR)/pc_LID8557.pdf 	$(PC_ARGS)	$(HUMAN_PICK_LID8557)

plots: plot_vs plot_cross 

dump: dump_sim dump_mouse dump_human dump_human_stranded

dump_sim: tools
	@bin/statdump -g $(DUMP_DIR_GLOB)/sim1.tab -t $(DUMP_DIR_TRS)/sim1 $(SIM1_PICK)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/sim2.tab -t $(DUMP_DIR_TRS)/sim2 $(SIM2_PICK)	

dump_mouse: tools
	@bin/statdump -g $(DUMP_DIR_GLOB)/mouse.tab -t $(DUMP_DIR_TRS)/mouse $(MOUSE_PICK)	

dump_human: tools
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID16627.tab -t $(DUMP_DIR_TRS)/human_LID16627 $(HUMAN_PICK_LID16627)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID16628.tab -t $(DUMP_DIR_TRS)/human_LID16628 $(HUMAN_PICK_LID16628)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID8465.tab -t $(DUMP_DIR_TRS)/human_LID8465 $(HUMAN_PICK_LID8465)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID8466.tab -t $(DUMP_DIR_TRS)/human_LID8466 $(HUMAN_PICK_LID8466)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID8556.tab -t $(DUMP_DIR_TRS)/human_LID8556 $(HUMAN_PICK_LID8556)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/human_LID8557.tab -t $(DUMP_DIR_TRS)/human_LID8557 $(HUMAN_PICK_LID8557)	
	
dump_human_stranded: tools
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID16627.tab -t $(DUMP_DIR_TRS)/s_human_LID16627 $(S_HUMAN_PICK_LID16627)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID16628.tab -t $(DUMP_DIR_TRS)/s_human_LID16628 $(S_HUMAN_PICK_LID16628)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID8465.tab -t $(DUMP_DIR_TRS)/s_human_LID8465 $(S_HUMAN_PICK_LID8465)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID8466.tab -t $(DUMP_DIR_TRS)/s_human_LID8466 $(S_HUMAN_PICK_LID8466)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID8556.tab -t $(DUMP_DIR_TRS)/s_human_LID8556 $(S_HUMAN_PICK_LID8556)	
	@bin/statdump -g $(DUMP_DIR_GLOB)/s_human_LID8557.tab -t $(DUMP_DIR_TRS)/s_human_LID8557 $(S_HUMAN_PICK_LID8557)	


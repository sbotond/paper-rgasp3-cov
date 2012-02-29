.PHONY: t

BASE			=/net/isilon4/research/bertone/external/RGASP3
REF_DIR			=$(BASE)/targets

PICKLE_DIR		=$(BASE)/output/pickled_stats
HUMAN_PICK		=$(PICKLE_DIR)/human
MOUSE_PICK		=$(PICKLE_DIR)/mouse
SIM_PICK		=$(PICKLE_DIR)/sim

DATA_DIR		=/nfs/nobackup/research/bertone/external/RGASP3/resubm_std
BAM_DIR_NS		=$(DATA_DIR)/all_nameSorted
BAM_DIR_NS		=$(DATA_DIR)/all_locSorted

HUMAN_REF		=$(REF_DIR)/hg19.fa.gz
HUMAN_ANNOT		=$(REF_DIR)/Homo_sapiens.GRCh37.62.gtf.gz

MOUSE_REF		=$(REF_DIR)/mm9.fa.gz
MOUSE_ANNOT		=$(REF_DIR)/Mus_musculus.NCBIM37.62.gtf.gz

TEST_DIR		=./test
TEST_ANNOT		=$(TEST_DIR)/test.gtf
TEST_BAM		=$(TEST_DIR)/test.bam

SIM_BAMS		=$(shell find $(DATA_DIR) -name "sim*.bam")
HUMAN_BAMS		=$(shell find $(DATA_DIR) -name "LID*.bam")
MOUSE_BAMS		=$(shell find $(DATA_DIR) -name "mouse*.bam")

parse_sim: $(SIM_BAMS)
	@for bam in $(SIM_BAMS);do ./annostat -d $(SIM_PICK) -g $(HUMAN_ANNOT) $$bam; done

parse_human: $(HUMAN_BAMS)
	@for bam in $(SIM_BAMS);do ./annostat -s -d $(HUMAN_PICK) -g $(HUMAN_ANNOT) $$bam; done

parse_mouse: $(MOUSE_BAMS)
	@for bam in $(MOUSE_BAMS);do ./annostat -d $(MOUSE_PICK) -g $(MOUSE_ANNOT) $$bam; done

t:
	./annostat  -s -d $(TEST_DIR) -g $(TEST_ANNOT) $(TEST_BAM) 

com:
	git commit -a

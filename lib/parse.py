import  HTSeq           as      ht
import  utils
import  stats

class Parse:
    def __init__(self, bam, annot, log):
        self.bam    = bam
        self.name   = utils.clean_name(bam)
        self.annot  = annot
        self.log    = log
        self.stranded   = self.annot.stranded

    def parse(self):
        self.log.log("Parsing alignments from: %s" % self.name)
        st      = stats.Stats(self.bam, self.name)
        reader  = ht.BAM_Reader(self.bam) 

        for aln in reader:
            # Unaligned read:
            if not aln.aligned:
                st.total_unaligned += 1
                continue
            # Secondary alignment:
            if aln.not_primary_alignment:
                self.process_alignment(aln, st.secondary_alns)
            # Primary alignment:
            else:
                self.process_alignment(aln, st.primary_alns)

        return st

    def invert_strand(self, iv):
        iv2 = iv.copy()
        if iv2.strand == "+":
            iv2.strand = "-"
        elif iv2.strand == "-":
            iv2.strand = "+"
        else:
            raise ValueError, "Illegal strand"
        return iv2

    def process_alignment(self, aln, sc):
        sc.total += 1

        # Process cigar:
        ivs     = [ ]
        split   = False 
        for op in aln.cigar:
            if op.type == "M":
                ref_iv  = op.ref_iv
                if self.stranded and aln.pe_which == "first":
                    ref_iv = self.invert_strand(ref_iv)
                ivs.append(op.ref_iv)
            elif op.type == "N":
                split   = True 

        genes, partial  = self.exon_overlaps(ivs)

        nr_genes    = float(len(genes))

        if nr_genes == 0.0:
        # Intergenic or intronic hit:

            intron_ov       = self.gene_overlaps(ivs)
            nr_intron_ov    = float(len(intron_ov))

            if nr_intron_ov > 0.0:
                # Intron overlaps:
                for gene in intron_ov:
                    if split:
                       sc.split_intron_cov[gene] += 1/nr_intron_ov
                    sc.intron_cov[gene] += 1/nr_intron_ov
            else:
                if split:
                    sc.split_intergenic_cov += 1 
                sc.intergenic_cov += 1 

        elif nr_genes > 0.0 and partial:
        # Partial exon hit:
            for gene in genes:
                sc.partial_exon_cov[gene]   = 1/nr_genes

        elif nr_genes > 0.0 and not partial:
        # Proper exon hit:
            for gene in genes:
                if split:
                    sc.split_exon_cov[gene] = 1/nr_genes
                sc.exon_cov[gene] = 1/nr_genes

        else:
        # Imossible:
            print >>sys.stderr, "Impossible branch"
            sys.exit(1)

    def exon_overlaps(self, ivs):
        """ Accumulate overlapping genes """
        genes   = set()
        partial = False
        exons   = self.annot.exons

        for iv in ivs:
           for s in exons[ iv ]:
                genes.update(s)
                # We have an empty interval:
                if len(s) == 0:
                    partial = True
        return (genes, partial) 

    def gene_overlaps(self, ivs):
        """ Accumulate overlapping genes """
        genes   = self.annot.genes 
        ov      = set()
        for iv in ivs:
            for s in genes[ iv ]:
                ov.update(s)
        return ov

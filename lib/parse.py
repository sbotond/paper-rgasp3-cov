
class Parse:
    """ Class for parsing alignments and gathering coverage statistics """
    def __init__(self, bam, annot, pdir, log):
        self.annot      = annot
        self.stranded   = self.annot['stranded']
        self.info       = self.parse_bam_path(bam)
        self.log        = log
        self.pdir       = pdir

    def parse_bam_path(self, bam_name):
        """ Parse BAM path """
        info             = {}
        info['bam_path'] = bam_name
        tmp              = bam_name.split(os.path.sep)
        info['group']    = tmp[-2]
        tmp              = tmp[-1].split('.')[0].split('_')
        info['dataset']  = tmp[0]
        if self.stranded:
            info['dataset'] = info['dataset'] + "_stranded"
        info['submission'] = tmp[1]
        return info

    def new_stats(self):
        """ Create new stats dict """
        st  = {
           'big_total':     0.0,
           'unaligned':     0.0,
           'aligned':       0.0,
           'prim':  {
                'type':         'prim',
                'total':        0.0,
                'exon':         defaultdict(float),
                'split_exon':   defaultdict(float),
                'part_exon':    defaultdict(float),
                'intron':       defaultdict(float),
                'inter':   0.0,
                'src_cov':   None,
            },

           'sec':  {
                'type':         'sec',
                'total':        0.0,
                'exon':         defaultdict(float),
                'split_exon':   defaultdict(float),
                'part_exon':    defaultdict(float),
                'intron':       defaultdict(float),
                'inter':   0.0,
                'src_cov':   None,
            },
        }
        return st

    def parse(self):
        """ Parse alignments """
        self.log.log("Parsing reads from BAM file: %s" % self.info['bam_path'])
        stats   = self.new_stats()
        reader  = ht.BAM_Reader(self.info['bam_path'])

        for aln in reader:
            # Increment total count:
            stats['big_total'] += 1
            if aln.aligned:
                # Increment aligned count:
                stats['aligned'] += 1
                if aln.not_primary_alignment: 
                    # Process as secondary alignment:
                    self.process_alignment(aln, stats['sec'])
                else:
                    # Process as primary alignment:
                    self.process_alignment(aln, stats['prim'])
            else:
                # Increment unaligned count:
                stats['unaligned'] += 1 

        # Calculate source coverage:
        stats['prim']['src_cov']  = self.tab_source_cov(stats['prim']['exon'])
        stats['sec']['src_cov']   = self.tab_source_cov(stats['sec']['exon'])
        self.stats                = stats
        # Check stats sanity:
        self.check_stats()

    def process_alignment(self, aln, st):
        """ Process a single alignment """
        st['total'] += 1

        # Check if alignment has a split operation:
        split               = self.is_split(aln)
        # Get match operation intervals:
        ivs                 = self.process_cigar(aln)
        # Serach for exon overlaps:
        exon_genes, partial = self.search_exons(ivs)

        # Register exon hits:
        nr_exon_genes   = float(len(exon_genes))
        # Proper exon hit:
        if nr_exon_genes > 0 and (not partial):
            for g in exon_genes:
                # Register exon hits:
                st['exon'][g] += 1.0/nr_exon_genes
                # Register split exon hits:
                if split:
                    st['split_exon'][g] += 1.0/nr_exon_genes
            return
        # Partial exon hit:
        if nr_exon_genes > 0 and partial:
            for g in exon_genes:
                st['part_exon'][g] += 1.0/nr_exon_genes
            return

        # Search for gene (intron) hits:
        intron_genes    = self.search_genes(ivs) 
        nr_intron_genes = float(len(intron_genes))
        
        # Register intron hits:
        if nr_intron_genes > 0:
            for g in intron_genes:
                st['intron'][g] += 1.0/nr_intron_genes
            return

        # Register intergenic hits:
        if nr_intron_genes == 0 and nr_exon_genes == 0:
            st['inter'] += 1
        else:
            self.log.fatal("Impossible branch")

    def process_cigar(self, aln):
        """ Process cigar operations """
        ivs     = set()
        for op in aln.cigar:
            if op.type != "M":
                continue
            ref_iv  = op.ref_iv
            if aln.pe_which not in ("first", "second"):
                self.log.fatal("Illegal pe_which attribute %s for %s" % (aln.pe_which, aln)) 
            # NOTE: invert the strand for the first read in stranded mode.
            # This is specific to the RGASP3 human datasets.
            if self.stranded and aln.pe_which == "first":
                ref_iv = self.invert_strand(ref_iv)
            ivs.add( ref_iv )
        return ivs

    def invert_strand(self, iv):
        """ Invert strand of a genomic interval """
        iv2 = iv.copy()
        if iv2.strand == "+":
            iv2.strand = "-"
        elif iv2.strand == "-":
            iv2.strand = "+"
        else:
            raise ValueError, "Illegal strand"
        return iv2

    def is_split(self, aln):
        """ Check if alignment has a split cigar operation """
        for op in aln.cigar:
            if op.type == "N":
                return True                
        return False

    def search_genes(self, ivs):
        """ Search for gene overlaps """
        genes = self.annot['genes']
        ovs   = set()
        for iv in ivs:
            for ov in genes[ iv ]:
                ovs.update(ov)
        return ovs

    def search_exons(self, ivs):
        """ Search for exon overlaps """
        exons   = self.annot['exons']
        genes   = set()
        partial = False 
        for iv in ivs:
            for ov in exons[ iv ]:
                genes.update(ov)
                if len(ov) == 0:
                    partial = True
        return genes, partial

    def check_stats(self):
        """ Stats sanity check """
        st                  = self.stats
        if st['big_total']  != (st['prim']['total'] + st['sec']['total'] + st['unaligned']):
            self.log.fatal("Big total is wrong!")
        self.check_sub_stat('prim')
        self.check_sub_stat('sec')
   
    def check_sub_stat(self, flv):
        """ Substats sanity check """
        s               = self.stats[flv]
        exon_hits       = sum(s['exon'].values())
        part_exon_hits  = sum(s['part_exon'].values())
        intron_hits     = sum(s['intron'].values())
        delta           = s['total'] - (exon_hits + part_exon_hits + intron_hits + s['inter'])
        if delta > 1.0:
            self.log.fatal("Detailed stats for %s are wrong: %g!" % (flv, delta))

    def tab_source_cov(self, h):
        """ Tabulate source coverage """
        src         = self.annot['sources']
        src_cov     = defaultdict(float)
        for name, cov in h.iteritems():
           src_cov[ src[name] ] += cov
        return src_cov

    def pickle_dump(self):
        """ Dump coverage statistics """
        self.name = "%s-%s_%s.pk" % (self.info['group'], self.info['dataset'], self.info['submission'])
        fh  = open(os.path.join(self.pdir, self.name), 'w')
        obj = {
            'info': self.info,
            'stats': self.stats,
        }
        cPickle.dump(obj, fh)

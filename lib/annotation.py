
class Annotation:
    """ Class for handling annotations """
    def __init__(self, log): 
        self.log    = log

    def load(self, gff, chrom_file, stranded):
        """ Load annotation from GFF file """
        reader      = ht.GFF_Reader(gff)
        chroms      = self.parse_chroms(chrom_file)
        exons       = self.new_gaos(chroms, stranded)
        genes       = self.new_gaos(chroms, stranded)
        sources     = { }
        
        gene_name, gene_iv  = None, None
        for feat in reader:
            # Skip non-exon features:
            if feat.type != "exon":
                continue
            # Register exon:
            exons[ feat.iv ] += feat.name
            # Register source:
            self.register_source(feat, sources)

            # Merge exons into genes:
            if gene_name is None:
                # New gene:
                gene_name   = feat.name
                gene_iv     = feat.iv
            elif gene_name == feat.name:
                # Internal exon:
                gene_iv     = self.merge_ivs(gene_iv, feat.iv)
            elif gene_name != feat.name:
                # Save gene:
                genes[ gene_iv ] += gene_name
                # New gene:
                gene_name   = feat.name
                gene_iv     = feat.iv
            else:
                self.log.fatal("Impossible branch!")
        # Register the very last gene:
        genes[ gene_iv ] += gene_name

        res = {
            'genes': genes,
            'exons': exons,
            'sources': sources,
            'stranded': stranded
        }
        return res

    def merge_ivs(self, a, b):
        """ Merge genomic intervals """
        if a.strand != b.strand:
            self.log("Strand mismatch when merging intervals!")
        iv      = a.copy()
        coords  = [a.start, a.end, b.start, b.end]
        iv.start   = min(coords)
        iv.end     = max(coords)
        if iv.length < 0:
            self.log("Negative iv length!")
        return iv

    def register_source(self, feat, src):
        """ Register feature source """
        if not feat.name in src:
            src[feat.name] = feat.source

    def new_gaos(self,chroms, stranded):
        """ Create a new genomic array of sets and add chromosomes """
        gaos       = ht.GenomicArrayOfSets(chroms="auto", stranded=stranded)
        for chrom in chroms.iterkeys():
            gaos.add_chrom(chrom)
        return gaos 

    def parse_chroms(self, fname):
        """ Parse chromosomes file """
        chroms  = {}
        for line in file(fname):
            chrom, length   = line.split()
            chroms[chrom]   = int(length)
        return chroms

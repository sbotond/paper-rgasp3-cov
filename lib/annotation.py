import      HTSeq       as      ht      
from        utils       import  merge_ivs

class Annotation:
    def __init__(self, gtf, stranded, log):
        self.log        = log
        self.gtf        = gtf
        self.stranded   = stranded
        self.load_features()

    def load_features(self):
        reader  = ht.GFF_Reader(self.gtf)
        if self.stranded:
            self.log.log("Loading stranded annotations from %s" % self.gtf)
            exons   = ht.GenomicArrayOfSets("auto", stranded=True)
            genes   = ht.GenomicArrayOfSets("auto", stranded=True)
        else:
            self.log.log("Loading non-stranded annotations from %s" % self.gtf)
            exons   = ht.GenomicArrayOfSets("auto", stranded=False)
            genes   = ht.GenomicArrayOfSets("auto", stranded=False)
        
        gene_name, gene_iv  = None, None
        for feature in reader:
            if feature.type != "exon":
                continue
            # Register exon:
            exons[ feature.iv ] += feature.name    

            # Register exon for gene:
            if gene_name == None:
                # First exon:
                gene_name, gene_iv  = feature.name, feature.iv
            elif gene_name == feature.name: 
                # Internal exon:
                gene_iv = merge_ivs(gene_iv, feature.iv)
            elif gene_name != feature.name:
                # New gene:
                genes[ gene_iv ] += gene_name
                gene_name, gene_iv  = feature.name, feature.iv
            else:
                self.log.fatal("Impossible branch!")
            
        # Register the last exon of the last gene:
        genes[gene_iv] += gene_name
       
        # Store annotations: 
        self.exons  = exons
        self.genes  = genes


from        collections     import      defaultdict
class AlnTypeStats:
    def __init__(self):
        self.total                  = 0

        self.exon_cov               = defaultdict(float)
        self.split_exon_cov         = defaultdict(float)
        self.partial_exon_cov       = defaultdict(float) 

        self.intron_cov             = defaultdict(float) 
        self.split_intron_cov       = defaultdict(float)

        self.intergenic_cov         = 0
        self.split_intergenic_cov   = 0

class Stats:
    def __init__(self, bam, name):
        self.bam    = bam
        self.name   = name

        self.total_unaligned    = 0
        self.primary_alns       = AlnTypeStats()
        self.secondary_alns     = AlnTypeStats()

    def sum_total(self):
        return ( self.sum_aligned() + self.sum_unaligned() )

    def sum_aligned(self):
        return ( self.primary_alns.total + self.secondary_alns.total )

    def sum_unaligned(self):
        return self.total_unaligned

    def get_sum(self, d):
        return sum(d.itervalues()) 

    def __repr__(self):
        s    = "Total records: %d\n" % self.sum_total()
        s   += "Total aligned: %d\n" % self.sum_aligned()
        s   += "Total unaligned: %d\n" % self.sum_unaligned()

        return s



        

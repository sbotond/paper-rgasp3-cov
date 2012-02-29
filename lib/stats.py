
class Stats:
    """ Class representing coverage statistics """
    def __init__(self, pickle=None, log=None):
        self.pickle = pickle
        self.log    = log
        self.st     = None
        self.info   = None
        if not pickle is None:
            self.load_pickle()

    def valid_stats(self):
        """ Return a dict of valid statistics """
        vs  = OrderedDict([ 
            ('big_total',        'Total number of records'),
            ('unaligned',        'Unaligned reads'),
            ('total',            'Total number of alignments'),
            ('exon',             'Proper exon hits'),
            ('exon_total',       'Proper and partial exon hits'),
            ('part_exon',        'Partial exon hits'),
            ('split_exon',       'Split exon hits'),
            ('intron',           'Intron hits'),
            ('inter',            'Intergenic hits'),
            ('genes_exon',       'Nr genes with proper exon hits'),
            ('genes_split_exon', 'Nr genes with split exon hits'),
            ('genes_part_exon',  'Nr genes with partial exon hits'),
            ('genes_intron',     'Nr genes with intron hits'),
            ('prop_exon',        'Proportion of exon hits'),
            ('prop_exon_total',  'Proportion of proper and partial exon hits'),
        ])
        return vs

    def print_valid_stats(self):
        """ Print valid stats """
        for name, desc in self.valid_stats().iteritems():
            print "%16s:\t%s" % (name, desc)

    def stat(self, name, flv='prim'):
        """ Return specified stat """
        desc    =   self.valid_stats()[name]
        note    =   ''
        if not (name in ('big_total','unaligned')):
            if flv == 'prim': note = ' (primary)'
            elif flv == 'sec': note = ' (secondary)'
        return (self._stat(name, flv), desc + note )        
        
    def _stat(self, name, flv='prim'): 
        """ Return specified stat """
        self.check_stat(name, flv)

        if name in ('big_total', 'unaligned'):
            return self._get_global(name)
        else:
            if name in ('total', 'inter'):
                return  self._get_substat(name, flv)
            elif name in ('exon','split_exon','part_exon','intron'):
                return self._get_sum(name, flv)
            elif name == 'genes_exon':
                return self._get_size('exon',flv)
            elif name == 'genes_part_exon':
                return self._get_size('part_exon',flv)
            elif name == 'genes_split_exon':
                return self._get_size('split_exon',flv)
            elif name == 'genes_intron':
                return self._get_size('intron',flv)
            elif name == 'prop_exon':
                return self._get_prop_exon(flv)
            elif name == 'exon_total':
                return ( self._get_sum('exon', flv) + self._get_sum('part_exon', flv) )
            elif name == 'prop_exon_total':
                return self._get_prop_exon_total(flv)
            else:
                self.log.fatal("Illegal stat type: %s" % name)

    def check_stat(self, name, flv):
        """ Check the validity of a specified stat """
        if not flv in ('prim', 'sec'):
            self.log.fatal("Invalid substat flavour: %s" % flv)

        if not name in self.valid_stats():
            self.log.fatal("Invalid substat: %s" % name)

    def src_cov(self, flv='prim'):
        """ Return source coverage dict """
        return self.st[flv]['src_cov']

    def _get_prop_exon(self, flv):
        eh  = self._get_sum('exon',flv)
        t   = self._get_substat('total',flv)
        return eh/float(t)

    def _get_prop_exon_total(self, flv):
        eh  = self._get_sum('exon',flv) + self._get_sum('part_exon',flv)
        t   = self._get_substat('total',flv)
        return eh/float(t)

    def _get_global(self, name):
        return self.st[name]

    def _get_substat(self, name, flv):
        return self.st[flv][name]

    def _get_size(self, name, flv):
        d   = self._get_substat(name, flv)
        return len(d)

    def _get_sum(self, name, flv):
        d   = self._get_substat(name, flv)
        return sum(d.values())

    def load_pickle(self):
        """ Load stats from pickle """
        fh       = open(self.pickle, 'r') 
        tmp      = cPickle.load(fh)
        fh.close()
        self.st     = tmp['stats']
        self.info   = tmp['info']

    def __repr__(self):
        i   = self.info
        st  = self.st
        s   =   "\n%s/%s-%s:\n" % (i['group'], i['dataset'], i['submission'])
        for name, desc in self.valid_stats().iteritems():
            note = ' (prim)'
            if name in ('big_total', 'unaligned'):
                note = ''
            st  = self.stat(name)
            s += "\t%s: %g\n" % (st[1], st[0])
        return s


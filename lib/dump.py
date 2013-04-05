
def print_head(vs, fh):
    """ Print global stats header to file handler """
    ids  = "group\tdataset\tsubmission\t" 
    ids  = ids + '\t'.join(map(str,vs.keys())) + "\n"
    fh.write(ids)

def dump_global(stats, fname):
    """ Dump global alignment statistics """
    fh  = open(fname, 'w')
    vs  = stats[0].valid_stats()
    print_head(vs, fh)
    tmp = []
    for st in stats:
        tmp = "%s\t%s\t%s" % (st.info['group'], st.info['dataset'], st.info['submission'])
        for i in vs.keys():
            tmp +=  "\t%s" % st.stat(i)[0]
        tmp += '\n'
        fh.write(tmp)
    fh.flush()
    fh.close()

def get_all_trs(stats, targets):
    """ Get the full set of transcripts across all statistics """
    trs = { }
    th  = defaultdict(dict)
    for tg in targets:
        for st in stats:
            th[st][tg] = st._get_substat(tg, 'prim')
            trs.update( th[st][tg] )
    return (trs.keys(), th)

def print_local_head(stats, fh):
    """ Print local stats header to a file handler """
    tmp = ''
    for st in stats:
        tmp  += "\t%s|%s|%s"  % (st.info['group'], st.info['dataset'], st.info['submission'])
    tmp += '\n'
    fh.write(tmp)

def dump_local(stats, fname):
    """ Dump primary alignment statistics (per stat) """
    targets = ['exon', 'split_exon', 'part_exon', 'intron']
    for tg in targets:
        fh      = open(fname+'_'+tg+".tab", 'w')
        print_local_head(stats, fh)
        trs, th = get_all_trs(stats, [tg])
        for tr in trs:
            fh.write(tr)
            for st in stats:
                fh.write("\t%s" % th[st][tg][tr])
            fh.write('\n')


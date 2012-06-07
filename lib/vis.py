
class Vis:
    """ Class for plotting stats """
    def __init__(self, stats, cfile, sfile, report, log):
        self.log    = log
        self.report = report
        self.cmap   = self.parse_cfile(cfile) 
        self.smap   = self.parse_sfile(sfile, self.cmap) 
        self.stats  = stats

    def parse_cfile(self, cfile):
        """ Parse style file """
        res = OrderedDict()
        for l in file(cfile):
            if l.startswith('#'):
                continue
            id, lty, pch    = l.strip().split("\t")
            res[id] = pch
        return res

    def parse_sfile(self, cfile, shape_map):
        """ Parse methods file """
        res = OrderedDict() 
        for l in file(cfile):
            if l.startswith('#'):
                continue
            name, team, number, desc, annot, color, style = l.strip().split("\t")
            res[(team,number)] = {
                'name': name,
                'desc': desc,
                'annot': annot,
                'color': color,
                'pch': shape_map[style],
            }
        return res 

    def tab_stat(self, stat, flv='prim'):
        """ Tabulate statistic """
        res = {}
        res['name'] = stat
        tmp = self.stats[0].stat(stat, flv)
        res['desc'] = tmp[1]

        groups      = []
        datasets    = []
        submissions = []
        data        = []

        for s in self.stats:
            groups.append( s.info['group'] )
            datasets.append( s.info['dataset'] )
            submissions.append( s.info['submission'] )
            data.append( s.stat(stat, flv)[0] )

        res['groups']       = groups
        res['datasets']     = datasets
        res['submissions']  = submissions
        res['data']         = data
        return res

    def plot_vs(self, f):
        """ Versus plot """
        for a,b in self._parse_vs_file(f):
            self._plot_vs(a, b)

    def plot_src_cov(self):
        """ Plot source coverage """
        ms  = 80
        types = ('protein_coding','pseudogene','processed_transcript')
        types = None
        st  = self._tab_src_cov(types)

        dataset = self.stats[0].info['dataset']
        shapes  = self.subm_to_shapes(zip(st['groups'],st['submissions']))
        sleg    = self.subm_to_sleg(zip(st['groups'],st['submissions']), ms=4)
        colors  = self.subm_to_colors(zip(st['groups'],st['submissions']))

        self.report.scatter_plot(x=st['x'], y=st['y'], area=ms, xticks=st['xticks'], colors=colors, shapes=shapes, xlab="Feature types", ylab="Coverage", title="Proper feature coverage by type (%s)" % dataset, sleg=sleg, fontsize=8, xtr=80)

    def plot_src_vs(self, src_type, stat, ms=80):
        """ Create versus plots """
        types = (src_type)
        st  = self._tab_src_cov(types)
        ss  = self.tab_stat(stat)

        x     = ss['data']
        y     = st['y']
        dataset = self.stats[0].info['dataset']
        shapes  = self.subm_to_shapes(zip(st['groups'],st['submissions']))
        sleg    = self.subm_to_sleg(zip(st['groups'],st['submissions']), ms=4)
        colors  = self.subm_to_colors(zip(st['groups'],st['submissions']))

        xlab    = ss['desc']
        ylab    = "Total proper %s hits (primary)" % src_type

        self.report.scatter_plot(x=x, y=y, area=ms, colors=colors, shapes=shapes, xlab=xlab, ylab=ylab, title=dataset, sleg=sleg, fontsize=8, xtr=80,cline=True)


    def _tab_src_cov(self, types):
        xticks  = OrderedDict()
        x       = []
        y              = []
        groups         = []
        submissions    = []
        for s   in self.stats:
            sc  = s.src_cov()
            for src, cov in sc.items():
                if types != None and src not in types:
                    continue
                x.append( self._update_xticks(src, xticks) )
                y.append( cov )
                groups.append( s.info['group'] )
                submissions.append( s.info['submission'] )
        res = {
            'x': x,
            'y': y,
            'xticks': xticks.keys(),
            'groups': groups,
            'submissions': submissions,
        }
        return res

    def _update_xticks(self, src, xticks):
        if not src in xticks:
            if len(xticks) == 0:
                xticks[src] = 1
            else:
                new_tick    = max(xticks.values()) + 1
                xticks[src] = new_tick
        return xticks[src]

    def _plot_vs(self, a, b):
        ms  =   80 
        ta  =   self.tab_stat(a)
        tb  =   self.tab_stat(b)

        title = ta['datasets'][0]
        xlab = ta['desc']
        x    = ta['data']
        ylab = tb['desc']
        y    = tb['data']
        gx   = ta['groups']
        gy   = tb['groups']
        lx   = ta['submissions']
        ly   = tb['submissions']
    
        if len(x) != len(y):
            self.log.fatal("vs_plot: data size mismatch")
        if tuple(gx) != tuple(gy):
            self.log.fatal("vs_plot: groups mismatch")
        groups  = gx
        if tuple(lx) != tuple(ly):
            self.log.fatal("vs_plot: labels mismatch")
        shapes  = self.subm_to_shapes(zip(gx,lx))
        colors  = self.subm_to_colors(zip(gx,lx))
        sleg    = self.subm_to_sleg(zip(gx,lx), ms=4)

        self.report.scatter_plot(x=x, y=y, area=ms, colors=colors, shapes=shapes, xlab=xlab, ylab=ylab, title=title, sleg=sleg, fontsize=8, cline=True)

    def subm_to_shapes(self, labels):
        """ Map submissions to shapes """
        return [ self.smap[x]['pch'] for x in labels]

    def subm_to_sleg(self, submissions, ms):
        """ Generate submission legend """
        res = {}
        for x in submissions:
           res[self.smap[x]['name']]   = plt.Line2D([0], [0], marker=self.smap[x]['pch'], ms=ms, color=self.smap[x]['color'], linestyle='', antialiased=True) 
        res_sorted = OrderedDict()
        for x in sorted(res.keys()):
            res_sorted[x] = res[x] 
        return res_sorted

    def subm_to_colors(self, g):
        """ Map groups to colors """
        return [ self.smap[x]['color'] for x in g ] 

    def _parse_vs_file(self, f):
        res = []
        for l in file(f):
            a, b    = l.split()
            for x in (a, b):
                if not x in self.stats[0].valid_stats():
                    self.log.fatal("Invalid stat type: %s" % x)
            res.append( (a,b) )
        return res

    def cross_plots(self, f):
        """ Produce cross-dataset plots """
        vs  = self._parse_cross_file(f)
        [ self._cross_plot(i) for i in vs ]

    def _cross_plot(self, p, ms=80):
        d   = self._cross_tabulate(p[0], p[1], p[2], p[3])

        title   = d['desc']
        xlab    = d['ds1']
        ylab    = d['ds2'] 
        x       = d['d1']
        y       = d['d2']
        groups  = d['groups']
        submissions = d['submissions']

        shapes  = self.subm_to_shapes(zip(groups,submissions))
        colors  = self.subm_to_colors(zip(groups,submissions))
        sleg    = self.subm_to_sleg(zip(groups,submissions), ms=4)
        
        self.report.scatter_plot(x=x, y=y, area=ms, colors=colors, shapes=shapes, xlab=xlab, ylab=ylab, title=title, sleg=sleg, fontsize=8,cline=True)

    def _cross_tabulate(self, stat, flv, s1, s2):
        groups          = []
        submissions     = []
        d1              = []
        d2              = []
        t1, t2  = {}, {}
        for s in self.stats:
            ds  = s.info['dataset']
            if ds == s1:
                grp, sbm = s.info['group'], s.info['submission']
                t1[(grp, sbm)], desc  = s.stat(stat, flv)
            if ds == s2:
                grp, sbm = s.info['group'], s.info['submission']
                t2[(grp, sbm)], desc  = s.stat(stat, flv)
        points  = set(t1.keys()).intersection(set(t2.keys()))
        for p in points:
            groups.append( p[0] )
            submissions.append( p[1] )
            d1.append( t1[p] )
            d2.append( t2[p] )
        res = {
            'desc': desc,
            'groups': groups,
            'submissions': submissions,
            'd1': d1,
            'd2': d2,
            'ds1': s1,
            'ds2': s2,
        }
        return res
    
    def _parse_cross_file(sel, f):
        return [ tuple(l.split()) for l in file(f) ]

    def pc_plots(self, f, flv='prim'):
        """ Produce point correlation plots """
        pc  = [ tuple(l.split()) for l in file(f) ]
        for s in self.stats:
            for p in pc: 
                self._pc_plot(s,p, flv) 

    def _pc_plot(self, s, p, flv):
        F   = {'prim': '(primary)', 'sec': '(secondary)'}
        #title   =   "%s: %s %s" % (s.info['dataset'], self._descore(s.info['group']), s.info['submission'])
        title   =   self.smap[(st.info['group'],st.info['submission'])]
        xlab    =   'Log ' + s.valid_stats()[p[0]].lower() + ' ' + F[flv]
        ylab    =   'Log ' + s.valid_stats()[p[1]].lower() + ' ' + F[flv]
        dx      =   s.st[flv][p[0]]
        dy      =   s.st[flv][p[1]]
        points  =   set(dx.keys()).intersection( set(dy.keys()) )
        x, y    =   [], []
        for i in points:
            x.append( np.log(dx[i]) )
            y.append( np.log(dy[i]) )
        a   = min(min(x), min(y))
        b   = max(max(x), max(y))
        z   = np.arange(a,b)
        m, ms   = 'b.', 3
        fig = plt.figure()
        plt.plot(x,y,m,ms=ms)
        plt.plot(z,z,'r-',lw=0.5)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        self.report.pages.savefig(fig)
        plt.close(fig)


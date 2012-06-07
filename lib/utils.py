
class Report:
    """ Class for plotting reports """
    def __init__(self, pdf):
        self.pdf    = pdf
        self.pages  = PdfPages(pdf)

    def plot_array(self, y, title="", xlab="", ylab=""):
        """ Visualise  array as a bar plot """
        fig = plt.figure()
        plt.bar(np.arange(len(y)),y,width=0.1)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        self.pages.savefig(fig)

    def plot_arrays(self,x, y, title="", xlab="", ylab=""):
        """ Visualise  array as a bar plot """
        fig = plt.figure()
        plt.bar(x,y,width=0.1)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        self.pages.savefig(fig)

    def plot(self,x, y,m,title="", xlab="", ylab="",ms=5):
        """ Simple XY plot """
        fig = plt.figure()
        plt.plot(x,y,m,ms=ms)
        plt.xlabel(xlab)
        plt.ylabel(ylab)
        plt.title(title)
        self.pages.savefig(fig)

    def scatter_plot(self, x, y, colors, shapes, xlab="", ylab="", title="", labels=None, sleg=None, area=10, xticks=None, yticks=None, fontsize=8, linewidth=0.5, alpha=0.8, legend_loc='center left', xtr=0, ytr=0, cline=False, plot_leg=False):
        fig = plt.figure()
        ax      = plt.subplot(111)

        # Plot markers:
        for i in xrange(len(x)):
            sct = ax.scatter(x[i], y[i], marker=shapes[i], c=colors[i], s=area, linewidth=linewidth, edgecolor='k')
            sct.set_alpha(alpha)

        # Plot x tick labels:
        if xticks != None:
            ax.set_xticks(x)
            ax.set_xticklabels(xticks, rotation=xtr, fontsize='x-small') 
        # Plot y tick labels:
        if yticks != None:
            ax.set_yticks(y)
            ax.set_yticklabels(yticks, rotation=ytr, fontsize='x-small') 


        if plot_leg:
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.87, box.height])

            leg     = ax.legend(sleg.values(), sleg.keys(), loc=legend_loc, bbox_to_anchor=(1, 0.5))
            ltext   = leg.get_texts()
            plt.setp(ltext, fontsize='xx-small')

        # Print linear regression line:
        if cline:
            slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(np.array(x),np.array(y))
            xs, xe  = float(min(x)), float(max(x))
            if xs == xe:
                xs, xe = float(min(x)), float(min(x)) + 100
            cx      = np.arange(xs, xe, (xe - xs)/100)
            cy      = intercept + slope * cx
            plt.plot(cx, cy, 'r-', lw=0.5)
            title   += " (r=%g, p=%g)" % (r_value, p_value)

        plt.xlabel(xlab, fontsize=12)
        plt.ylabel(ylab, fontsize=12)
        plt.title(title, fontsize=12)
        self.pages.savefig(fig)
        plt.clf()
        plt.close(fig)

    def close(self):
        self.pages.close()

    def __del__(self):
        self.close()

class Log:
    """ Logging utility class """
    def __init__(self, fname=None, level=0):
        self.level = level
        if fname == None:
            self.fname  = "<sys.stderr>"     
            self.file   = sys.stderr
        else:
            self.file   = open(fname, "w")
            self.fname  = fname

    def close(self):
        self.file.flush()
        self.file.close()

    def log(self, message):
        if self.level < 0:
            return
        self.file.write("[%s] %s\n" % (time.strftime("%y-%m-%d %H:%M:%s"), message) )

    def fatal(self, message):
        self.file.write("[%s] %s\n" % (time.strftime("%y-%m-%d %H:%M:%s"), message) )
        sys.exit(1)

def pickle_dump(obj, fname):
    """ Pickle object to file """
    fh  = open(fname, "w")
    cPickle.dump(obj, fh)
    fh.flush()
    fh.close()
    return fname

def pickle_load(fname):
    """ Load object from pickle """
    return cPickle.load(file(fname))


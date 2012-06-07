
def parse_arguments():
    """ Parse arguments """
    parser = argparse.ArgumentParser(description='Plot coverage statistics.')
    parser.add_argument('input_files', metavar='input file', type=str, nargs='*',default=None,
                   help='Input pickled stats.')
    parser.add_argument('-r', metavar='report_pdf', type=str, default="statvis.pdf", help='Report PDF.')
    parser.add_argument('-c', metavar='style_file', type=str, default=None, help='Style file.', required=True)
    parser.add_argument('-m', metavar='methods_file', type=str, default=None, help='Methods file.', required=True)
    parser.add_argument('-t', metavar='title', type=str, default="Dataset", help='Dataset title.')
    parser.add_argument('-vs', metavar='vs_file', type=str, default=None, help='Versus plots file.')
    parser.add_argument('-vc', metavar='cross_file', type=str, default=None, help='Cross plots file.')
    parser.add_argument('-vp', metavar='pc_file', type=str, default=None, help='Point correlation plots file.')
    parser.add_argument('-xvs', action='store_true' ,default=False, help='Report list of valid stats.')
    args            = parser.parse_args()
    if type(args.input_files) != list:
        args.input_files = [ args.input_files ]
    return args

args    = parse_arguments()
L       = Log()
R       = Report(args.r)

# Print list of valid statistics:
if args.xvs:
    Stats().print_valid_stats()
    sys.exit(0)

if len(args.input_files) == 0:
    print >>sys.stderr, "No input files specified!"
    sys.exit(0)

# Load statistics from pickled files:
stats   = [ ]
for f in args.input_files:
    stats.append( Stats(f, L) )

v   = Vis(stats, args.c, args.m, R, L)

# Versus plots:
if not args.vs is None:
    v.plot_vs(args.vs)
    v.plot_src_cov()
    v.plot_src_vs('protein_coding','total')
    v.plot_src_vs('pseudogene','total')
    v.plot_src_vs('processed_transcript','total')

# Cross-dataset plots:
if args.vc != None:
    v.cross_plots(args.vc)

# PC plots:
if args.vp != None:
    v.pc_plots(args.vp)


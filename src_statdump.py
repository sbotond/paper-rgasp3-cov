
def parse_arguments():
    """ Parse arguments """
    parser = argparse.ArgumentParser(description='Dump primary alignment statistics.')
    parser.add_argument('input_files', metavar='input file', type=str, nargs='*',default=None,
                   help='Input pickled stats.')
    parser.add_argument('-g', metavar='global_stats_file', type=str, default="global_stats.tab", help='Global stats file.')
    parser.add_argument('-t', metavar='tr_stats_file', type=str, default="tr_stats.tab", help='Transcripts stats file.')
    args            = parser.parse_args()
    if type(args.input_files) != list:
        args.input_files = [ args.input_files ]
    return args

args    = parse_arguments()
L       = Log()

if len(args.input_files) == 0:
    print >>sys.stderr, "No input files specified!"
    sys.exit(0)

# Load statistics from pickled files:
stats   = [ ]
for f in args.input_files:
    stats.append( Stats(f, L) )

dump_global(stats, args.g)
dump_local(stats, args.t)


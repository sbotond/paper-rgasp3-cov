
def parse_arguments():
    """ Parse arguments """
    parser = argparse.ArgumentParser(description='Harness feature coverage statistics.')
    parser.add_argument('input_file', metavar='input file', type=str, nargs=1, default=None, help='Input BAM file.')
    parser.add_argument('-g', metavar='annot_pickle', type=str, default="", help='Pickled annotation.')
    parser.add_argument('-p', metavar='pickle_prefix', type=str, default="", help='Output directory.')
    args            = parser.parse_args()
    args.input_file = args.input_file[0]
    return args

args        = parse_arguments()
input_file  = args.input_file 
annot_file  = args.g
outdir      = args.p
L           = Log()

annot   = pickle_load(annot_file)
parser  = Parse(input_file, annot, outdir, L)
parser.parse()
parser.pickle_dump()


def parse_arguments():
    """ Parse arguments """
    parser = argparse.ArgumentParser(description='Parse and pickle annotation.')
    parser.add_argument('-g', metavar='gtf', type=str, help='Annotation in GFF format.', required=True)
    parser.add_argument('-l', metavar='chromlens', type=str, help='Chromosome list file (lengths ignored).', required=True)
    parser.add_argument('-p', metavar='pickle_name', type=str, help='Output pickle file.', required=True)
    parser.add_argument('-s', action='store_true' ,default=False, help='Toggle stranded mode.')
    args = parser.parse_args()
    return args

args    = parse_arguments()
L       = Log()

gff_file    = args.g
chroms_file = args.l
pickle_name = args.p
stranded    = args.s

parser  = Annotation(L)
annot   = parser.load(gff_file, chroms_file, stranded)
pickle_dump(annot, pickle_name)


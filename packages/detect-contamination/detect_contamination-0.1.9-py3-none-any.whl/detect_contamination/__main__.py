import argparse
import sys 
import os
import subprocess
from detect_contamination.detect import detection
from detect_contamination.index_builder import build_index
from detect_contamination.table import table
from detect_contamination.graph import draw

def parse_args():

    parser = argparse.ArgumentParser(
        description="Detect contamination in an assembly"
    )

    subparsers = parser.add_subparsers()

    # PARSER FOR BUILD
    parser_build = subparsers.add_parser(
        "build", help="Build up an index containing information about genomes you want to search against"
    )

    parser_build.add_argument(
        "genomes",
        metavar="GENOMES",
        type=str,
        help="a concatenated file containing the sequences you want to include in the index"
    )

    parser_build.add_argument(
        "taxonomy_tree",
        metavar="NODES",
        type=str,
        help="`\t|\t`-separated file mapping taxonomy IDs to their parents and rank, up to the root of the tree. When using NCBI taxonomy IDs, this will be the `nodes.dmp` from `ftp://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxdump.tar.gz`."
    )

    parser_build.add_argument(
        "name_table",
        metavar="NAMES",
        type=str,
        help="'\t|\t'-separated file mapping taxonomy IDs to a name. A further column (typically column 4) must specify `scientific name`. When using NCBI taxonomy IDs, `names.dmp` is the appropriate file."
    )

    parser_build.add_argument(
        "index_prefix",
        metavar="INDEX",
        type=str,
        help="the prefix for the index files that will be generated, will have format: (index_name).1.cf, (index_name).2.cf ..."
    )

    parser_build.add_argument(
        "--threads",
        type=int,
        default=os.cpu_count(),
        help="the number of threads to use. This will be passed on to centrifuge-build which will use that many search threads"
    )

    parser_build.add_argument(
        "--conversion_table",
        type=str,
        default=None,
        help="a file mapping sequence ids (from the genomes file) to their corresponding taxonomic id, if specified, the program will use this instead of automatically generating this file"
    )

    parser_build.set_defaults(func=build_index)

    # PARSER FOR DETECT
    parser_detect = subparsers.add_parser(
        "detect", help="Detect the contamination in the provided genomes"
    )

    parser_detect.add_argument(
        "contaminated",
        metavar="ASSEMBLY",
        type=str,
        help=" this is the assembly file, that will be ran against the index to determine its composition"
    )

    parser_detect.add_argument(
        "index",
        metavar="INDEX",
        type=str,
        help="this is the prefex of the index files that the user wishes to search against"
    )

    parser_detect.add_argument(
        "--fragment_length",
        type=int,
        default=150,
        help="the length of the fragments"
    )

    parser_detect.add_argument(
        "--overlap_length",
        type=int,
        default=0,
        help="how much each adjacent fragment will overlap by"
    )


    parser_detect.add_argument(
        "--output_file",
        type=str,
        default="result.png",
        help="the name of the output file that the pie chart will be placed in, will be ignored if graphical output is not specified"
    )


    parser_detect.add_argument(
        "--graphical_output",
        action="store_true",
        help="output the results as a pie chart, if not specified, the reuslts will be printed as a table"
    )

    parser_detect.add_argument(
        "--threads",
        type=int,
        default=os.cpu_count(),
        help="the number of threads to use. This will be passed on to centrifuge which will use that many search threads"
    )

    parser_detect.set_defaults(func=detection)

    return parser.parse_args()


def main():

    # centrifuge is not installed locally
    path_command = subprocess.run('which centrifuge', 
                                    shell=True, 
                                    capture_output=True
                                )

    if (path_command.returncode != 0):
        raise Exception("centrifuge is not installed or initialised")

    args = parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
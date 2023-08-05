import argparse
from detect_contamination.detect_contamination import detect_contamination
from detect_contamination.table import table
from detect_contamination.graph import draw

def detection(args: argparse.Namespace):
    results = detect_contamination(args)

    if (args.graphical_output):
        draw(results, args.output_file)
    else:
        table(results)

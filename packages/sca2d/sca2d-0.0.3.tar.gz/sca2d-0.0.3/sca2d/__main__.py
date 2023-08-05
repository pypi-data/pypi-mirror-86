'''The entry point for SCA2D. This file runs when you run `sca2d` in terminal'''

import sys
import argparse
from sca2d import Analyser

def parse_args():
    """
    This sets up the argumant parsing using the argparse module. It will automatically
    create a help message describing all options. Run `sca2d -h` in your terminal to see
    this description.
    """
    parser = argparse.ArgumentParser(description="SCA2D - A static code analyser for OpenSCAD.")
    parser.add_argument("filename",
                        metavar="<filename>",
                        type=str,
                        help="The .scad file to analyse.")
    parser.add_argument("--output-tree",
                        help="Output the parse tree to output.sca2d",
                        action="store_true")
    return parser.parse_args()

def main():
    '''
    creates a sca2d analyser and then analyses the input file. Printing
    analysis to the screen
    '''
    args = parse_args()
    analyser = Analyser()
    parsed = analyser.analyse_file(args.filename, output_tree=args.output_tree)
    if parsed:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

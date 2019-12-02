#!/usr/bin/env python3

"""
This program generates Devicetree overlays given the devicetree for the core
"""

import argparse
import os
import sys

import testbench

SUPPORTED_TYPES = ["rtl"]

def main():
    """Parse arguments and generate overlay"""
    arg_parser = argparse.ArgumentParser(description="Generate Devicetree overlays")

    arg_parser.add_argument("-t", "--type", required=True,
                            help="The type of the target to generate an overlay for. \
                                Supported types include: testbench")
    arg_parser.add_argument("-o", "--output",
                            help="The name of the output file. If not provided, \
                                  the overlay is printed to stdout.")
    arg_parser.add_argument("dts", help="The devicetree for the target")

    parsed_args = arg_parser.parse_args(sys.argv[1:])

    if parsed_args.type not in SUPPORTED_TYPES:
        print("Type '%s' is not supported, please choose one of: %s" % (parsed_args.type,
                                                                        ', '.join(SUPPORTED_TYPES)))
        sys.exit(1)

    try:
        os.stat(parsed_args.dts)
    except FileNotFoundError:
        print("Could not find file '%s'" % parsed_args.dts)
        sys.exit(1)

    if parsed_args.type == "rtl":
        overlay = testbench.generate_overlay(parsed_args.dts)

    if parsed_args.output:
        with open(parsed_args.output, "w") as output_file:
            output_file.write(overlay)
    else:
        print(overlay)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

"""
This program generates Devicetree overlays given the devicetree for the core
"""

import argparse
import os
import sys

import pydevicetree

import testbench
import arty

SUPPORTED_TYPES = ["rtl", "arty"]

def main():
    """Parse arguments and generate overlay"""
    arg_parser = argparse.ArgumentParser(description="Generate Devicetree overlays")

    arg_parser.add_argument("-t", "--type", required=True,
                            help="The type of the target to generate an overlay for. \
                                Supported types include: rtl, arty")
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

    tree = pydevicetree.Devicetree.parseFile(parsed_args.dts)

    overlay = pydevicetree.Devicetree.from_dts("""
    /include/ "%s"
    / {
        chosen {};
    };
    """ % parsed_args.dts)

    if parsed_args.type == "rtl":
        testbench.generate_overlay(tree, overlay)
    elif parsed_args.type == "arty":
        arty.generate_overlay(tree, overlay)

    if parsed_args.output:
        with open(parsed_args.output, "w") as output_file:
            output_file.write(overlay.to_dts())
    else:
        print(overlay)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

import sys

import pydevicetree

from all_targets import PORTS, CAP_SIZE_FOR_VCS
from all_targets import number_to_cells, set_boot_hart, set_stdout, set_entry

def attach_testrams(tree, overlay):
    """Generate testrams attached to ports in the overlay

    Attached rams are also created in the in-memory tree so that they can be queried as if the
    overlay has been applied.
    """
    testram_count = 0
    for port in tree.match("sifive,.*port"):
        ranges = port.get_ranges()
        address = ranges[0][0]
        size = min(ranges[0][2], CAP_SIZE_FOR_VCS)

        num_address_cells = port.get_field("#address-cells")
        num_size_cells = port.get_field("#size-cells")

        address_cells = number_to_cells(address, num_address_cells)
        size_cells = number_to_cells(size, num_size_cells)

        port.children.append(pydevicetree.Node.from_dts("""
            testram%d: testram@%x {
                compatible = "sifive,testram0";
                reg = <%s %s>;
                reg-names = "mem";
            };
        """ % (testram_count, address, address_cells, size_cells)))
        overlay.children.append(pydevicetree.Node.from_dts("""
        &%s {
            testram%d: testram@%x {
                compatible = "sifive,testram0";
                reg = <%s %s>;
                reg-names = "mem";
            };
        };
        """ % (port.label, testram_count, address, address_cells, size_cells)))

        testram_count += 1

def get_boot_rom(tree):
    """Given a tree with attached testrams, return the testram which contains the default reset
    vector"""
    port_compatibles = list(map(lambda n: n.get_field("compatible"), tree.match("sifive,.*-port")))
    for port in PORTS:
        if port in port_compatibles:
            return tree.match(port)[0].match("sifive,testram0")[0]
    sys.stderr.write("%s: Unable to determine test bench reset vector\n" % sys.argv[0])
    sys.exit(1)

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    attach_testrams(tree, overlay)

    bootrom = get_boot_rom(tree)
    if bootrom is not None:
        set_entry(overlay, bootrom, 0)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 100000000)

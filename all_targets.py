#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
These constants and functions are useful for all target types
"""

import itertools

import pydevicetree

PORT_PROTOCOLS = [
    "ahb",
    "apb",
    "axi4",
    "tl",
]

PORT_TYPES = [
    "periph",
    "sys",
    "mem",
]

# The resulting order of the contents of PORTS is sensitive and should not be modified without
# first consulting the RTL testbench developers or RTL simulation will break.
PORTS = ["sifive,%s-%s-port" % (protocol, port_type) \
             for protocol, port_type in itertools.product(PORT_PROTOCOLS, PORT_TYPES)]

CAP_SIZE_FOR_VCS = 0x1fffffff

STDOUT_DEVICES = [
    "sifive,uart0",
    "sifive,trace",
    "ucb,htif0",
]

def set_entry(overlay, node, offset):
    """Set entry vector in overlay"""
    chosen = overlay.get_by_path("/chosen")
    chosen.properties.append(pydevicetree.Property.from_dts("metal,entry = <&%s %d>;" % \
                                                            (node.label, offset)))

def get_boot_hart(tree):
    """Given a tree, return the node which should be used as the boot hart"""
    riscv_harts = tree.match("^riscv$")
    for hart in riscv_harts:
        if hart.get_reg()[0][0] == 1:
            return hart
    return riscv_harts[0]

def set_boot_hart(tree, overlay):
    """Set boot hart in overlay"""
    chosen = overlay.get_by_path("/chosen")
    chosen.properties.append(pydevicetree.Property.from_dts("metal,boothart = <&" + \
                                                            get_boot_hart(tree).label + ">;"))

def number_to_cells(num, num_cells):
    """Convert an integer into 32-bit cells"""
    cells = []
    for i in range(num_cells):
        cells.insert(0, (0xFFFFFFFF & (num >> (32 * i))))
    return " ".join(["0x%x" % x for x in cells])

def get_stdout(tree):
    """Given a tree, return teh node which should be used as stdout"""
    for compat in STDOUT_DEVICES:
        nodes = tree.match(compat)
        if len(nodes) > 0:
            return nodes[0]
    return None

def set_stdout(tree, overlay, baudrate):
    """Set the stdout path and baud rate"""
    chosen = overlay.get_by_path("/chosen")
    stdout = get_stdout(tree)
    if stdout is not None:
        chosen.properties.append(
            pydevicetree.Property.from_dts("stdout-path = \"%s:%d\";" % \
                    (stdout.get_path(), baudrate)))

#!/usr/bin/env python3

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

import itertools
import sys

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

def get_boot_hart(tree):
    """Given a tree, return the node which should be used as the boot hart"""
    riscv_harts = tree.match("^riscv$")
    for hart in riscv_harts:
        if hart.get_reg()[0][0] == 1:
            return hart
    return riscv_harts[0]

def attach_testrams(tree, overlay):
    """Generate testrams attached to ports in the overlay

    Attached rams are also created in the in-memory tree so that they can be queried as if the
    overlay has been applied.
    """
    testram_count = 0
    for port in tree.match("sifive,.*port"):
        ranges = port.get_ranges()
        child_address = ranges[0][1]
        size = min(ranges[0][2], CAP_SIZE_FOR_VCS)

        port.children.append(pydevicetree.Node.from_dts("""
            testram%d: testram@%x {
                compatible = "sifive,testram0";
                reg = <0x%x 0x%x>;
                reg-names = "mem";
            };
        """ % (testram_count, child_address, child_address, size)))
        overlay.children.append(pydevicetree.Node.from_dts("""
        &%s {
            testram%d: testram@%x {
                compatible = "sifive,testram0";
                reg = <0x%x 0x%x>;
                reg-names = "mem";
            };
        };
        """ % (port.label, testram_count, child_address, child_address, size)))

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

def generate_overlay(argv):
    """Generate the overlay"""
    if len(argv) < 2:
        print("Please provide a devicetree file")
        sys.exit(1)

    tree = pydevicetree.Devicetree.parseFile(argv[1])

    overlay = pydevicetree.Devicetree.from_dts("""
    /dts-v1/;
    / {
        chosen {};
    };
    """)

    attach_testrams(tree, overlay)

    # Set boot hart in overlay
    chosen = overlay.get_by_path("/chosen")
    chosen.properties.append(pydevicetree.Property.from_dts("metal,boothart = <&" + \
                                                            get_boot_hart(tree).label + ">;"))

    # Set entry vector in overlay
    bootrom = get_boot_rom(tree)
    if bootrom is not None:
        chosen.properties.append(pydevicetree.Property.from_dts("metal,entry = <&" + \
                                                                bootrom.label + " 0>;"))

    return overlay.to_dts()

if __name__ == "__main__":
    print(generate_overlay(sys.argv))

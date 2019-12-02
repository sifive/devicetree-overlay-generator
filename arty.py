#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

import sys

import pydevicetree

from all_targets import get_boot_hart, get_stdout

def get_spi_flash(tree):
    """Get the SPI Flash node"""
    spi_nors = tree.match("jedec,spi-nor")
    if len(spi_nors) == 0:
        print("Unable to find the SPI flash!")
        sys.exit(1)
    return spi_nors[0]

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    # Set boot hart in overlay
    chosen = overlay.get_by_path("/chosen")
    chosen.properties.append(pydevicetree.Property.from_dts("metal,boothart = <&" + \
                                                            get_boot_hart(tree).label + ">;"))

    # Set entry vector in overlay
    bootrom = get_spi_flash(tree)
    if bootrom is not None:
        chosen.properties.append(pydevicetree.Property.from_dts("metal,entry = <&" + \
                                                                bootrom.label + " 0x400000>;"))

    stdout = get_stdout(tree)
    if stdout is not None:
        chosen.properties.append(
            pydevicetree.Property.from_dts("stdout-path = \"%s:115200\";" % stdout.get_path()))

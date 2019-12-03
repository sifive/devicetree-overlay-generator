#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

import sys

from all_targets import set_boot_hart, set_stdout, set_entry

def get_spi_flash(tree):
    """Get the SPI Flash node"""
    spi_nors = tree.match("jedec,spi-nor")
    if len(spi_nors) == 0:
        print("Unable to find the SPI flash!")
        sys.exit(1)
    return spi_nors[0]

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    bootrom = get_spi_flash(tree)
    if bootrom is not None:
        set_entry(overlay, bootrom, 0x400000)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 115200)

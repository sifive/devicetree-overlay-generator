#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

from all_targets import set_boot_hart, set_stdout, set_entry
from arty import get_spi_flash

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    bootrom = get_spi_flash(tree)

    model = tree.root().get_field("model")
    if model == "sifive,hifive1":
        offset = 0x400000
    elif model == "sifive,hifive1-revb":
        offset = 0x40000
    else:
        offset = 0x0

    if bootrom is not None:
        set_entry(overlay, bootrom, offset)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 115200)

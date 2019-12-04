#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

from targets.generic import set_boot_hart, set_stdout, set_entry, get_spi_flash

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    spi = get_spi_flash(tree)
    memory = tree.get_by_path("/memory")
    if spi is not None:
        set_entry(overlay, spi, 0x400000)
    else:
        set_entry(overlay, memory, 0x0)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 115200)

#!/usr/bin/env python3
# Copyright (c) 2020 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating VCU118 Devicetree overlays from the Devicetree
for the core on the VCU118.
"""

from targets.generic import set_boot_hart, set_stdout, set_entry, get_spi_flash
from targets.generic import get_spi_region, get_rams, set_rams, get_dtim, get_boot_hart, set_ecc_scrub

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    ddr = tree.get_by_path("/memory")
    bootram = tree.get_by_path("/soc/boot-memory")
    if ddr is not None:
        set_entry(overlay, ddr, 0, 0)
    elif bootram is not None:
        set_entry(overlay, bootram, 0, 0)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 115200)

    ram, itim = get_rams(tree)

    # Prioritize the dtim over /memory
    dtim = get_dtim(tree, get_boot_hart(tree))
    if dtim is not None:
        ram = dtim

    set_rams(overlay, ram, itim)

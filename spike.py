#!/usr/bin/env python3
# Copyright (c) 2019 SiFive Inc.
# SPDX-License-Identifier: Apache-2.0

"""
This is a python script for generating RTL testbench Devicetree overlays from the Devicetree
for the RTL DUT.
"""

from all_targets import set_boot_hart, set_stdout, set_entry

def generate_overlay(tree, overlay):
    """Generate the overlay"""
    bootrom = tree.get_by_path("/memory")
    if bootrom is not None:
        set_entry(overlay, bootrom, 0)

    set_boot_hart(tree, overlay)
    set_stdout(tree, overlay, 115200)

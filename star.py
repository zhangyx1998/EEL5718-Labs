#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#  ______ Topology
# =====================
# Author: _________
from __init__ import mn, N, H, info, create, run_tests

info(f"Creating linear topology with {N} switches, {H} hosts per switch.", False)

info("Creating hosts and switches")
hosts, switches = create()

info("Connecting switches")
# TODO: Implement your topology here

run_tests(hosts[0], hosts[-1])

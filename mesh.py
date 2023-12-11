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
for s1 in switches:
    for s2 in switches:
        if s1 == s2:
            continue
        mn.addLink(s1, s2)
        print(f"[LINK]", s1, "<->", s2)

run_tests(hosts[0], hosts[-1])

#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#   Hybrid Topology
# =====================
from __init__ import mn, N, H, info, create, run_tests

import linear
import ring
import star
import tree
import mesh

# Connect all subnets to a central switch
[hybrid_central], _ = create(1, 0, prefix="hybrid")
for subnet in (linear, mesh, ring, star, tree):
    switch = subnet.switches[0]
    mn.addLink(hybrid_central, switch)
    print(f"[LINK]", hybrid_central, "<->", switch)

if __name__ == "__main__":
    run_tests(tree.hosts[-1], star.hosts[-1])

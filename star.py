#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#  Star Topology
# =====================
prefix = None if __name__ == "__main__" else "star"
from __init__ import mn, N, H, info, create, run_tests

info(f"Creating linear topology with {N} switches, {H} hosts per switch.", False)

info("Creating hosts and switches")
[central_switch], _ = create(1, 0, prefix=prefix)
switches, hosts = create(prefix=prefix)

info("Connecting switches")
for s in switches:
    mn.addLink(central_switch, s)
    print(f"[LINK]", central_switch, "<->", s)

if __name__ == "__main__":
    run_tests(hosts[0], hosts[-1])

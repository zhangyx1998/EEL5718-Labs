#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#    Ring Topology
# =====================
prefix = None if __name__ == "__main__" else "ring"
from __init__ import mn, N, H, info, create, run_tests

info(f"Creating linear topology with {N} switches, {H} hosts per switch.", False)

info("Creating hosts and switches")
switches, hosts = create(prefix=prefix)

info("Connecting switches")
for s1, s2 in zip(switches, [*switches[1:], switches[0]]):
    mn.addLink(s1, s2)
    print(f"[LINK]", s1, "<->", s2)

if __name__ == "__main__":
    run_tests(hosts[0], hosts[-1])

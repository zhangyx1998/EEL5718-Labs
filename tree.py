#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#    Tree Topology
# =====================
prefix = None if __name__ == "__main__" else "tree"
from __init__ import mn, N, H, info, create, run_tests

info(f"Creating tree topology with {N} switches, {H} hosts per switch.", False)
total = 1
switches = []

info(f"Creating root node", False)
layer, _ = create(1, 0, prefix=prefix)

info("Creating hosts and switches")
while total < N:
    n = len(layer) * 2
    total += n
    if total < N:
        # New middle layer
        info(f"Creating middle layer with {n} nodes", False)
        next_layer, _ = create(n, 0, prefix=prefix)
    else:
        # New leaf layer
        info(f"Creating leaf layer with {n} nodes", False)
        global hosts
        next_layer, hosts = create(n, prefix=prefix)
    # Connect to previous layer
    for i, s in enumerate(next_layer):
        mn.addLink(s, layer[i // 2])
        print(f"[LINK]", s, "<->", layer[i // 2])
    switches += layer
    layer = next_layer


switches += layer

if __name__ == "__main__":
    run_tests(hosts[0], hosts[-1])

#!/usr/bin/python3
# ====================
# EEL5713 Lab2 Part3
#   Mesh Topology
# ====================
# Author: Yuxuan Zhang
import argparse
from mininet.net import Mininet
from mininet.link import Link
from mininet.node import Host, OVSSwitch, Controller
from mininet.clean import cleanup

# Argument to specify the number of hosts
parser = argparse.ArgumentParser()
parser.add_argument("--num-hosts", "-N", type=int, default=5)
parser.add_argument("--interactive", action="store_true", default=False)
args = parser.parse_args()
N = args.num_hosts


def info(msg=None, wait_key=args.interactive):
    CYAN = "\033[96m"
    RST = "\033[0m"
    if wait_key:
        msg = "Press ENTER to continue ..." if msg is None else msg
        input(CYAN + f"[INFO] {msg} ..." + RST)
    elif msg is not None:
        print(CYAN + "[INFO]", msg, end=RST + "\n")


info(f"Creating mesh topo with {N} hosts.", False)
mn = Mininet()
# List of all objects
hosts = []
switches = []
addresses = []
controller = Controller("c0", inNamespace=False)

# Loop to create hosts, each with a dedicated switch
info("Creating hosts and switches")
for i in range(N):
    host = mn.addHost(f"h{i+1}", inNamespace=False)
    hosts.append(host)
    switch = mn.addSwitch(f"s{i+1}", stp=True, inNamespace=False)
    switches.append(switch)
    mn.addLink(host, switch)
    ip = f"10.0.0.{i+1}"
    mask = "24"
    addresses.append([ip, mask])
    host.setIP("/".join([ip, mask]))
    print(f"[INIT]", f"{host}@{ip}", "->", switch)

# Loop to connect switches in a mesh
info("Connecting switches")
for i in range(0, N - 1):
    for j in range(i + 1, N):
        mn.addLink(switches[i], switches[j])
        print(f"[LINK]", switches[i], "<->", switches[j])

# Start emulation
info("Starting mininet emulation")
controller = mn.addController("controller")
mn.start()

# Ping test
info("Running pingall test")
mn.pingAll()

# Enter CLI (only in interactive mode)
if args.interactive:
    info("Entering CLI", False)
    mn.interact()

# Cleanup and exit
info("Cleaning up and exiting")
cleanup()

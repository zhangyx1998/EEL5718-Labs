#!/usr/bin/python3
# =====================
# EEL5713 Final Project
#   Project Framework
# =====================
# Author: Yuxuan Zhang
import argparse
import atexit
import signal
from statistics import mean, stdev
from mininet.net import Mininet
from mininet.clean import cleanup
from __test__ import *

from tqdm import tqdm
import networkx as nx
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Cleanup existing mininet nodes and links
cleanup()

# MiniNet initialization
mn = Mininet()
controller = mn.addController("controller")

# Argument to specify the number of hosts
parser = argparse.ArgumentParser()
parser.add_argument("--num-switches", "-N", type=int, default=4)
parser.add_argument("--hosts-per-switch", "-H", type=int, default=2)
parser.add_argument("--interactive", "-I", action="store_true", default=False)
args = parser.parse_args()
N = args.num_switches
H = args.hosts_per_switch


def info(msg=None, wait_key=args.interactive):
    CYAN = "\033[96m"
    RST = "\033[0m"
    if wait_key:
        msg = "Press ENTER to continue ..." if msg is None else msg
        input(CYAN + f"[INFO] {msg} ..." + RST)
    elif msg is not None:
        print(CYAN + "[INFO]", msg, end=RST + "\n")


addr_counter = 0
indexes = {}

hosts = []
switches = []
links = {}


def link(a, b):
    mn.addLink(a, b)
    if str(a) in links:
        links[str(a)].append(str(b))
    else:
        links[str(a)] = [str(b)]
    if str(b) in links:
        links[str(b)].append(str(a))
    else:
        links[str(b)] = [str(a)]


def new_host(prefix=None, s=None):
    global indexes, addr_counter, hosts
    prefix = "h" if prefix is None else prefix + "_h"
    index = indexes[prefix] if prefix in indexes else 1
    h = mn.addHost(f"{prefix}{index}", inNamespace=False)
    if s is not None:
        link(h, s)
        addr_counter += 1
        h.setIP(f"10.0.0.{addr_counter}/24")
        print(f"[INIT]", f"{h}@{h.IP()}", "->", s)
    indexes[prefix] = index + 1
    hosts.append(h)
    return h


def new_switch(prefix=None):
    global indexes, addr_counter, switches
    prefix = "s" if prefix is None else prefix + "_s"
    index = indexes[prefix] if prefix in indexes else 1
    s = mn.addSwitch(f"{prefix}{index}", inNamespace=False)
    switches.append(s)
    indexes[prefix] = index + 1
    return s


def create(num_switches=N, hosts_per_switch=2, prefix=None):
    # Create switches
    switches = []
    hosts = []
    for _ in range(num_switches):
        s = new_switch(prefix)
        switches.append(s)
        # Create hosts
        for _ in range(hosts_per_switch):
            h = new_host(prefix, s)
            hosts.append(h)

    return switches, hosts


def all_host_pairs():
    for i, h1 in enumerate(hosts):
        for j, h2 in enumerate(hosts):
            if i != j:
                yield h1, h2


def stat(title, results, out=None):
    """Calculate mean and standard deviation of a list of numbers"""
    results = list(map(float, results))
    m, s = mean(results), stdev(results)
    r = min(results), max(results)
    print("#", title)
    print("  mean ", m, sep=" = ")
    print("  stdev", s, sep=" = ")
    print("  min  ", r[0], sep=" = ")
    print("  max  ", r[1], sep=" = ")
    if out is not None:
        print("#", title, file=out)
        print(*results, sep=", ", file=out)
        print("# mean ", m, sep=" = ", file=out)
        print("# stdev", s, sep=" = ", file=out)
        print("# min  ", r[0], sep=" = ", file=out)
        print("# max  ", r[1], sep=" = ", file=out)
    return mean(results), stdev(results)


def graph(outfile="graph.pdf"):
    G = nx.Graph(links)
    nx.draw_networkx(G, with_labels=True, node_color="c", edge_color="k", font_size=8)
    plt.axis("off")
    plt.draw()
    plt.savefig(outfile)
    info(f"Graph saved to {outfile}", False)


def run_tests(outfile="test_results.txt"):
    info("Generating graph", False)
    graph(outfile.replace(".txt", ".pdf"))

    info("Starting mininet emulation")
    mn.start()

    info("Running pingAll test", False)
    mn.pingAll()

    # Enter CLI (only in interactive mode)
    if args.interactive:
        info("Entering CLI", False)
        mn.interact()
        return

    # Write output to file
    out = open(outfile, "w")
    pairs = list(all_host_pairs())

    # 1. ICMP (ping) latency
    info("Running ICMP tests (ping)", False)
    results = []
    for server, host in tqdm(pairs, leave=False, desc="ICMP Tests", unit="pair"):
        results.append(str(test_icmp(server, host)))
    stat("ICMP Latency", results, out)

    # 2. TCP/UDP latency and bandwidth
    info("Running TCP/UDP tests (qperf)", False)
    results = []
    for server, host in tqdm(pairs, leave=False, desc="UDP Tests", unit="pair"):
        result = test_tcp_udp(server, host)
        results.append(result)
    tcp_lat, tcp_bw, udp_lat, udp_bw = zip(*results)
    stat("TCP Latency", tcp_lat, out)
    stat("TCP Bandwidth", tcp_bw, out)
    stat("UDP Latency", udp_lat, out)
    stat("UDP Bandwidth", udp_bw, out)


def exit_handler():
    # Mask sigint
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    info("Cleaning up mininet", False)
    cleanup()


atexit.register(exit_handler)

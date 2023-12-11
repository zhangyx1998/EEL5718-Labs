#!/usr/bin/python3
# ====================
# EEL5713 Lab2 Part3
#   Mesh Topology
# ====================
# Author: Yuxuan Zhang

import argparse
import atexit
from mininet.net import Mininet
from mininet.clean import cleanup

# Cleanup existing mininet nodes and links
cleanup()

# MiniNet initialization
mn = Mininet()
controller = mn.addController("controller")

# Argument to specify the number of hosts
parser = argparse.ArgumentParser()
parser.add_argument("--num-switches", "-N", type=int, default=4)
parser.add_argument("--hosts-per-switch", "-H", type=int, default=2)
parser.add_argument("--interactive", action="store_true", default=False)
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


def new_host(prefix = None, s = None):
    global indexes, addr_counter, hosts
    prefix = "h" if prefix is None else prefix + "_h"
    index = indexes[prefix] if prefix in indexes else 1
    h = mn.addHost(f"{prefix}{index}", inNamespace=False)
    if s is not None:
        mn.addLink(h, s)
        addr_counter += 1
        h.setIP(f"10.0.0.{addr_counter}/24")
        print(f"[INIT]", f"{h}@{h.IP()}", "->", s)
    indexes[prefix] = index + 1
    hosts.append(h)
    return h


def new_switch(prefix = None):
    global indexes, addr_counter, switches
    prefix = "s" if prefix is None else prefix + "_s"
    index = indexes[prefix] if prefix in indexes else 1
    s = mn.addSwitch(f"{prefix}{index}", inNamespace=False)
    switches.append(s)
    indexes[prefix] = index + 1
    return s


def create(num_switches = N, hosts_per_switch=2, prefix = None):
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

def run_tests(server, client):
    # Start emulation
    info("Starting mininet emulation")
    mn.start()
    # Ping test
    info("Running pingAll test")
    mn.pingAll()
    # QPerf test
    info(f"Starting qperf server on {server}")
    print(server.cmd("qperf &"))
    info(f"Testing TCP latency from {client} to {server}")
    print(client.cmd("qperf", "-vvs", server.IP(), "tcp_lat"))
    info(f"Testing UDP latency from {client} to {server}")
    print(client.cmd("qperf", "-vvs", server.IP(), "udp_lat"))


def exit_handler():
    # Enter CLI (only in interactive mode)
    if args.interactive:
        info("Entering CLI", False)
        mn.interact()
    info("Cleaning up mininet", False)
    cleanup()


atexit.register(exit_handler)

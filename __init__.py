#!/usr/bin/python3
# ====================
# EEL5713 Lab2 Part3
#   Mesh Topology
# ====================
# Author: Yuxuan Zhang

import argparse
import atexit
from mininet.clean import cleanup

# Cleanup existing mininet nodes and links
cleanup()

# Argument to specify the number of hosts
parser = argparse.ArgumentParser()
parser.add_argument("--num-hosts", "-N", type=int, default=5)
parser.add_argument("--interactive", action="store_true", default=False)
args = parser.parse_args()
N = args.num_hosts
INTERACTIVE = args.interactive

def info(msg=None, wait_key=INTERACTIVE):
    CYAN = "\033[96m"
    RST = "\033[0m"
    if wait_key:
        msg = "Press ENTER to continue ..." if msg is None else msg
        input(CYAN + f"[INFO] {msg} ..." + RST)
    elif msg is not None:
        print(CYAN + "[INFO]", msg, end=RST + "\n")

atexit.register(cleanup)

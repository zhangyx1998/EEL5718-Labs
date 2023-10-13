#!/usr/bin/python3
# ====================
# EEL5713 Lab2 Part3
#   Mesh Topology
# ====================
# Author: Yuxuan Zhang
#!/usr/bin/python
import argparse
from mininet.link import Link
from mininet.node import Host, OVSSwitch, Controller
from mininet.clean import cleanup

# Argument to specify the number of hosts
parser = argparse.ArgumentParser()
parser.add_argument("--num-hosts", "-N", type=int, default=5)
parser.add_argument("--wait-key", action="store_true", default=False)
args = parser.parse_args()
N = args.num_hosts
print(f"[INFO] Creating mesh topo with {N} hosts.")


def info(msg=None):
    if args.wait_key:
        msg = "Press ENTER to continue ..." if msg is None else msg
        input(f"[INFO] {msg} ...")
    elif msg is not None:
        print("[INFO]", msg)


# List of all objects
hosts: list[Host] = []
switches: list[OVSSwitch] = []
addresses: list[str] = []
controller = Controller("c0", inNamespace=False)

# Loop to create hosts, each with a dedicated switch
info("Creating hosts and switches")
for i in range(N):
    host = Host(f"h{i+1}", inNamespace=False)
    hosts.append(host)
    switch = OVSSwitch(f"s{i+1}", stp=True, inNamespace=False)
    switches.append(switch)
    Link(host, switch)
    ip = f"10.0.0.{i+1}"
    mask = "24"
    addresses.append([ip, mask])
    host.setIP("/".join([ip, mask]))
    print(f"[INIT]", f"{host}@{ip}", "->", switch)

# Loop to connect switches in a mesh
info("Connecting switches")
for i in range(0, N - 1):
    for j in range(i + 1, N):
        Link(switches[i], switches[j])
        print(f"[LINK]", switches[i], "<->", switches[j])
# Start all switches
controller.start()
for switch in switches:
    switch.start([controller])

# Ping test
info("Running tests")
for host in hosts:
    for ip, _ in addresses:
        print(hosts[i].cmd(f"ping -c 1 {ip}"))

# Stop everything
for switch in switches:
    switch.stop()
controller.stop()
cleanup()
info("Completed, terminating")

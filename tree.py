#!/usr/bin/python3
# ====================
# EEL5713 Lab2 Part2
#   Tree Topology
# ====================
# Author: Yumeng Zhang

from mininet.topo import Topo

class MyTreeTopo(Topo):
    "Simple topology example."

    def __init__(self):
        "Create custom topo."
        # Initialize topology
        super().__init__()

        # Add hosts and switches
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6')
        h7 = self.addHost('h7')
        h8 = self.addHost('h8')
        s1 = self.addSwitch('s1')
        s2_1 = self.addSwitch('s2_1')
        s2_2 = self.addSwitch('s2_2')
        s3_1 = self.addSwitch('s3_1')
        s3_2 = self.addSwitch('s3_2')
        s4_1 = self.addSwitch('s4_1')
        s4_2 = self.addSwitch('s4_2')


        # Add links
        self.addLink(s1, s2_1)
        self.addLink(s1, s2_2)
        self.addLink(s2_1, h1)
        self.addLink(s2_1, h2)
        self.addLink(s2_2, s3_1)
        self.addLink(s2_2, s3_2)
        self.addLink(s3_1, h3)
        self.addLink(s3_1, h4)
        self.addLink(s3_2, s4_1)
        self.addLink(s3_2, s4_2)
        self.addLink(s4_1, h5)
        self.addLink(s4_1, h6)
        self.addLink(s4_2, h7)
        self.addLink(s4_2, h8)
        

topos = {'mytreetopo': (lambda: MyTreeTopo())}


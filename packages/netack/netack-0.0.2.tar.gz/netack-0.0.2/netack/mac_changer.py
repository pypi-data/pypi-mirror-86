#!/usr/bin/env python

import subprocess
import re

class MAC:
	
	def change_mac(self,interface, new_mac):
		interface = interface
		new_mac = new_mac
		print("[+] Changing MAC address for " + interface + " to " + new_mac)
		subprocess.call(["ifconfig", interface , "down"])
		subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
		subprocess.call(["ifconfig", interface, "up"])


	def get_current_mac(self, interface):
		ifconfig_result = subprocess.check_output(["ifconfig", interface])
		mac_address_search_result = re.search("\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode())

		if mac_address_search_result:
			return mac_address_search_result.group(0)
		else:
			print("[-]MAC address in sot available")

	def start(self, interface, new_mac):
		current_mac = self.get_current_mac(interface)
		print("Current MAC = " + str(current_mac))
		self.change_mac(interface, new_mac)

		current_mac = self.get_current_mac(interface)
		if current_mac == new_mac:
		    print("[+] MAC address was successfully changed to " + current_mac)
		else:
		    print("[-] MAC address did not changed.")
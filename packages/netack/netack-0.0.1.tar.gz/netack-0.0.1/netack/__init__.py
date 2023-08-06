import arp_spoof
import DNS_spoof
import mac_changer
import network_scanner
import code_injector
import Sniffer
import fake_download


class NetAck:

    def arpspoof(self, target_ip, gateway_ip):
        arp = arp_spoof.ArpSpoof()
        arp.start(target_ip, gateway_ip)

    def dnsspoof(self, target_site, redirect_to):
        dns = DNS_spoof.DNSSpoof(target_site, redirect_to)
        dns.start()

    def macchanger(self, interface, newmac):
        mac = mac_changer.MAC()
        mac.start(interface, newmac)

    def scan(self,ip):#ip is a specific ip or a range of ip
        sc = network_scanner.NetworkScanner()
        sc.scan(ip)

    def codeinjector(self, code):
        ci = code_injector.Code_Injector(code)
        ci.start()

    def sniffer(self, interface):
        sn = Sniffer.Sniffer(interface)

    def fileinterceptor(self, file):
        fi = fake_download.FakeDownload(str(file))
        fi.start()

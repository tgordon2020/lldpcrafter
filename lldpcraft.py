import socket
import sys
from scapy.layers.l2 import Ether
from scapy.contrib.lldp import *
from scapy.all import sendp
from time import sleep

#### Update interface name with valid name ####
#### Windows use ipconfig /all
#### Linux use ifconfig  ###
interface_name = "Intel(R) Wi-Fi 6 AX201 160MHz"


src_ip = socket.inet_aton(input("LLDP management IPv4 Address: "))
input_name = input("System Name: ")
input_desc = input("System Description: ")

print("""Choose a capability to advertise:
      1) Access Point
      2) Telephone
      3) Switch/Bridge """)

input_capabilities = int(input("Enter 1 2 or 3: "))

if input_capabilities == 1:
    capabilities = LLDPDUSystemCapabilities(wlan_access_point_enabled=1,wlan_access_point_available=1)
elif input_capabilities == 2:
    capabilities = LLDPDUSystemCapabilities(telephone_enabled=1,telephone_available=1,mac_bridge_enabled=1,mac_bridge_available=1)
elif input_capabilities == 3:
    capabilities = LLDPDUSystemCapabilities(mac_bridge_enabled=1,mac_bridge_available=1)
else:
    print("You didn't choose a capability, exiting")
    sys.exit()


src_mac = 'aa:bb:cc:dd:ee:ff'
dst_mas = '01:80:c2:00:00:0e'
padding = '\x00'

eth = Ether(src=src_mac, dst=dst_mas)
chassis_id = LLDPDUChassisID(subtype=0x04, id=src_mac)
port_id = LLDPDUPortID(subtype=0x05, id='1')
ttl = LLDPDUTimeToLive(ttl=5)
sys_description = LLDPDUSystemDescription(description=input_desc)
sys_name = LLDPDUSystemName(system_name=input_name)
mgmt_address = LLDPDUManagementAddress(management_address_subtype=0x01, management_address=src_ip)


frame = eth / chassis_id / port_id / ttl / capabilities / sys_description / sys_name / mgmt_address / padding / padding



while True:
    sendp(frame, iface=interface_name)
    print("sleeping for 30 seconds")
    sleep(30)

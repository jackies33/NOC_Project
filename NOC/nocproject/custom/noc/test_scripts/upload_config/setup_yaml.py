
import ipaddress
import yaml

network = input("Input network in this format please 0.0.0.0/0 : ")
ip_net = ipaddress.ip_network(network)


ipv4_addresses = [str(ip) for ip in ip_net if ip.version == 4][1:]


with open("devices.yaml", "w") as file:
    yaml.dump(ipv4_addresses, file)
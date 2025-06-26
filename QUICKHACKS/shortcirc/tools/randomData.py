import json
import random
import os
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
def random_IP():
    ip = []
    for _ in range(0, 4):
        ip.append(str(random.randint(1, 255)))
    return ".".join(ip)
def random_referer():
    referers_path = os.path.join(SCRIPT_ROOT, '../../L7/referers.txt')
    with open(referers_path, "r") as referers:
        referers = referers.readlines()
    return random.choice(referers)
def random_useragent():
    agents_path = os.path.join(SCRIPT_ROOT, '../../L7/user_agents.json')
    with open(agents_path, "r") as agents:
        user_agents = json.load(agents)["agents"]
    return random.choice(user_agents)
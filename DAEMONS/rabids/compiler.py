import os
import subprocess
import tempfile
import shutil
import sys
import time
import re
from pathlib import Path


ASCII_ART = r'''
   _______________                        |*\_/*|________
  |  ___________  |     .-.     .-.      ||_/-\_|______  |
  | |           | |    .****. .****.     | |           | |
  | |   0   0   | |    .*****.*****.     | |   0   0   | |
  | |     -     | |     .*********.      | |     -     | |
  | |   \___/   | |      .*******.       | |   \___/   | |
  | |___     ___| |       .*****.        | |___________| |
  |_____|\_/|_____|        .***.         |_______________|
    _|__|/ \|_|_.............*.............._|________|_
   / ********** \                          / ********** \
 /  ************  \                      /  ************  \
--------------------                    --------------------
'''


def print_ascii_art_red():
    RED = '\033[31m'
    RESET = '\033[0m'
    print(f"{RED}{ASCII_ART}{RESET}")


def parse_ily_source(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    go_imports = []
    rust_imports = []
    go_main_code = []
    rust_compile_code = []
    rust_attrs = []

    current_block = None
    brace_count = 0

    for line in lines:
        stripped = line.strip()
        if current_block is None:
            if stripped.startswith("import #g"):
                go_imports.append(stripped.replace("import #g", "").strip())
            elif stripped.startswith("import #r"):
                rust_imports.append(stripped.replace("import #r", "").strip())
            elif stripped.startswith("#!["):
                rust_attrs.append(stripped)
            elif stripped.startswith("func main()"):
                current_block = "go"
                brace_count = 0
            elif stripped.startswith("func compile"):
                current_block = "rust"
                brace_count = 0
        else:
            brace_count += line.count("{")
            brace_count -= line.count("}")
            if brace_count < 0:
                current_block = None
            else:
                if current_block == "go":
                    go_main_code.append(line)
                elif current_block == "rust":
                    match = re.match(r"\s*func compile(\(.*\))(.*)", line)
                    if match:
                        rust_fn = "fn compile" + match.group(1) + match.group(2)
                        rust_compile_code.append(rust_fn)
                    else:
                        rust_compile_code.append(line)

    return go_imports, rust_imports, rust_attrs, go_main_code, rust_compile_code


def print_progress(message_list, duration=4):
    RED = '\033[31m'
    RESET = '\033[0m'
    BAR_CHAR = '█'
    BAR_LENGTH = 30
    steps = BAR_LENGTH + 1
    msg_count = len(message_list)
    for i in range(steps):
        percent = int((i / BAR_LENGTH) * 100)
        bar = f"{RED}{BAR_CHAR * i}{RESET}{' ' * (BAR_LENGTH - i)}"
        msg = message_list[min(i * msg_count // steps, msg_count - 1)]
        print(f"\r{msg} [{bar}] {percent}%", end='', flush=True)
        time.sleep(duration / BAR_LENGTH)
    print(' ' * 80, end='\r') 
    print() 


def write_and_compile_go(go_imports, go_code):
    imports_block = "import (\n" + "".join([f'\t"{imp}"\n' for imp in go_imports]) + ")\n"
    go_program = "package main\n\n" + imports_block + "\nfunc main() {\n" + "".join(go_code) + "\n}\n"

    temp_dir = tempfile.mkdtemp(prefix="ily_go_")
    go_src = Path(temp_dir) / "main.go"
    go_src.write_text(go_program)

    go_exe = Path(temp_dir) / "go_payload.exe"

    env = os.environ.copy()
    env["GOOS"] = "windows"
    env["GOARCH"] = "amd64"

    try:
        subprocess.run(["go", "build", "-o", str(go_exe), str(go_src)], check=True, env=env)
    except subprocess.CalledProcessError as e:
        print("[Error] Go compilation failed:", e)
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    return go_exe.read_bytes()


def write_and_compile_rust(rust_imports, rust_attrs, rust_code, go_pe_bytes, output_exe_name):
    target = "x86_64-pc-windows-gnu"
    is_mac = sys.platform == "darwin"

    linker = shutil.which("x86_64-w64-mingw32-gcc")
    if is_mac and linker is None:
        print("[Error] Missing required linker: x86_64-w64-mingw32-gcc")
        print("Install it via Homebrew: brew install mingw-w64")
        return

    use_lines = [f"use {imp};" for imp in rust_imports]
    use_lines.append("use goldberg::goldberg_stmts;")
    imports_str = "\n".join(use_lines)
    attrs_str = "\n".join(rust_attrs)

    go_pe_array = ", ".join(str(b) for b in go_pe_bytes)
    go_pe_declaration = f"const GO_PAYLOAD: &[u8] = &[{go_pe_array}];"

    rust_code_str = ''.join(rust_code)

    memexec_code = f"""
{attrs_str}
{imports_str}
{go_pe_declaration}

fn main() {{
    unsafe {{
        memexec::memexec_exe(GO_PAYLOAD).expect(\"Failed to execute PE from memory\");
    }}
    goldberg_stmts! {{
        {{
            {rust_code_str}
        }}
    }}
}}
"""

    temp_dir = tempfile.mkdtemp(prefix="ily_rust_")
    src_dir = Path(temp_dir) / "src"
    src_dir.mkdir(parents=True, exist_ok=True)
    main_rs = src_dir / "main.rs"
    main_rs.write_text(memexec_code)

    cargo_toml = Path(temp_dir) / "Cargo.toml"
    cargo_toml.write_text(f"""
[package]
name = "ily_combined"
version = "0.1.0"
edition = "2018"

[dependencies]
memexec = {{ git = \"https://github.com/DmitrijVC/memexec\", version = \"0.3\" }}
goldberg = \"0.1\"
""")

    import_crates = set()
    for imp in rust_imports:
        crate = imp.split('::')[0]
        if crate not in ("std", "core"):
            import_crates.add(crate)
    if import_crates:
        import subprocess
        for crate in import_crates:
            try:
                subprocess.run(["cargo", "add", crate], cwd=temp_dir, check=True)
            except Exception as e:
                print(f"[Warning] Could not add crate {crate}: {e}")

    cargo_config_dir = Path(temp_dir) / ".cargo"
    cargo_config_dir.mkdir(exist_ok=True)
    config_toml = cargo_config_dir / "config.toml"
    config_toml.write_text(f"""
[target.{target}]
linker = "{linker}"
""")

    exe_path = Path.cwd() / output_exe_name
    try:
        subprocess.run(
            ["cargo", "build", "--release", "--target", target],
            cwd=temp_dir,
            check=True
        )
        built_exe = Path(temp_dir) / "target" / target / "release" / "ily_combined.exe"
        shutil.copy(str(built_exe), exe_path)
        print(f"Executable created at: {exe_path}")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Rust compilation failed: {e}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


def compile_ily(file_path, output_exe_name):
    print_ascii_art_red()
    print(f"Compiling {file_path}...")

    go_imports, rust_imports, rust_attrs, go_main, rust_compile = parse_ily_source(file_path)

    go_binary_data = b""
    if go_main:
        progress_messages = [
            "Starting Go compilation...",
            "Cross-compiling Go code to Windows binary...",
            "Go compilation complete. Starting Rust compilation...",
            "Compiling Rust to Windows target...",
            "Finalizing executable..."
        ]
        print_progress(progress_messages, duration=6)
        go_binary_data = write_and_compile_go(go_imports, go_main)
    else:
        go_binary_data = b""

    if rust_compile:
        write_and_compile_rust(rust_imports, rust_attrs, rust_compile, go_binary_data, output_exe_name)


def print_usage():
    print("Usage: python ily_compiler.py <filename.ily> [output_exe_name.exe]")

if __name__ == "__main__":
    if len(sys.argv) < 2 or not sys.argv[1].endswith(".ily"):
        print_usage()
    else:
        output_exe_name = sys.argv[2] if len(sys.argv) > 2 else "ily_combined.exe"
        try:
            compile_ily(sys.argv[1], output_exe_name)
        except subprocess.CalledProcessError as e:
            print(f"[Error] Compilation or execution failed: {e}")


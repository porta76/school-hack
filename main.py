import sys
import os
import subprocess
import readline
from tabulate import tabulate
from loading import show_loading_screen, clear_screen

# --- ASCII Art ---
RED = "\033[38;2;204;103;102m"
YELLOW = "\033[93m"
BLUE = "\033[34m"
GREEN = "\033[38;2;180;189;104m"
PINK = "\033[38;2;227;148;220m"
CYAN = "\033[36m"
WHITE = "\033[1;37m"
RESET = "\033[0m"

# Interface colors (only pink, red, white)
INTERFACE_RED = "\033[38;2;204;103;102m"
INTERFACE_PINK = "\033[38;2;227;148;220m"
INTERFACE_WHITE = "\033[38;2;208;208;208m"
INTERFACE_GREEN = "\033[38;2;180;189;104m"
INTERFACE_YELLOW = "\033[93m"

ASCII_ARTS = {
    'daemon': f'''{RED}
                        *
                     *
          (\___/)     (
          \ (- -)     )\ *
          c\   >'    ( #
            )-_/      '
     _______| |__    ,|//
    # ___ `  ~   )  ( /
    \,|  | . ' .) \ /#
   _( /  )   , / \ / |
     //  ;;,,;,;   \,/
      _,#;,;;,;,;
    /,i;;;,,;#,;
   ((  %;;,;,;;,;
    ))  ;#;,;%;;,,
  _//    ;,;; ,#;,
 /_)     #,;  //
        //    \|_

{RED}PWNING SYSTEMS WITH PWN0S{RESET}
{INTERFACE_WHITE}meatspace? it moves so slow. me, i like the net. it moves fast{RESET}{PINK} <3{RESET}''',
    'quickhack': f'''{YELLOW}
                                 |     |
                                 \\_V_//
                                 \/=|=\/
                                  [=v=]
                                __\___/_____
                               /..[  _____  ]
                              /_  [ [  M /] ]
                             /../.[ [ M /@] ]
                            <-->[_[ [M /@/] ]
                           /../ [.[ [ /@/ ] ]
      _________________]\ /__/  [_[ [/@/ C] ]
     <_________________>>0---]  [=\ \@/ C / /
        ___      ___   ]/000o   /__\ \ C / /
           \    /              /....\ \_/ /
        ....\||/....           [___/=\___/
       .    .  .    .          [...] [...]
      .      ..      .         [___/ \___]
      .    0 .. 0    .         <---> <--->
   /\/\.    .  .    ./\/\      [..]   [..]
  / / / .../|  |\... \ \ \    _[__]   [__]_
 / / /       \/       \ \ \  [____>   <____]

{YELLOW}PWNING SYSTEMS WITH PWN0S{RESET}

{INTERFACE_WHITE}meatspace? it moves so slow. me, i like the net. it moves fast{RESET}{PINK} <3{RESET}''',
    'interfaceplug': f'''{BLUE}
 ____________________________________________________
T ================================================= |T
| ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|[L
| __________________________________________________[|
|I __==___________  ___________     .  ,. _ .   __  T|
||[_j  L_I_I_I_I_j  L_I_I_I_I_j    /|/V||(g/|   ==  l|
lI _______________________________  _____  _________I]
 |[__I_I_I_I_I_I_I_I_I_I_I_I_I_I_] [__I__] [_I_I_I_]|
 |[___I_I_I_I_I_I_I_I_I_I_I_I_L  I   ___   [_I_I_I_]|
 |[__I_I_I_I_I_I_I_I_I_I_I_I_I_L_I __I_]_  [_I_I_T ||
 |[___I_I_I_I_I_I_I_I_I_I_I_I____] [_I_I_] [___I_I_j|
 | [__I__I_________________I__L_]                   |
 |                                                  |  
 l__________________________________________________j

{BLUE}PWNING SYSTEMS WITH PWN0S{RESET}
{INTERFACE_WHITE}meatspace? it moves so slow. me, i like the net. it moves fast{RESET}{PINK} <3{RESET}''',
    'default': None, 
}

# Load default ASCII art from ascii.txt
ASCII_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ascii.txt')
if os.path.exists(ASCII_PATH):
    with open(ASCII_PATH, 'r', encoding='utf-8') as f:
        ASCII_ARTS['default'] = f.read()
else:
    ASCII_ARTS['default'] = 'PWN0S'

# --- Module logic wrappers ---
def run_filedaemon(opts):
    action = opts.get('ACTION')
    if action == 'start':
        subprocess.run([sys.executable, os.path.join('DAEMONS', 'filedaemon', 'filedaemon.py'), '-start'])
    elif action == 'clean':
        subprocess.run([sys.executable, os.path.join('DAEMONS', 'filedaemon', 'filedaemon.py'), '-clean'])
    else:
        print("[!] Set ACTION to 'start' or 'clean' before running.")

def run_rabid_spider(opts):
    lhost = opts.get('LHOST')
    lport = opts.get('LPORT')
    key = opts.get('KEY')
    if not (lhost and lport and key):
        print("[!] Set LHOST, LPORT, and KEY before running.")
        return
    subprocess.run([
        sys.executable, os.path.join('DAEMONS', 'rabids', 'rabids.py'),
        '-rabids', '-spider', '-lhost', str(lhost), '-lport', str(lport), '-key', str(key)
    ])

def run_brainwipe(opts):
    url = opts.get('URL')
    template = opts.get('TEMPLATE')
    foldername = opts.get('FOLDERNAME')
    filename = opts.get('FILENAME')
    filesize = opts.get('FILESIZE')
    payload_file = opts.get('PAYLOAD_FILE')
    payload_name = opts.get('PAYLOAD_NAME')

    args = [sys.executable, os.path.join('DAEMONS', 'brainwipe', 'brainwipe.py')]
    # Only pass URL if TEMPLATE is not set
    if template:
        args += ['--template', template]
    else:
        if not url:
            print("[!] Set URL before running.")
            return
        args.append(url)
    if foldername:
        args += ['--foldername', foldername]
    if filename:
        args += ['--filename', filename]
    if filesize:
        args += ['--filesize', filesize]
    if payload_file:
        args += ['--payload-file', payload_file]
    if payload_name:
        args += ['--payload-name', payload_name]
    subprocess.run(args)

def run_blackout(opts):
    server_ip = opts.get('SERVER_IP')
    device = opts.get('DEVICE')
    command = opts.get('COMMAND')
    print(f"[+] Would connect to server {server_ip}, device {device}, send command {command}")

def run_deck(opts):
    username = opts.get('USERNAME')
    ip = opts.get('IP')
    password = opts.get('PASSWORD')
    if not (username and ip and password):
        print("[!] Set USERNAME, IP, and PASSWORD before running.")
        return
    subprocess.run([sys.executable, os.path.join('INTERFACEPLUGS', 'deck', 'deck.py'), '-username', username, '-ip', ip, '-password', password])

def run_ping(opts):
    mode = opts.get('MODE')
    value = opts.get('VALUE')
    if mode == 'ip':
        subprocess.run([sys.executable, os.path.join('QUICKHACKS', 'ping', 'ping.py'), '-ip', value])
    elif mode == 'sip':
        subprocess.run([sys.executable, os.path.join('QUICKHACKS', 'ping', 'ping.py'), '-sip'])
    elif mode == 'pn':
        subprocess.run([sys.executable, os.path.join('QUICKHACKS', 'ping', 'ping.py'), '-pn', value])
    elif mode == 'ut':
        subprocess.run([sys.executable, os.path.join('QUICKHACKS', 'ping', 'ping.py'), '-ut', value])
    else:
        print("[!] Set MODE to one of: ip, sip, pn, ut and VALUE as needed.")

def run_shortcirc(opts):
    target = opts.get('TARGET')
    method = opts.get('METHOD')
    time_ = opts.get('TIME')
    threads = opts.get('THREADS')
    if not (target and method and time_ and threads):
        print("[!] Set TARGET, METHOD, TIME, and THREADS before running.")
        return
    subprocess.run([
        sys.executable, os.path.join('QUICKHACKS', 'shortcirc', 'shortcirc.py'),
        '-target', target, '-method', method, '-time', str(time_), '-threads', str(threads)
    ])

def run_icepick(opts):
    t = opts.get('TARGET')
    p = opts.get('PAYLOAD')
    if not (t and p):
        print("[!] Set T and P before running.")
        return
    subprocess.run([
        sys.executable, os.path.join('QUICKHACKS', 'icepick', 'icepick.py'),
        '-t', t, '-p', p
    ])

# --- Module class and registry ---
class Module:
    def __init__(self, name, options, run_func, option_desc=None, description=None):
        self.name = name
        self.options = options.copy()
        self.option_desc = option_desc or {k: '' for k in options}
        self.values = {k: v for k, v in options.items()}
        self.run_func = run_func
        self.description = description or ''
    def set_option(self, key, value):
        if key in self.options:
            self.values[key] = value
            return True
        return False
    def show_options(self):
        table = []
        for k in self.options:
            table.append([f"{INTERFACE_PINK}{k}{RESET}", f"{INTERFACE_RED}{self.values.get(k, '')}{RESET}", f"{INTERFACE_WHITE}{self.option_desc.get(k, '')}{RESET}"])
        print(tabulate(table, headers=[f"{INTERFACE_WHITE}Option{RESET}", f"{INTERFACE_WHITE}Value{RESET}", f"{INTERFACE_WHITE}Description{RESET}"], tablefmt="github"))
    def run(self):
        return self.run_func(self.values)

MODULES = {
    'daemon/filedaemon': Module(
        'daemon/filedaemon',
        options={'ACTION': ''},
        option_desc={'ACTION': "'start' to run server, 'clean' to wipe dir"},
        run_func=run_filedaemon,
        description='Simple HTTP file server and cleaner.'
    ),
    'daemon/rabid/spider': Module(
        'daemon/rabid/spider',
        options={'LHOST': '', 'LPORT': '', 'KEY': ''},
        option_desc={'LHOST': 'Local host for reverse shell', 'LPORT': 'Local port', 'KEY': 'XOR key (0-255)'},
        run_func=run_rabid_spider,
        description='Rabid Spider payload builder (reverse shell generator).'
    ),
    'daemon/rabid/bartmoss': Module(
        'daemon/rabid/bartmoss',
        options={'NOTE': ''},
        option_desc={'NOTE': 'The ransom note text to write to the desktop'},
        run_func=lambda opts: subprocess.run([
            sys.executable, os.path.join('DAEMONS', 'rabids', 'rabids.py'),
            '-rabids', '-bartmoss', '-note', str(opts.get('NOTE', ''))
        ]),
        description='Bartmoss ransomware payload builder (sets ransom note).'
    ),
    'daemon/brainwipe': Module(
        'daemon/brainwipe',
        options={
            'URL': '',
            'TEMPLATE': '',
            'FOLDERNAME': '',
            'FILENAME': '',
            'FILESIZE': '',
            'PAYLOAD_FILE': '',
            'PAYLOAD_NAME': ''
        },
        option_desc={
            'URL': 'Target URL to clone',
            'TEMPLATE': 'Template name (optional)',
            'FOLDERNAME': 'Folder name for drive template',
            'FILENAME': 'File name for drive template',
            'FILESIZE': 'File size for drive template',
            'PAYLOAD_FILE': 'Path to a file to use as the payload (will be base64-encoded automatically)',
            'PAYLOAD_NAME': 'Payload file name for drive template (overrides FILENAME for payload only)'
        },
        run_func=run_brainwipe,
        description='Website cloner and phishing credential harvester.'
    ),
    'interfaceplug/blackout': Module(
        'interfaceplug/blackout',
        options={'SERVER_IP': '', 'DEVICE': '', 'COMMAND': ''},
        option_desc={'SERVER_IP': 'Server IP for ESP32', 'DEVICE': 'Serial device', 'COMMAND': 'Command to send'},
        run_func=run_blackout,
        description='ESP32 blackout controller (IoT interface).'
    ),
    'interfaceplug/deck': Module(
        'interfaceplug/deck',
        options={'USERNAME': '', 'IP': '', 'PASSWORD': ''},
        option_desc={'USERNAME': 'SSH username', 'IP': 'Target IP', 'PASSWORD': 'SSH password'},
        run_func=run_deck,
        description='SSH connection manager.'
    ),
    'quickhack/ping': Module(
        'quickhack/ping',
        options={'MODE': '', 'VALUE': ''},
        option_desc={'MODE': 'ip/sip/pn/ut', 'VALUE': 'Value for the selected mode'},
        run_func=run_ping,
        description='IP, phone, and username tracker.'
    ),
    'quickhack/shortcirc': Module(
        'quickhack/shortcirc',
        options={'TARGET': '', 'METHOD': '', 'TIME': '', 'THREADS': ''},
        option_desc={'TARGET': 'Target ip:port, url or phone', 'METHOD': 'Attack method', 'TIME': 'Attack duration (s)', 'THREADS': 'Threads count'},
        run_func=run_shortcirc,
        description='Denial-of-service (DoS) attack toolkit.'
    ),
    'quickhack/icepick': Module(
        'quickhack/icepick',
        options={'T': '', 'P': ''},
        option_desc={'T': 'Path to first EXE', 'P': 'Path to second EXE'},
        run_func=run_icepick,
        description='EXE dropper/runner for red team ops.'
    ),
}

COMMANDS = ['use', 'set', 'show', 'run', 'back', 'exit']

# --- Tab completion logic ---
def get_module_names():
    return list(MODULES.keys())

def get_option_names(module):
    if module and module in MODULES:
        return list(MODULES[module].options.keys())
    return []

def metasploit_completer(text, state):
    buffer = readline.get_line_buffer()
    line = buffer.split()
    if not line:
        opts = COMMANDS + get_module_names()
    elif line[0] == 'use':
        opts = [m for m in get_module_names() if m.startswith(text)]
    elif line[0] == 'set':
        current_module = getattr(metasploit_completer, 'current_module', None)
        opts = get_option_names(current_module)
        opts = [o for o in opts if o.startswith(text)]
    elif line[0] == 'show':
        opts = ['modules', 'options']
        opts = [o for o in opts if o.startswith(text)]
    else:
        opts = [c for c in COMMANDS if c.startswith(text)]
    if state < len(opts):
        return opts[state] + ' '
    return None

def get_ascii_art_for_context(current_module):
    if current_module:
        if current_module.startswith('daemon/'):
            return ASCII_ARTS['daemon']
        elif current_module.startswith('quickhack/'):
            return ASCII_ARTS['quickhack']
        elif current_module.startswith('interfaceplug/'):
            return ASCII_ARTS['interfaceplug']
    return ASCII_ARTS['default']

def metasploit_shell():
    current_module = None
    readline.set_completer(metasploit_completer)
    readline.parse_and_bind('tab: complete')
    metasploit_completer.current_module = None
    last_art_context = None
    def print_art_for_context(context):
        art = get_ascii_art_for_context(context)
        if art:
            print(art)
        print('\033[0m', end='')  # Reset color after art
        print()  # Add one blank line after art
    clear_screen()
    print_art_for_context(current_module)
    last_art_context = current_module
    while True:
        try:
            prompt = f"{INTERFACE_PINK}{current_module if current_module else '*'}{RESET} {INTERFACE_PINK}>{RESET} "
            cmdline = input(prompt)
            parts = cmdline.strip().split()
            if not parts:
                continue
            cmd = parts[0].lower()
            if cmd == 'exit' or cmd == 'quit':
                clear_screen()
                print_art_for_context(current_module)
                break
            elif cmd == 'help':
                clear_screen()
                print_art_for_context(current_module)
                
                # Show available commands
                print(f"{INTERFACE_WHITE}Available Commands:{RESET}")
                print()
                command_descriptions = {
                    'use': 'Select a module to use',
                    'set': 'Set a module option',
                    'show': 'Show modules or options',
                    'run': 'Execute the current module',
                    'back': 'Go back to main menu',
                    'exit': 'Exit PWN0S',
                    'help': 'Show this help message'
                }
                cmd_table = [[f"{INTERFACE_PINK}{cmd}{RESET}", f"{INTERFACE_WHITE}{desc}{RESET}"] for cmd, desc in command_descriptions.items()]
                print(tabulate(cmd_table, headers=[f"{INTERFACE_WHITE}Command{RESET}", f"{INTERFACE_WHITE}Description{RESET}"], tablefmt="github"))
                print()
                continue
            elif cmd == 'show':
                if len(parts) > 1 and parts[1] == 'modules':
                    table = []
                    for m, mod in MODULES.items():
                        table.append([f"{INTERFACE_PINK}{m}{RESET}", f"{INTERFACE_WHITE}{mod.description}{RESET}"])
                    print()
                    print(tabulate(table, headers=[f"{INTERFACE_WHITE}Module{RESET}", f"{INTERFACE_WHITE}Description{RESET}"], tablefmt="github"))
                    print()
                elif len(parts) > 1 and parts[1] == 'options':
                    if current_module:
                        print()
                        MODULES[current_module].show_options()
                        print()
                    else:
                        print()
                        print(f"{INTERFACE_RED}[!] No module selected.{RESET}")
                        print()
                else:
                    print()
                    print(f"{INTERFACE_RED}[!] Unknown show command.{RESET}")
                    print()
            elif cmd == 'use':
                if len(parts) < 2:
                    print()
                    print(f"{INTERFACE_YELLOW}Usage: use <module>{RESET}")
                    print()
                    continue
                modname = parts[1]
                if modname not in MODULES:
                    print()
                    print(f"{INTERFACE_RED}[!] Unknown module: {modname}{RESET}")
                    print()
                    continue
                current_module = modname
                metasploit_completer.current_module = current_module
                clear_screen()
                print_art_for_context(current_module)
                print(f"{INTERFACE_WHITE}[+] Using module: {current_module}{RESET}")
                print()
                last_art_context = current_module
            elif cmd == 'set':
                if not current_module:
                    print()
                    print(f"{INTERFACE_RED}[!] No module selected.{RESET}")
                    print()
                    continue
                if len(parts) < 3:
                    print()
                    print(f"{INTERFACE_YELLOW}Usage: set <OPTION> <VALUE>{RESET}")
                    print()
                    continue
                opt = parts[1].upper()
                val = ' '.join(parts[2:])
                if MODULES[current_module].set_option(opt, val):
                    print(f"{INTERFACE_GREEN}[+] Set {opt} => {val}{RESET}")
                    print()
                else:
                    print()
                    print(f"{INTERFACE_RED}[!] Unknown option: {opt}{RESET}")
                    print()
            elif cmd == 'run':
                if not current_module:
                    print()
                    print(f"{INTERFACE_RED}[!] No module selected.{RESET}")
                    print()
                    continue
                show_loading_screen(loading_message=f"Running {current_module}...", duration=2, print_ascii_art=lambda: print(get_ascii_art_for_context(current_module)))
                clear_screen()
                print_art_for_context(current_module)
                MODULES[current_module].run()
                print()
            elif cmd == 'back':
                current_module = None
                metasploit_completer.current_module = None
                clear_screen()
                print_art_for_context(current_module)
                last_art_context = current_module
            else:
                print()
                print(f"{INTERFACE_RED}[!] Unknown command: {cmd}{RESET}")
                print()
        except (KeyboardInterrupt, EOFError):
            print()
            continue

if __name__ == "__main__":
    try:
        from tabulate import tabulate
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tabulate'])
        from tabulate import tabulate
    metasploit_shell() 
## What's New

### v0.1.4

- **Bartmoss Ransomware Payload Builder**: Added a new module for generating a customizable ransomware payload. The Bartmoss module allows you to specify a ransom note that will be written to the victim's desktop. The payload is built as a Windows executable with AV evasion and persistence features.
  - Set the ransom note text to be displayed on the victim's desktop.
  - The built executable will be saved in the `DAEMONS/rabids/bin/` directory as `bartmoss.exe`.
  - **IMP** Need Rust to be installed
```
use daemon/rabid/bartmoss
set NOTE "Your ransom note here"
run
```

### v0.1.3

- **Google Drive Phishing Template**: The Brainwipe module now includes a highly customizable Google Drive phishing template. You can set:
  - **FOLDERNAME**: The folder name displayed in the fake drive
  - **FILENAME**: The file name shown for download
  - **FILESIZE**: The displayed file size
  - **PAYLOAD_FILE**: Path to the file to serve as the payload (auto base64-encoded)
  - **PAYLOAD_NAME**: The name of the payload file for download (overrides FILENAME for the payload only)
```
pwn0s > use daemon/brainwipe
pwn0s > set TEMPLATE drive
```

### v0.1.2

- **New Metasploit-style Interface**: PWN0S now uses a module-based command structure similar to Metasploit Framework. Use `use <module>`, `set <option> <value>`, and `run` commands for all operations.

- **Rabids payload builder** is now Go-based for Windows payloads: generates, encrypts, and compiles a silent EXE with persistence and AV evasion. Access via: `use daemon/rabid/spider` then set `LHOST`, `LPORT`, and `KEY` options.

- **Icepick EXE binder** for red team/offsec use: `use quickhack/icepick` then set `T` (target EXE path) and `P` (payload EXE path) options.

## Overview

PWN0S consolidates multiple cybersecurity capabilities into a single, streamlined interface, empowering security professionals with a robust platform for penetration testing and offensive security operations. Its key features include:

- **Quickhacks**: A suite of network reconnaissance and attack tools for rapid deployment during engagements, enabling swift intelligence gathering and exploitation.

- **Daemons**: Background services that automate payload generation, file serving, and persistent operations, reducing manual overhead in complex workflows.

- **Interface Plugs**: Hardware management utilities for interfacing with microcontrollers and other devices, enabling seamless integration with physical attack vectors.

## How to Install

1. **Clone the repository** (if you haven't already):

   ```bash
   git clone https://github.com/sarwaaaar/PWN0S.git
   cd PWN0S
   ```

2. **Install Python 3.8+**

   - Make sure you have Python 3.8 or newer installed. You can check your version with:
     ```bash
     python3 --version
     ```
   - If you need to install Python:
     - **macOS:**
       ```bash
       brew install python3
       ```
     - **Linux (Debian/Ubuntu):**
       ```bash
       sudo apt update && sudo apt install python3 python3-pip
       ```
     - **Windows:**
       Download from [python.org](https://www.python.org/downloads/)

3. **Install dependencies**

   - Install all required Python packages:
     ```bash
     python3 -m pip install --upgrade pip
     python3 -m pip install -r requirements.txt
     ```

4. **(Optional) Install system dependencies**

   - Some features require additional tools:
     - `php`, `go`, `cargo`, `msfvenom`, `wget`, `httrack`, `monolith`
   - On macOS (using Homebrew):
     ```bash
     brew install php go msfvenom wget httrack
     cargo install monolith
     ```
   - On Linux (Debian/Ubuntu):
     ```bash
     sudo apt install php go cargo metasploit-framework wget httrack
     cargo install monolith
     ```
   - For `msfvenom`, see [Metasploit installation guide](https://docs.metasploit.com/docs/using-metasploit/getting-started/nightly-installers.html)

5. **Run PWN0S**
   ```bash
   python3 main.py
   ```

You're ready to use PWN0S! For command usage, see the Command Reference below.

## Command Reference

PWN0S provides a comprehensive module-based interface designed for efficiency and ease of use. The interface uses a Metasploit-style command structure with modules organized into three main categories: **Daemons**, **Quickhacks**, and **Interface Plugs**.

### Quick Start

**Basic Commands:**
- `use <module>` - Select a module
- `set <OPTION> <VALUE>` - Configure options
- `show modules` - List available modules
- `show options` - View module options
- `run` - Execute module
- `help` - Show commands
- `exit` - Exit PWN0S

**Example Workflow:**
```
pwn0s > use daemon/filedaemon
pwn0s > set ACTION start
pwn0s > run

# Bartmoss ransomware builder example:
pwn0s > use daemon/rabid/bartmoss
pwn0s > set NOTE "Your files have been encrypted! Contact us at evil@domain.com."
pwn0s > run
```

### Available Modules

| Category | Modules |
|----------|---------|
| **Daemons** | `daemon/filedaemon`, `daemon/rabid/spider`, `daemon/rabid/bartmoss`, `daemon/brainwipe` |
| **Interface Plugs** | `interfaceplug/blackout`, `interfaceplug/deck` |
| **Quickhacks** | `quickhack/ping`, `quickhack/shortcirc`, `quickhack/icepick` |

### Detailed Documentation

For comprehensive command reference, detailed module descriptions, usage examples, and troubleshooting guides, see the **[PWN0S Wiki](https://github.com/sarwaaaar/PWN0S/wiki)**.

The wiki includes:
- Complete command syntax and examples
- Detailed module options and configurations
- Advanced usage scenarios
- Troubleshooting and best practices
- Color scheme and interface details

PWN0S is actively under development, with several exciting features planned:

- **Advanced Malware Modules**: Support for researching and simulating cryptominers, ransomware, time bombs, and other malware types in controlled environments.
- **Expanded Hardware Capabilities**:
  - **Radio Hacking**: Integration with SDR for intercepting and manipulating wireless signals.
  - **RFID Card Reader/Writer**: Tools for cloning and modifying RFID tags.
  - **Infrared Communication**: Support for IR-based attacks on IoT and legacy devices.
  - **Keystroke Injection**: Enhanced BadUSB and Rubber Ducky integration.
- **Remote Cyber Deck Framework**: A lightweight framework running on Raspberry Pi Zero W, coordinating with Pico W and ESP32-S3 for a fully portable, remote-capable cyber deck, enabling synchronized attacks across devices.

## Legal Disclaimer

PWN0S is intended for educational purposes and authorized security testing only. Users must obtain explicit permission before using this toolkit against any systems or networks. The authors and contributors are not liable for any misuse, damage, or legal consequences resulting from the use of this tool. Always adhere to applicable laws and ethical guidelines.

## Contributing

Contributions are welcome to enhance PWN0S's capabilities. To contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Implement and test your changes thoroughly.
4. Commit your changes (`git commit -m "Add your feature"`).
5. Push to your fork (`git push origin feature/your-feature`).
6. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Links

- **Seeker (Integrated Phishing Toolkit)**: https://github.com/thewhiteh4t/seeker
- **GhostTrack (OSINT Tracking Tool)**: https://github.com/HunxByts/GhostTrack
- **Impulse (DDoS Toolkit)**: https://github.com/LimerBoy/Impulse
- **Metasploit Framework**: https://github.com/rapid7/metasploit-framework
- **Kali Linux**: https://www.kali.org/
- **Rust Programming Language**: https://www.rust-lang.org/

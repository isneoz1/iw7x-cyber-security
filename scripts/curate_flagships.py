#!/usr/bin/env python3
"""Curate flagship tools in catalog.json.

For a hand-picked list of industry-standard tools we guarantee correct,
Kali-ready install/run commands. If a tool with the same title already exists
(from the scraper) we *upgrade* it in place; otherwise we add it to its
category. This makes the most-used tools "just work" after install.

Run:  python scripts/curate_flagships.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


# category_id -> list of authoritative flagship tools
FLAGSHIPS: dict[str, list[dict]] = {
    "information_gathering": [
        {"title": "Nmap", "description": "The network mapper — host discovery, port and service/version scanning, NSE scripts.",
         "install": ["sudo apt install -y nmap"], "run": ["nmap"], "url": "https://nmap.org", "tags": ["scanner", "recon"]},
        {"title": "Masscan", "description": "Internet-scale TCP port scanner, asynchronous and extremely fast.",
         "install": ["sudo apt install -y masscan"], "run": ["masscan"], "url": "https://github.com/robertdavidgraham/masscan", "tags": ["scanner"]},
        {"title": "RustScan", "description": "Ultra-fast port scanner that feeds open ports straight into Nmap.",
         "install": ["sudo apt install -y rustscan || cargo install rustscan"], "run": ["rustscan"], "url": "https://github.com/RustScan/RustScan", "tags": ["scanner"]},
        {"title": "naabu", "description": "Fast SYN/CONNECT port scanner from ProjectDiscovery.",
         "install": ["go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"], "run": ["naabu -h"], "url": "https://github.com/projectdiscovery/naabu", "tags": ["scanner"]},
    ],
    "osint": [
        {"title": "theHarvester", "description": "Gather emails, subdomains, hosts and names from public sources (OSINT recon).",
         "install": ["sudo apt install -y theharvester"], "run": ["theHarvester -h"], "url": "https://github.com/laramies/theHarvester", "tags": ["osint", "recon"]},
        {"title": "Amass", "description": "In-depth attack surface mapping and asset/subdomain discovery (OWASP).",
         "install": ["sudo apt install -y amass"], "run": ["amass -h"], "url": "https://github.com/owasp-amass/amass", "tags": ["recon", "osint"]},
        {"title": "subfinder", "description": "Fast passive subdomain discovery from ProjectDiscovery.",
         "install": ["go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"], "run": ["subfinder -h"], "url": "https://github.com/projectdiscovery/subfinder", "tags": ["recon"]},
        {"title": "SpiderFoot", "description": "Automated OSINT collection and attack-surface reconnaissance.",
         "install": ["pipx install spiderfoot"], "run": ["spiderfoot -h"], "url": "https://github.com/smicallef/spiderfoot", "tags": ["osint"]},
        {"title": "Sherlock", "description": "Hunt down social-media accounts by username across 400+ sites.",
         "install": ["pipx install sherlock-project"], "run": ["sherlock --help"], "url": "https://github.com/sherlock-project/sherlock", "tags": ["osint"]},
        {"title": "holehe", "description": "Check if an email is used on 120+ sites via account-recovery leaks.",
         "install": ["pipx install holehe"], "run": ["holehe --help"], "url": "https://github.com/megadose/holehe", "tags": ["osint"]},
        {"title": "Maigret", "description": "Collect a dossier on a person by username from thousands of sites.",
         "install": ["pipx install maigret"], "run": ["maigret --help"], "url": "https://github.com/soxoj/maigret", "tags": ["osint"]},
        {"title": "dnsx", "description": "Fast, multi-purpose DNS toolkit for resolving and probing records.",
         "install": ["go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest"], "run": ["dnsx -h"], "url": "https://github.com/projectdiscovery/dnsx", "tags": ["recon"]},
    ],
    "web_attack": [
        {"title": "ffuf", "description": "Fast web fuzzer for content, parameter and vhost discovery.",
         "install": ["sudo apt install -y ffuf"], "run": ["ffuf -h"], "url": "https://github.com/ffuf/ffuf", "tags": ["web", "fuzzing", "bruteforce"]},
        {"title": "feroxbuster", "description": "Recursive content discovery / directory brute-forcer written in Rust.",
         "install": ["sudo apt install -y feroxbuster"], "run": ["feroxbuster -h"], "url": "https://github.com/epi052/feroxbuster", "tags": ["web", "bruteforce"]},
        {"title": "Gobuster", "description": "Directory, DNS, vhost and S3 brute-forcing tool.",
         "install": ["sudo apt install -y gobuster"], "run": ["gobuster -h"], "url": "https://github.com/OJ/gobuster", "tags": ["web", "bruteforce"]},
        {"title": "httpx", "description": "Fast and multi-purpose HTTP probing toolkit from ProjectDiscovery.",
         "install": ["go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"], "run": ["httpx -h"], "url": "https://github.com/projectdiscovery/httpx", "tags": ["web", "recon"]},
        {"title": "katana", "description": "Next-generation crawling and spidering framework.",
         "install": ["go install -v github.com/projectdiscovery/katana/cmd/katana@latest"], "run": ["katana -h"], "url": "https://github.com/projectdiscovery/katana", "tags": ["web", "crawler"]},
        {"title": "dalfox", "description": "Powerful, fast XSS scanning and parameter-analysis tool.",
         "install": ["go install -v github.com/hahwul/dalfox/v2@latest"], "run": ["dalfox -h"], "url": "https://github.com/hahwul/dalfox", "tags": ["web", "xss"]},
        {"title": "Arjun", "description": "HTTP parameter discovery suite for hidden GET/POST params.",
         "install": ["pipx install arjun"], "run": ["arjun -h"], "url": "https://github.com/s0md3v/Arjun", "tags": ["web"]},
        {"title": "WhatWeb", "description": "Identify web technologies, CMSes, frameworks and versions.",
         "install": ["sudo apt install -y whatweb"], "run": ["whatweb --help"], "url": "https://github.com/urbanadventurer/WhatWeb", "tags": ["web", "recon"]},
        {"title": "WPScan", "description": "WordPress security scanner for vulnerable plugins, themes and users.",
         "install": ["sudo apt install -y wpscan"], "run": ["wpscan --help"], "url": "https://github.com/wpscanteam/wpscan", "tags": ["web", "scanner"]},
        {"title": "Nikto", "description": "Classic web-server scanner for dangerous files and misconfigurations.",
         "install": ["sudo apt install -y nikto"], "run": ["nikto -Help"], "url": "https://github.com/sullo/nikto", "tags": ["web", "scanner"]},
    ],
    "vuln_scanning": [
        {"title": "Nuclei", "description": "Fast, template-based vulnerability scanner from ProjectDiscovery.",
         "install": ["go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"], "run": ["nuclei -h"], "url": "https://github.com/projectdiscovery/nuclei", "tags": ["scanner", "web"]},
        {"title": "Trivy", "description": "All-in-one scanner for containers, filesystems, git repos and IaC.",
         "install": ["sudo apt install -y trivy"], "run": ["trivy --help"], "url": "https://github.com/aquasecurity/trivy", "tags": ["scanner", "cloud"]},
    ],
    "sql_injection": [
        {"title": "sqlmap", "description": "Automatic SQL injection detection and database takeover tool.",
         "install": ["sudo apt install -y sqlmap"], "run": ["sqlmap --help"], "url": "https://github.com/sqlmapproject/sqlmap", "tags": ["web", "sql"]},
        {"title": "Ghauri", "description": "Advanced, automated SQL injection detection & exploitation tool.",
         "install": ["pipx install ghauri"], "run": ["ghauri --help"], "url": "https://github.com/r0oth3x49/ghauri", "tags": ["web", "sql"]},
    ],
    "wordlist_generator": [
        {"title": "Hashcat", "description": "The world's fastest password recovery / GPU hash cracker.",
         "install": ["sudo apt install -y hashcat"], "run": ["hashcat --help"], "url": "https://hashcat.net/hashcat/", "tags": ["credentials", "bruteforce"]},
        {"title": "John the Ripper", "description": "Versatile password cracker supporting hundreds of hash formats.",
         "install": ["sudo apt install -y john"], "run": ["john"], "url": "https://www.openwall.com/john/", "tags": ["credentials", "bruteforce"]},
        {"title": "Hydra", "description": "Fast parallel online login brute-forcer for 50+ protocols.",
         "install": ["sudo apt install -y hydra"], "run": ["hydra -h"], "url": "https://github.com/vanhauser-thc/thc-hydra", "tags": ["bruteforce", "credentials"]},
        {"title": "name-that-hash", "description": "Identify the type of a hash before cracking it.",
         "install": ["pipx install name-that-hash"], "run": ["nth --help"], "url": "https://github.com/HashPals/Name-That-Hash", "tags": ["credentials"]},
        {"title": "CeWL", "description": "Custom wordlist generator that spiders a target site.",
         "install": ["sudo apt install -y cewl"], "run": ["cewl --help"], "url": "https://github.com/digininja/CeWL", "tags": ["credentials", "recon"]},
    ],
    "exploit_framework": [
        {"title": "Metasploit Framework", "description": "The definitive framework for developing and executing exploits.",
         "install": ["sudo apt install -y metasploit-framework"], "run": ["msfconsole"], "url": "https://github.com/rapid7/metasploit-framework", "tags": ["exploit"]},
        {"title": "SearchSploit (Exploit-DB)", "description": "Offline command-line search of the Exploit Database archive.",
         "install": ["sudo apt install -y exploitdb"], "run": ["searchsploit"], "url": "https://gitlab.com/exploit-database/exploitdb", "tags": ["exploit"]},
        {"title": "Commix", "description": "Automated OS command injection detection and exploitation.",
         "install": ["sudo apt install -y commix"], "run": ["commix --help"], "url": "https://github.com/commixproject/commix", "tags": ["web", "exploit"]},
    ],
    "active_directory": [
        {"title": "NetExec", "description": "Swiss-army knife for pentesting networks (the maintained CrackMapExec).",
         "install": ["pipx install git+https://github.com/Pennyw0rth/NetExec"], "run": ["nxc --help"], "url": "https://github.com/Pennyw0rth/NetExec", "tags": ["active-directory"]},
        {"title": "Impacket", "description": "Python classes for crafting and abusing Windows network protocols (SMB, MSRPC, Kerberos).",
         "install": ["pipx install impacket"], "run": ["impacket-secretsdump -h"], "url": "https://github.com/fortra/impacket", "tags": ["active-directory"]},
        {"title": "BloodHound.py", "description": "Python ingestor that collects Active Directory data for BloodHound.",
         "install": ["pipx install bloodhound"], "run": ["bloodhound-python -h"], "url": "https://github.com/dirkjanm/BloodHound.py", "tags": ["active-directory"]},
        {"title": "Certipy", "description": "Enumerate and abuse Active Directory Certificate Services (AD CS).",
         "install": ["pipx install certipy-ad"], "run": ["certipy -h"], "url": "https://github.com/ly4k/Certipy", "tags": ["active-directory"]},
        {"title": "Kerbrute", "description": "Fast Kerberos pre-auth username enumeration and password spraying.",
         "install": ["go install github.com/ropnop/kerbrute@latest"], "run": ["kerbrute -h"], "url": "https://github.com/ropnop/kerbrute", "tags": ["active-directory", "bruteforce"]},
        {"title": "Responder", "description": "LLMNR/NBT-NS/mDNS poisoner and rogue authentication server.",
         "install": ["sudo apt install -y responder"], "run": ["responder -h"], "url": "https://github.com/lgandx/Responder", "tags": ["active-directory", "network"]},
        {"title": "bloodyAD", "description": "Interact with and abuse Active Directory objects over LDAP.",
         "install": ["pipx install bloodyAD"], "run": ["bloodyAD --help"], "url": "https://github.com/CravateRouge/bloodyAD", "tags": ["active-directory"]},
        {"title": "Coercer", "description": "Coerce Windows machines to authenticate via multiple RPC methods.",
         "install": ["pipx install coercer"], "run": ["coercer -h"], "url": "https://github.com/p0dalirius/Coercer", "tags": ["active-directory"]},
    ],
    "post_exploitation": [
        {"title": "Sliver", "description": "Cross-platform adversary-emulation / C2 framework by Bishop Fox.",
         "install": ["curl https://sliver.sh/install | sudo bash"], "run": ["sliver"], "url": "https://github.com/BishopFox/sliver", "tags": ["c2"]},
        {"title": "pwncat-cs", "description": "Post-exploitation platform: upgraded reverse shells and privesc helpers.",
         "install": ["pipx install pwncat-cs"], "run": ["pwncat-cs --help"], "url": "https://github.com/calebstewart/pwncat", "tags": ["c2", "privesc"]},
        {"title": "Chisel", "description": "Fast TCP/UDP tunnel over HTTP for pivoting through firewalls.",
         "install": ["go install github.com/jpillora/chisel@latest"], "run": ["chisel --help"], "url": "https://github.com/jpillora/chisel", "tags": ["network", "c2"]},
        {"title": "ligolo-ng", "description": "Advanced tunneling/pivoting using a TUN interface.",
         "install": ["go install github.com/nicocha30/ligolo-ng/cmd/agent@latest", "go install github.com/nicocha30/ligolo-ng/cmd/proxy@latest"], "run": ["proxy -h"], "url": "https://github.com/nicocha30/ligolo-ng", "tags": ["network", "c2"]},
    ],
    "privilege_escalation": [
        {"title": "LinPEAS", "description": "Linux privilege-escalation enumeration script (part of PEASS-ng).",
         "install": ["git clone https://github.com/peass-ng/PEASS-ng.git"], "run": ["echo 'Run: bash PEASS-ng/linPEAS/linpeas.sh on the target'"], "url": "https://github.com/peass-ng/PEASS-ng", "tags": ["privesc"]},
        {"title": "pspy", "description": "Snoop on Linux processes without root to spot cron jobs and secrets.",
         "install": ["git clone https://github.com/DominicBreuker/pspy.git"], "run": ["echo 'Download a release binary from the pspy repo and run ./pspy64'"], "url": "https://github.com/DominicBreuker/pspy", "tags": ["privesc", "forensics"]},
        {"title": "GTFOBins lookup (gtfoblookup)", "description": "Offline search of GTFOBins for privesc via misconfigured binaries.",
         "install": ["pipx install gtfoblookup"], "run": ["gtfoblookup -h"], "url": "https://github.com/nccgroup/GTFOBLookup", "tags": ["privesc"]},
    ],
    "wireless_attack": [
        {"title": "Aircrack-ng", "description": "Complete suite to assess Wi-Fi network security (capture and crack).",
         "install": ["sudo apt install -y aircrack-ng"], "run": ["aircrack-ng --help"], "url": "https://www.aircrack-ng.org", "tags": ["wireless"]},
        {"title": "Wifite", "description": "Automated wireless auditor that attacks WEP/WPA/WPS networks.",
         "install": ["sudo apt install -y wifite"], "run": ["sudo wifite -h"], "url": "https://github.com/derv82/wifite2", "tags": ["wireless"]},
        {"title": "Bettercap", "description": "Swiss-army knife for network attacks and monitoring (Wi-Fi, BLE, MITM).",
         "install": ["sudo apt install -y bettercap"], "run": ["sudo bettercap -h"], "url": "https://github.com/bettercap/bettercap", "tags": ["wireless", "network", "web"]},
        {"title": "hcxdumptool", "description": "Capture PMKID/handshakes from WLAN devices for offline cracking.",
         "install": ["sudo apt install -y hcxdumptool hcxtools"], "run": ["hcxdumptool -h"], "url": "https://github.com/ZerBea/hcxdumptool", "tags": ["wireless"]},
    ],
    "network_sniffing": [
        {"title": "Wireshark", "description": "The world's foremost network protocol analyzer.",
         "install": ["sudo apt install -y wireshark"], "run": ["wireshark"], "url": "https://www.wireshark.org", "tags": ["forensics", "network"]},
        {"title": "tcpdump", "description": "Powerful command-line packet capture and analysis.",
         "install": ["sudo apt install -y tcpdump"], "run": ["sudo tcpdump -h"], "url": "https://www.tcpdump.org", "tags": ["network"]},
        {"title": "mitmproxy", "description": "Interactive, scriptable TLS-capable intercepting HTTP proxy.",
         "install": ["pipx install mitmproxy"], "run": ["mitmproxy --version"], "url": "https://github.com/mitmproxy/mitmproxy", "tags": ["web", "network"]},
        {"title": "Ettercap", "description": "Comprehensive suite for man-in-the-middle attacks on a LAN.",
         "install": ["sudo apt install -y ettercap-graphical"], "run": ["sudo ettercap --help"], "url": "https://github.com/Ettercap/ettercap", "tags": ["network"]},
    ],
    "forensics": [
        {"title": "Volatility 3", "description": "Advanced memory forensics framework for RAM analysis.",
         "install": ["pipx install volatility3"], "run": ["vol -h"], "url": "https://github.com/volatilityfoundation/volatility3", "tags": ["forensics"]},
        {"title": "binwalk", "description": "Firmware/file analysis and extraction of embedded content.",
         "install": ["sudo apt install -y binwalk"], "run": ["binwalk -h"], "url": "https://github.com/ReFirmLabs/binwalk", "tags": ["forensics", "reversing"]},
        {"title": "Autopsy / Sleuth Kit", "description": "Disk-image forensics and file-system analysis toolkit.",
         "install": ["sudo apt install -y sleuthkit autopsy"], "run": ["echo 'Run: autopsy (then open the printed URL) or use tsk_* tools'"], "url": "https://www.sleuthkit.org", "tags": ["forensics"]},
        {"title": "ExifTool", "description": "Read, write and edit metadata in images, documents and media.",
         "install": ["sudo apt install -y libimage-exiftool-perl"], "run": ["exiftool -ver"], "url": "https://exiftool.org", "tags": ["forensics", "osint"]},
        {"title": "Foremost", "description": "Recover files (carving) from disk images by header/footer.",
         "install": ["sudo apt install -y foremost"], "run": ["foremost -h"], "url": "https://foremost.sourceforge.net", "tags": ["forensics"]},
    ],
    "reverse_engineering": [
        {"title": "Ghidra", "description": "NSA's software reverse-engineering suite with a powerful decompiler.",
         "install": ["sudo apt install -y ghidra"], "run": ["ghidra"], "url": "https://ghidra-sre.org", "tags": ["reversing"]},
        {"title": "radare2", "description": "Portable command-line reverse-engineering and binary analysis framework.",
         "install": ["sudo apt install -y radare2"], "run": ["r2 -h"], "url": "https://github.com/radareorg/radare2", "tags": ["reversing"]},
        {"title": "Cutter", "description": "Free GUI for reverse engineering, powered by Rizin.",
         "install": ["sudo apt install -y cutter"], "run": ["cutter"], "url": "https://github.com/rizinorg/cutter", "tags": ["reversing"]},
        {"title": "jadx", "description": "Decompile Android APK/DEX to readable Java source.",
         "install": ["sudo apt install -y jadx"], "run": ["jadx --help"], "url": "https://github.com/skylot/jadx", "tags": ["reversing", "mobile"]},
        {"title": "pwndbg", "description": "GDB plugin that makes exploit development and RE far easier.",
         "install": ["git clone https://github.com/pwndbg/pwndbg.git", "cd pwndbg && ./setup.sh"], "run": ["echo 'Launch gdb; pwndbg loads automatically'"], "url": "https://github.com/pwndbg/pwndbg", "tags": ["reversing", "exploit"]},
    ],
    "binary_exploitation": [
        {"title": "pwntools", "description": "The CTF and exploit-development framework for Python.",
         "install": ["pipx install pwntools"], "run": ["pwn --help"], "url": "https://github.com/Gallopsled/pwntools", "tags": ["exploit"]},
        {"title": "ROPgadget", "description": "Search for ROP gadgets in binaries to build exploit chains.",
         "install": ["pipx install ROPGadget"], "run": ["ROPgadget --help"], "url": "https://github.com/JonathanSalwan/ROPgadget", "tags": ["exploit", "reversing"]},
        {"title": "one_gadget", "description": "Find one-shot execve gadgets in libc for exploitation.",
         "install": ["sudo gem install one_gadget"], "run": ["one_gadget --help"], "url": "https://github.com/david942j/one_gadget", "tags": ["exploit"]},
    ],
    "mobile_security": [
        {"title": "MobSF", "description": "Mobile Security Framework: automated static & dynamic APK/IPA analysis.",
         "install": ["git clone https://github.com/MobSF/Mobile-Security-Framework-MobSF.git", "cd Mobile-Security-Framework-MobSF && ./setup.sh"], "run": ["echo 'Run ./run.sh inside the MobSF folder, then open http://localhost:8000'"], "url": "https://github.com/MobSF/Mobile-Security-Framework-MobSF", "tags": ["mobile"]},
        {"title": "objection", "description": "Runtime mobile exploration toolkit powered by Frida.",
         "install": ["pipx install objection"], "run": ["objection --help"], "url": "https://github.com/sensepost/objection", "tags": ["mobile"]},
        {"title": "Frida", "description": "Dynamic instrumentation toolkit for hooking apps at runtime.",
         "install": ["pipx install frida-tools"], "run": ["frida --version"], "url": "https://frida.re", "tags": ["mobile", "reversing"]},
        {"title": "apktool", "description": "Reverse-engineer, decode and rebuild Android APK resources.",
         "install": ["sudo apt install -y apktool"], "run": ["apktool --version"], "url": "https://github.com/iBotPeaches/Apktool", "tags": ["mobile", "reversing"]},
    ],
    "cloud_security": [
        {"title": "Prowler", "description": "Security assessment and hardening for AWS, Azure and GCP.",
         "install": ["pipx install prowler"], "run": ["prowler -h"], "url": "https://github.com/prowler-cloud/prowler", "tags": ["cloud"]},
        {"title": "ScoutSuite", "description": "Multi-cloud security auditing tool (AWS, Azure, GCP, OCI).",
         "install": ["pipx install scoutsuite"], "run": ["scout --help"], "url": "https://github.com/nccgroup/ScoutSuite", "tags": ["cloud"]},
        {"title": "Pacu", "description": "Offensive AWS exploitation framework.",
         "install": ["pipx install pacu"], "run": ["pacu --help"], "url": "https://github.com/RhinoSecurityLabs/pacu", "tags": ["cloud"]},
    ],
    "container_k8s": [
        {"title": "kube-hunter", "description": "Hunt for security weaknesses in Kubernetes clusters.",
         "install": ["pipx install kube-hunter"], "run": ["kube-hunter --help"], "url": "https://github.com/aquasecurity/kube-hunter", "tags": ["cloud"]},
        {"title": "kube-bench", "description": "Check Kubernetes against the CIS Benchmark.",
         "install": ["go install github.com/aquasecurity/kube-bench@latest"], "run": ["kube-bench --help"], "url": "https://github.com/aquasecurity/kube-bench", "tags": ["cloud"]},
    ],
    "phishing_attack": [
        {"title": "Gophish", "description": "Full-featured open-source phishing campaign framework.",
         "install": ["git clone https://github.com/gophish/gophish.git"], "run": ["echo 'Download a Gophish release, unzip and run ./gophish'"], "url": "https://github.com/gophish/gophish", "tags": ["social-engineering"]},
        {"title": "Evilginx2", "description": "Man-in-the-middle phishing framework that bypasses 2FA via session cookies.",
         "install": ["go install github.com/kgretzky/evilginx2@latest"], "run": ["sudo evilginx2 -h"], "url": "https://github.com/kgretzky/evilginx2", "tags": ["social-engineering"]},
        {"title": "Zphisher", "description": "Automated phishing tool with many ready-made templates.",
         "install": ["git clone https://github.com/htr-tech/zphisher.git", "cd zphisher && chmod +x zphisher.sh"], "run": ["echo 'Run ./zphisher.sh inside the zphisher folder'"], "url": "https://github.com/htr-tech/zphisher", "tags": ["social-engineering"]},
    ],
    "social_engineering": [
        {"title": "SET (Social-Engineer Toolkit)", "description": "The classic framework for social-engineering attacks.",
         "install": ["sudo apt install -y set"], "run": ["sudo setoolkit"], "url": "https://github.com/trustedsec/social-engineer-toolkit", "tags": ["social-engineering"]},
    ],
    "payload_creation": [
        {"title": "MSFvenom", "description": "Metasploit's payload generator and encoder.",
         "install": ["sudo apt install -y metasploit-framework"], "run": ["msfvenom -h"], "url": "https://github.com/rapid7/metasploit-framework", "tags": ["payload"]},
        {"title": "Villain", "description": "Backdoor/C2 generator that manages multiple reverse shells and payloads.",
         "install": ["git clone https://github.com/t3l3machus/Villain.git", "cd Villain && pip3 install -r requirements.txt"], "run": ["echo 'Run python3 Villain.py inside the Villain folder'"], "url": "https://github.com/t3l3machus/Villain", "tags": ["payload", "c2"]},
        {"title": "Donut", "description": "Generate position-independent shellcode from .NET assemblies, EXE/DLL.",
         "install": ["pipx install donut-shellcode"], "run": ["echo 'Use the donut Python module to build shellcode'"], "url": "https://github.com/TheWover/donut", "tags": ["payload"]},
    ],
    "cryptography": [
        {"title": "Ciphey", "description": "Automated decryption/decoding using natural-language detection.",
         "install": ["pipx install ciphey"], "run": ["ciphey --help"], "url": "https://github.com/Ciphey/Ciphey", "tags": ["credentials"]},
        {"title": "hashID", "description": "Identify the type of a given hash.",
         "install": ["sudo apt install -y hashid"], "run": ["hashid -h"], "url": "https://github.com/psypanda/hashID", "tags": ["credentials"]},
    ],
    "steganography": [
        {"title": "Steghide", "description": "Hide and extract data in image and audio files.",
         "install": ["sudo apt install -y steghide"], "run": ["steghide --help"], "url": "https://steghide.sourceforge.net", "tags": ["steganography"]},
        {"title": "Stegseek", "description": "Lightning-fast Steghide cracker to recover hidden data.",
         "install": ["sudo apt install -y stegseek || (wget https://github.com/RickdeJager/stegseek/releases/latest/download/stegseek.deb && sudo apt install -y ./stegseek.deb)"], "run": ["stegseek --help"], "url": "https://github.com/RickdeJager/stegseek", "tags": ["steganography"]},
        {"title": "zsteg", "description": "Detect stego and hidden data in PNG and BMP files.",
         "install": ["sudo gem install zsteg"], "run": ["zsteg --help"], "url": "https://github.com/zed-0xff/zsteg", "tags": ["steganography"]},
    ],
    "fuzzing": [
        {"title": "wfuzz", "description": "Web application fuzzer for brute-forcing parameters and paths.",
         "install": ["sudo apt install -y wfuzz"], "run": ["wfuzz -h"], "url": "https://github.com/xmendez/wfuzz", "tags": ["web", "fuzzing"]},
        {"title": "AFL++", "description": "State-of-the-art coverage-guided fuzzing framework.",
         "install": ["sudo apt install -y aflplusplus"], "run": ["afl-fuzz -h"], "url": "https://github.com/AFLplusplus/AFLplusplus", "tags": ["fuzzing"]},
    ],
    "devsecops": [
        {"title": "TruffleHog", "description": "Find leaked credentials and secrets across git history and more.",
         "install": ["go install github.com/trufflesecurity/trufflehog/v3@latest"], "run": ["trufflehog --help"], "url": "https://github.com/trufflesecurity/trufflehog", "tags": ["credentials"]},
        {"title": "Gitleaks", "description": "Detect hardcoded secrets and API keys in code and git repos.",
         "install": ["sudo apt install -y gitleaks"], "run": ["gitleaks --help"], "url": "https://github.com/gitleaks/gitleaks", "tags": ["credentials"]},
        {"title": "Semgrep", "description": "Fast, open-source static analysis for finding bugs and vulnerabilities.",
         "install": ["pipx install semgrep"], "run": ["semgrep --help"], "url": "https://github.com/semgrep/semgrep", "tags": ["scanner"]},
    ],
    "api_security": [
        {"title": "kiterunner", "description": "Content discovery tool built for modern API endpoints and routes.",
         "install": ["go install github.com/assetnote/kiterunner@latest"], "run": ["kr --help"], "url": "https://github.com/assetnote/kiterunner", "tags": ["web"]},
    ],
    "threat_intel": [
        {"title": "MISP", "description": "Open-source threat-intelligence sharing platform.",
         "install": ["echo 'MISP is best deployed via its official installer or Docker: https://github.com/MISP/MISP'"], "run": ["echo 'See https://github.com/MISP/MISP for deployment'"], "url": "https://github.com/MISP/MISP", "tags": ["forensics"]},
        {"title": "YARA", "description": "Pattern-matching engine to identify and classify malware.",
         "install": ["sudo apt install -y yara"], "run": ["yara --help"], "url": "https://github.com/VirusTotal/yara", "tags": ["forensics"]},
    ],
    "blue_team": [
        {"title": "Suricata", "description": "High-performance IDS/IPS and network security monitoring engine.",
         "install": ["sudo apt install -y suricata"], "run": ["suricata --help"], "url": "https://github.com/OISF/suricata", "tags": ["forensics", "network"]},
        {"title": "Zeek", "description": "Powerful network analysis framework for security monitoring.",
         "install": ["sudo apt install -y zeek"], "run": ["zeek --help"], "url": "https://github.com/zeek/zeek", "tags": ["forensics", "network"]},
    ],
}


def to_tool(d: dict) -> dict:
    return {
        "title": d["title"],
        "description": d["description"],
        "install": list(d.get("install", [])),
        "run": list(d.get("run", [])),
        "uninstall": list(d.get("uninstall", [])),
        "url": d.get("url", ""),
        "tags": list(d.get("tags", [])),
        "os": list(d.get("os", ["linux"])),
        "archived": False,
        "archived_reason": "",
        "requires_root": bool(d.get("requires_root", False)),
        "installable": True,
        "runnable": True,
        "subgroup": d.get("subgroup", ""),
        "flagship": True,
    }


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in data["categories"]}

    # Map normalized title -> (category_id, index) for the whole catalog.
    title_loc: dict[str, tuple[str, int]] = {}
    for cid, cat in cats.items():
        for i, tool in enumerate(cat.get("tools", [])):
            title_loc.setdefault(norm(tool.get("title", "")), (cid, i))

    added = upgraded = 0
    for cid, tools in FLAGSHIPS.items():
        if cid not in cats:
            print(f"  ! unknown category {cid}, skipping")
            continue
        for spec in tools:
            new = to_tool(spec)
            key = norm(new["title"])
            if key in title_loc:
                loc_cid, idx = title_loc[key]
                existing = cats[loc_cid]["tools"][idx]
                # Upgrade authoritative fields, keep the entry where it lives.
                existing.update({
                    "description": new["description"],
                    "install": new["install"],
                    "run": new["run"],
                    "url": new["url"] or existing.get("url", ""),
                    "tags": sorted(set(existing.get("tags", [])) | set(new["tags"])),
                    "os": ["linux"],
                    "installable": True,
                    "runnable": True,
                    "archived": False,
                    "flagship": True,
                })
                upgraded += 1
            else:
                cats[cid].setdefault("tools", []).append(new)
                title_loc[key] = (cid, len(cats[cid]["tools"]) - 1)
                added += 1

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})
    data["meta"]["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Flagships upgraded: {upgraded}  |  added: {added}  |  total tools now: {total}")


if __name__ == "__main__":
    main()

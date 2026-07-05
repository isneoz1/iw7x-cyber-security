# NeoZ - Complete Cybersecurity Arsenal

**Version 2.0.0** - The ULTIMATE cybersecurity toolkit with 15,000+ tools

> "Absolutely all tools in the world in cybersecurity" - Literally everything you need for pentesting, hacking, forensics, and more.

## 📊 What's Inside

- **50+ Categories** of cybersecurity tools
- **15,000+ Tools** total
- **Multiple Specializations**: OSINT, Web, Wireless, Exploitation, RE, Forensics, and MORE
- **All Platforms**: Linux, Windows, macOS, Web-based
- **Complete Documentation** for each tool

## 🗂️ Main Tool Categories

### Reconnaissance & OSINT
- theHarvester - Email & subdomain harvesting
- OWASP Amass - Advanced subdomain enumeration
- SpiderFoot - Automated OSINT framework
- Recon-ng - Web reconnaissance
- Maltego - Visual link analysis
- Shodan CLI - IoT device search

### Network Scanning
- **Nmap** - Port scanning (Essential)
- Masscan - Internet-scale scanner
- Zmap - Network-wide research scanner
- Nessus - Professional vulnerability scanner
- OpenVAS - Open source vulnerability assessment
- Qualys - Cloud-based scanning

### Web Application Testing
- Burp Suite - Professional web penetration testing
- OWASP ZAP - Free web security scanner
- SQLmap - SQL injection detection
- Nikto - Web server scanner
- w3af - Web attack framework
- Wfuzz - Web fuzzer
- Gobuster - Fast directory enumeration
- XSStrike - XSS scanner

### Wireless & WiFi
- Aircrack-ng - WiFi password cracking
- Hashcat - GPU password cracking
- John the Ripper - CPU cracking
- Wireshark - Packet analyzer
- Kismet - WiFi detector
- Bettercap - Network penetration framework

### Exploitation & Frameworks
- Metasploit Framework - The industry standard
- Empire - PowerShell exploitation
- BeEF - Browser exploitation
- Commix - Command injection framework
- Cobalt Strike - Advanced C2 platform
- Sliver - Open source C2

### Reverse Engineering
- Ghidra - NSA's reverse engineering tool
- IDA Pro - Professional disassembler
- Radare2 - Open source framework
- Cutter - Radare2 GUI
- Binary Ninja - Advanced binary analysis
- GDB - GNU Debugger
- Frida - Dynamic instrumentation

### Malware Analysis
- Cuckoo Sandbox - Automated analysis
- VirusTotal - Online scanner
- Hybrid-Analysis - Online malware service
- Volatility - Memory forensics
- YARA - Pattern matching
- Strings - Binary analysis

### Digital Forensics
- Sleuth Kit - Digital forensics framework
- Autopsy - GUI for Sleuth Kit
- FTK Imager - Forensic imaging
- EnCase - Enterprise platform
- ExifTool - Metadata extraction
- SIFT - SANS toolkit

### Password Cracking
- Hashcat - GPU-accelerated (FASTEST)
- John the Ripper - CPU cracking
- Rainbowcrack - Rainbow tables
- Medusa - Parallel login brute-forcer
- Hydra - Multi-protocol brute-forcer
- Online Hash Tools - Quick lookups

### Phishing & Social Engineering
- Gophish - Phishing framework
- Social Engineer Toolkit - SE framework
- King Phisher - Campaign simulator
- Phishery - HTTP credential harvester
- MailSniper - Exchange server scanning

### Steganography & Hiding
- Steghide - Hide data in media
- steg_detect - Detect hidden data
- OutGuess - Universal steganography
- Exiftool - Metadata manipulation

### Cryptography
- OpenSSL - SSL/TLS and crypto
- GnuPG - PGP encryption
- Hashlib - Cryptographic hashing
- CryptTool - Educational tool

### Mobile Security
- Frida - Mobile instrumentation
- Burp Suite Mobile - Mobile proxy
- APKTool - APK decompiler
- jadx - DEX decompiler

### Cloud Security
- CloudMapper - AWS mapper
- Scout2 - AWS auditor
- Prowler - AWS checks
- Falco - Container runtime security

### Active Directory
- BloodHound - AD domain mapper
- Mimikatz - Credential extraction
- SharpHound - PowerShell ingestor
- Responder - LLMNR poisoning
- Kerbrute - Kerberos enumeration
- Rubeus - Kerberos tool
- Impacket - Network protocol library

### API Security
- Postman - API testing
- Insomnia - REST client
- Burp Suite - API testing
- Swagger UI - Documentation

### Database Security
- SQLmap - SQL injection
- NoSQLMap - NoSQL injection
- MySQL Scanner - MySQL vulnerabilities
- MSSQL Scripts - MSSQL exploitation

### Container & Kubernetes
- Kubesec - Kubernetes scanner
- kube-bench - CIS benchmark
- kube-hunter - Kubernetes pentest
- Docker Bench - Docker audit
- Trivy - Vulnerability scanner

### Incident Response
- YARA - Pattern matching
- Sigma - Detection rules
- OSQuery - System query
- Splunk - SIEM platform
- Elastic Stack - Open source SIEM
- Wazuh - Security monitoring

### WAF & IDS Bypass
- WAFW00F - WAF fingerprinting
- WAF Ninja - Bypass techniques
- Fragroute - Packet fragmenting

### Code Analysis
- SonarQube - Code quality
- Checkmarx - SAST platform
- Semgrep - Static analysis
- Bandit - Python security
- Pylint - Python analyzer

### DNS Tools
- DNSRecon - DNS reconnaissance
- Dig - Domain information
- Nslookup - DNS lookup

### Anonymity & Privacy
- Tor Browser - Anonymized browsing
- Proxychains - Proxy routing
- OpenVPN - VPN client
- Wireguard - Modern VPN

### Payload Generation
- msfvenom - Metasploit payloads
- Veil - Payload obfuscation
- Shellter - Shellcode injection

### Post-Exploitation
- Mimikatz - Credential extraction
- PowerShell Empire - Post-ex framework
- Responder - LLMNR poisoning

## 🚀 Quick Start

### Installation

```bash
cd NeoZ
python -m pip install -r requirements.txt
./install.sh
```

### Usage

```bash
# Run the main application
python neoz.py

# Or use CLI directly
python -m neoz.cli --help

# Install tools
python neoz.py --install nmap

# Search for tools
python neoz.py --search "sql injection"

# List all categories
python neoz.py --categories
```

## 📦 File Structure

```
NeoZ/
├── catalog_complete.json       # 15,000+ tools database
├── neoz/
│   ├── app.py                  # Main application
│   ├── catalog_complete.py     # Catalog loader
│   ├── security_tools.py       # Security tools classes
│   ├── advanced_tools.py       # Advanced/specialized tools
│   ├── models.py               # Data models
│   ├── system.py               # System utilities
│   ├── ui.py                   # UI components
│   └── cli.py                  # Command-line interface
└── requirements.txt            # Python dependencies
```

## 🔧 New Features in v2.0

### ✨ Expanded Tool Coverage
- **+7,000 New Tools** from v1.5
- **50 Categories** instead of 38
- Complete coverage of ALL cybersecurity domains

### 🎯 Advanced Modules
- `security_tools.py` - Organized tool classes
- `catalog_complete.py` - Catalog management
- `advanced_tools.py` - Specialized tools

### 📊 Statistics
```
Total Categories: 50
Total Tools: 15,000+
Supported Platforms: Linux, Windows, macOS, Web
Languages: English, Français
```

## 🎓 Tool Categories by Difficulty

### Beginner
- Nmap - Network scanning
- Wireshark - Packet analysis
- SQLmap - SQL injection
- Nikto - Web scanning

### Intermediate
- Metasploit - Exploitation
- Burp Suite - Web penetration
- Ghidra - Reverse engineering
- Aircrack-ng - WiFi cracking

### Advanced
- Frida - Dynamic instrumentation
- Radare2 - Advanced reverse engineering
- YARA - Malware analysis
- Volatility - Memory forensics

## 🛡️ Security Domains Covered

- ✅ OSINT & Reconnaissance
- ✅ Network Scanning & Enumeration
- ✅ Web Application Security
- ✅ Wireless & WiFi
- ✅ Exploitation & Frameworks
- ✅ Reverse Engineering
- ✅ Malware Analysis
- ✅ Digital Forensics
- ✅ Password Cracking
- ✅ Phishing & Social Engineering
- ✅ Steganography
- ✅ Cryptography
- ✅ Mobile Security
- ✅ Cloud Security
- ✅ Active Directory
- ✅ API Security
- ✅ Database Security
- ✅ Container Security
- ✅ Incident Response
- ✅ WAF Bypass
- ✅ IDS/IPS Evasion
- ✅ Code Analysis
- ✅ C2 Frameworks
- ✅ And MORE...

## 💻 Requirements

- Python 3.8+
- Linux/Kali Linux recommended
- 4GB+ RAM
- 10GB+ disk space (for tools installation)

## 📚 Documentation

Each tool in the catalog includes:
- **Title**: Tool name
- **Description**: What it does
- **Install Commands**: How to install
- **Run Commands**: How to execute
- **Tags**: Feature labels
- **OS Support**: Compatible platforms
- **Root Required**: Privilege level needed

## 🔗 Useful Links

- [GitHub Repository](https://github.com/isneoz1/iw7x-cyber-security)
- [Python 3](https://www.python.org/)
- [Kali Linux](https://www.kali.org/)

## 📝 License

This project is a comprehensive security toolkit for educational and authorized security testing purposes only.

## 👨‍💻 Author

**NeoZ Team** - Cybersecurity Toolkit

---

**Version 2.0.0** | Updated: July 2026

> "In cybersecurity, knowledge is power. This toolkit gives you access to the world's most comprehensive arsenal of security tools."

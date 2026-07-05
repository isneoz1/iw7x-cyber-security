"""
OSINT & Reconnaissance Tools Module
"""

import subprocess
import platform
import json
from typing import List, Dict, Any

class OSINTTools:
    """Open Source Intelligence Tools"""
    
    def __init__(self):
        self.tools = {
            'theHarvester': {
                'description': 'Email and subdomain harvesting',
                'install_cmd': 'pip install theHarvester',
                'run_cmd': 'theHarvester -d {domain} -b google'
            },
            'amass': {
                'description': 'Subdomain enumeration',
                'install_cmd': 'go install -v github.com/OWASP/Amass/v3/...@latest',
                'run_cmd': 'amass enum -d {domain}'
            },
            'shodan': {
                'description': 'IoT device search',
                'install_cmd': 'pip install shodan',
                'run_cmd': 'shodan search {query}'
            },
            'spiderfoot': {
                'description': 'Automated OSINT',
                'install_cmd': 'git clone https://github.com/smicallef/spiderfoot.git',
                'run_cmd': 'python sf.py -l 127.0.0.1:5001'
            },
            'recon-ng': {
                'description': 'Web reconnaissance framework',
                'install_cmd': 'git clone https://github.com/lanmaster53/recon-ng.git',
                'run_cmd': 'python recon-ng'
            }
        }
    
    def list_tools(self) -> List[str]:
        """List all OSINT tools"""
        return list(self.tools.keys())
    
    def get_tool_info(self, tool: str) -> Dict[str, Any]:
        """Get tool information"""
        return self.tools.get(tool, {})
    
    def install_tool(self, tool: str) -> bool:
        """Install an OSINT tool"""
        if tool not in self.tools:
            print(f"Tool {tool} not found")
            return False
        
        cmd = self.tools[tool]['install_cmd']
        try:
            subprocess.run(cmd.split(), check=True)
            print(f"✓ {tool} installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install {tool}: {e}")
            return False


class ReconnaissanceTools:
    """Network Reconnaissance Tools"""
    
    def __init__(self):
        self.tools = {
            'nmap': {
                'description': 'Port scanning',
                'install_cmd': 'apt-get install nmap',
                'common_scans': {
                    'basic': 'nmap {target}',
                    'service_version': 'nmap -sV {target}',
                    'aggressive': 'nmap -sV -A {target}',
                    'udp': 'nmap -sU {target}',
                }
            },
            'masscan': {
                'description': 'Fast internet-scale scanner',
                'install_cmd': 'git clone https://github.com/robertdavidgraham/masscan',
                'common_scans': {
                    'quick': 'masscan -p443 {target}'
                }
            },
            'zmap': {
                'description': 'Network-wide scanner',
                'install_cmd': 'git clone https://github.com/zmap/zmap.git',
                'common_scans': {}
            }
        }
    
    def get_nmap_scan(self, scan_type: str, target: str) -> str:
        """Generate Nmap scan command"""
        scans = self.tools['nmap']['common_scans']
        if scan_type in scans:
            return scans[scan_type].replace('{target}', target)
        return f"nmap {target}"


class WebSecurityTools:
    """Web Application Security Tools"""
    
    def __init__(self):
        self.tools = {
            'burpsuite': 'Professional web testing',
            'owasp_zap': 'Free web scanner',
            'sqlmap': 'SQL injection detection',
            'nikto': 'Web server scanner',
            'w3af': 'Web attack framework',
            'wfuzz': 'Web fuzzer',
            'dirbuster': 'Directory enumeration',
            'gobuster': 'Fast dir/DNS fuzzing',
            'xsstrike': 'XSS scanner'
        }
    
    def list_web_tools(self) -> Dict[str, str]:
        """List web security tools"""
        return self.tools


class WirelessTools:
    """Wireless & WiFi Security Tools"""
    
    def __init__(self):
        self.tools = {
            'aircrack-ng': 'WiFi cracking',
            'hashcat': 'GPU password cracking',
            'john': 'Password cracking',
            'wireshark': 'Packet analyzer',
            'kismet': 'WiFi detector',
            'tshark': 'CLI packet capture',
            'bettercap': 'Network penetration'
        }


class ExploitationTools:
    """Exploitation Frameworks"""
    
    def __init__(self):
        self.frameworks = {
            'metasploit': {
                'description': 'Penetration testing framework',
                'cmd': 'msfconsole',
                'modules': ['exploit', 'payload', 'encoder', 'nop', 'post']
            },
            'empire': {
                'description': 'PowerShell exploitation',
                'cmd': 'python empire'
            },
            'beef': {
                'description': 'Browser exploitation',
                'cmd': 'ruby beef'
            },
            'commix': {
                'description': 'Command injection',
                'cmd': 'python commix.py'
            }
        }


class ReverseEngineeringTools:
    """Reverse Engineering Tools"""
    
    def __init__(self):
        self.tools = {
            'ghidra': 'NSA reverse engineering',
            'ida_pro': 'Professional disassembler',
            'radare2': 'Open source framework',
            'cutter': 'Radare2 GUI',
            'gdb': 'GNU debugger',
            'frida': 'Dynamic instrumentation'
        }


class MalwareAnalysisTools:
    """Malware Analysis Tools"""
    
    def __init__(self):
        self.tools = {
            'cuckoo': 'Automated sandbox',
            'virustotal': 'Online scanner',
            'volatility': 'Memory forensics',
            'yara': 'Pattern matching',
            'strings': 'Binary analysis',
            'file': 'File identification'
        }


class ForensicsTools:
    """Digital Forensics Tools"""
    
    def __init__(self):
        self.tools = {
            'sleuthkit': 'Forensic framework',
            'autopsy': 'GUI forensics',
            'volatility': 'Memory forensics',
            'exiftool': 'Metadata extraction',
            'ewf-tools': 'EWF utilities'
        }


class PasswordCrackingTools:
    """Password & Hash Cracking Tools"""
    
    def __init__(self):
        self.tools = {
            'hashcat': 'GPU cracking - fastest',
            'john': 'CPU cracking',
            'rainbowcrack': 'Rainbow tables',
            'hydra': 'Login brute-force',
            'medusa': 'Parallel brute-force'
        }


class AllSecurityTools:
    """Complete compilation of all security tools"""
    
    CATEGORIES = {
        'OSINT': OSINTTools(),
        'Reconnaissance': ReconnaissanceTools(),
        'Web Security': WebSecurityTools(),
        'Wireless': WirelessTools(),
        'Exploitation': ExploitationTools(),
        'Reverse Engineering': ReverseEngineeringTools(),
        'Malware Analysis': MalwareAnalysisTools(),
        'Forensics': ForensicsTools(),
        'Password Cracking': PasswordCrackingTools(),
    }
    
    @classmethod
    def get_all_tools(cls) -> Dict[str, List[str]]:
        """Get all tools organized by category"""
        all_tools = {}
        for category, tools_obj in cls.CATEGORIES.items():
            if hasattr(tools_obj, 'list_tools'):
                all_tools[category] = tools_obj.list_tools()
            elif hasattr(tools_obj, 'tools'):
                all_tools[category] = list(tools_obj.tools.keys())
        return all_tools
    
    @classmethod
    def get_total_count(cls) -> int:
        """Get total number of tools"""
        total = 0
        all_tools = cls.get_all_tools()
        for tools_list in all_tools.values():
            total += len(tools_list)
        return total

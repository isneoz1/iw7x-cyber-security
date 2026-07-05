"""
Advanced & Specialized Cybersecurity Tools
Covers: AD, API, Database, Container, Incident Response, etc.
"""

from typing import List, Dict, Any

class ActiveDirectoryTools:
    """Active Directory & Domain Controller Attack Tools"""
    
    TOOLS = {
        'bloodhound': {
            'title': 'BloodHound',
            'description': 'AD domain relationship mapper',
            'tags': ['ad', 'enumeration', 'privilege-escalation']
        },
        'mimikatz': {
            'title': 'Mimikatz',
            'description': 'Windows credential extraction',
            'tags': ['ad', 'credentials', 'windows']
        },
        'sharphound': {
            'title': 'SharpHound',
            'description': 'BloodHound PowerShell ingestor',
            'tags': ['ad', 'powershell']
        },
        'responder': {
            'title': 'Responder',
            'description': 'LLMNR/NBNS poisoning',
            'tags': ['ad', 'ntlm', 'mitm']
        },
        'kerbrute': {
            'title': 'Kerbrute',
            'description': 'Kerberos user enumeration',
            'tags': ['ad', 'kerberos']
        },
        'pykerbrute': {
            'title': 'PyKerbRute',
            'description': 'Python Kerberos brute-force',
            'tags': ['ad', 'kerberos', 'brute-force']
        },
        'rubeus': {
            'title': 'Rubeus',
            'description': 'Kerberos interaction tool',
            'tags': ['ad', 'kerberos']
        },
        'impacket': {
            'title': 'Impacket',
            'description': 'Network protocol library',
            'tags': ['ad', 'exploitation']
        }
    }


class APISecurityTools:
    """API Security Testing Tools"""
    
    TOOLS = {
        'postman': {
            'title': 'Postman',
            'description': 'API testing platform',
            'tags': ['api', 'testing']
        },
        'insomnia': {
            'title': 'Insomnia',
            'description': 'REST API client',
            'tags': ['api', 'testing']
        },
        'burpsuite_api': {
            'title': 'Burp Suite Pro',
            'description': 'API security testing',
            'tags': ['api', 'web', 'professional']
        },
        'swagger': {
            'title': 'Swagger UI',
            'description': 'API documentation',
            'tags': ['api', 'documentation']
        },
        'owasp_api_security': {
            'title': 'OWASP API Security',
            'description': 'API testing guidelines',
            'tags': ['api', 'guidelines']
        }
    }


class DatabaseSecurityTools:
    """Database Security & Scanning Tools"""
    
    TOOLS = {
        'sqlmap': {
            'title': 'SQLMap',
            'description': 'SQL injection detection',
            'tags': ['database', 'sql-injection']
        },
        'nosqlmap': {
            'title': 'NoSQLMap',
            'description': 'NoSQL injection tool',
            'tags': ['database', 'nosql']
        },
        'dbf': {
            'title': 'Database Footprinter',
            'description': 'Database enumeration',
            'tags': ['database', 'enumeration']
        },
        'mysql_scanner': {
            'title': 'MySQL Scanner',
            'description': 'MySQL vulnerability scanner',
            'tags': ['database', 'mysql']
        },
        'mssql_scripts': {
            'title': 'MSSQL Scripts',
            'description': 'MSSQL exploitation',
            'tags': ['database', 'mssql']
        }
    }


class ContainerSecurityTools:
    """Kubernetes & Container Security Tools"""
    
    TOOLS = {
        'kubesec': {
            'title': 'Kubesec',
            'description': 'Kubernetes security scanner',
            'tags': ['kubernetes', 'container']
        },
        'kube-bench': {
            'title': 'kube-bench',
            'description': 'CIS Kubernetes benchmark',
            'tags': ['kubernetes', 'compliance']
        },
        'kube-hunter': {
            'title': 'kube-hunter',
            'description': 'Kubernetes penetration testing',
            'tags': ['kubernetes', 'pentest']
        },
        'docker_bench': {
            'title': 'Docker Bench',
            'description': 'Docker security audit',
            'tags': ['docker', 'audit']
        },
        'trivy': {
            'title': 'Trivy',
            'description': 'Container vulnerability scanner',
            'tags': ['container', 'scanning']
        }
    }


class IncidentResponseTools:
    """Incident Response & Detection Tools"""
    
    TOOLS = {
        'yara': {
            'title': 'YARA',
            'description': 'Malware pattern matching',
            'tags': ['incident-response', 'detection']
        },
        'sigma': {
            'title': 'Sigma',
            'description': 'Detection rule language',
            'tags': ['incident-response', 'detection']
        },
        'osquery': {
            'title': 'OSQuery',
            'description': 'System query engine',
            'tags': ['incident-response', 'detection']
        },
        'splunk': {
            'title': 'Splunk',
            'description': 'SIEM platform',
            'tags': ['incident-response', 'siem']
        },
        'elastic': {
            'title': 'Elastic Stack',
            'description': 'Open source SIEM',
            'tags': ['incident-response', 'siem', 'open-source']
        },
        'wazuh': {
            'title': 'Wazuh',
            'description': 'Security monitoring platform',
            'tags': ['incident-response', 'detection']
        }
    }


class WAFBypassTools:
    """Web Application Firewall Bypass Tools"""
    
    TOOLS = {
        'wafw00f': {
            'title': 'WAFW00F',
            'description': 'WAF fingerprinting',
            'tags': ['waf', 'bypass']
        },
        'wafninja': {
            'title': 'WAF Ninja',
            'description': 'WAF bypass techniques',
            'tags': ['waf', 'bypass']
        },
        'sqlmap_waf': {
            'title': 'SQLMap WAF Bypass',
            'description': 'SQLMap WAF evasion',
            'tags': ['waf', 'sql-injection']
        }
    }


class IDS_IPSBypassTools:
    """IDS/IPS Evasion Tools"""
    
    TOOLS = {
        'nmap_decoys': {
            'title': 'Nmap Decoys',
            'description': 'IDS evasion scanning',
            'tags': ['ids-evasion', 'scanning']
        },
        'fragroute': {
            'title': 'Fragroute',
            'description': 'Network packet fragmenting',
            'tags': ['ids-evasion', 'network']
        },
        'inetsim': {
            'title': 'INetSim',
            'description': 'Network simulation',
            'tags': ['ids-evasion', 'simulation']
        }
    }


class CodeAnalysisTools:
    """Static & Dynamic Code Analysis"""
    
    TOOLS = {
        'sonarqube': {
            'title': 'SonarQube',
            'description': 'Code quality analysis',
            'tags': ['code-analysis', 'sast']
        },
        'checkmarx': {
            'title': 'Checkmarx',
            'description': 'SAST platform',
            'tags': ['code-analysis', 'sast', 'commercial']
        },
        'semgrep': {
            'title': 'Semgrep',
            'description': 'Static analysis tool',
            'tags': ['code-analysis', 'sast', 'open-source']
        },
        'bandit': {
            'title': 'Bandit',
            'description': 'Python security checker',
            'tags': ['code-analysis', 'python']
        },
        'pylint': {
            'title': 'Pylint',
            'description': 'Python code analyzer',
            'tags': ['code-analysis', 'python']
        }
    }


class C2FrameworksTools:
    """Command & Control Frameworks"""
    
    TOOLS = {
        'empire': {
            'title': 'PowerShell Empire',
            'description': 'Post-exploitation framework',
            'tags': ['c2', 'powershell']
        },
        'metasploit_multi': {
            'title': 'Metasploit Multi Handler',
            'description': 'Multi-protocol handler',
            'tags': ['c2', 'metasploit']
        },
        'cobalt_strike': {
            'title': 'Cobalt Strike',
            'description': 'Commercial adversary simulation',
            'tags': ['c2', 'commercial']
        },
        'sliver': {
            'title': 'Sliver',
            'description': 'C2 platform',
            'tags': ['c2', 'open-source']
        },
        'mythic': {
            'title': 'Mythic',
            'description': 'Modular C2 framework',
            'tags': ['c2', 'framework']
        }
    }


class DDoSTools:
    """Denial of Service Tools"""
    
    TOOLS = {
        'slowhttptest': {
            'title': 'SlowHTTPTest',
            'description': 'Slow HTTP DoS',
            'tags': ['dos', 'http']
        },
        'hping3': {
            'title': 'hping3',
            'description': 'Ping-like tool with DoS',
            'tags': ['dos', 'network']
        },
        'goldeneye': {
            'title': 'GoldenEye',
            'description': 'HTTP DoS tool',
            'tags': ['dos', 'http']
        }
    }


class NetworkMappingTools:
    """Network Visualization & Mapping"""
    
    TOOLS = {
        'gephi': {
            'title': 'Gephi',
            'description': 'Network visualization',
            'tags': ['network', 'visualization']
        },
        'networkx': {
            'title': 'NetworkX',
            'description': 'Python network library',
            'tags': ['network', 'python']
        }
    }


class AllAdvancedTools:
    """Complete collection of advanced tools"""
    
    CATEGORIES = {
        'Active Directory': ActiveDirectoryTools(),
        'API Security': APISecurityTools(),
        'Database Security': DatabaseSecurityTools(),
        'Container Security': ContainerSecurityTools(),
        'Incident Response': IncidentResponseTools(),
        'WAF Bypass': WAFBypassTools(),
        'IDS/IPS Evasion': IDS_IPSBypassTools(),
        'Code Analysis': CodeAnalysisTools(),
        'C2 Frameworks': C2FrameworksTools(),
        'DDoS': DDoSTools(),
        'Network Mapping': NetworkMappingTools(),
    }
    
    @staticmethod
    def count_all_tools() -> int:
        """Count all advanced tools"""
        total = 0
        for category in AllAdvancedTools.CATEGORIES.values():
            if hasattr(category, 'TOOLS'):
                total += len(category.TOOLS)
        return total
    
    @staticmethod
    def export_all_tools() -> Dict[str, List[Dict[str, Any]]]:
        """Export all tools as dictionary"""
        result = {}
        for category_name, category_obj in AllAdvancedTools.CATEGORIES.items():
            if hasattr(category_obj, 'TOOLS'):
                result[category_name] = list(category_obj.TOOLS.values())
        return result

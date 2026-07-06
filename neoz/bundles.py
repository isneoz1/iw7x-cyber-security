"""Task bundles — install a whole curated kit for a job with one command.

    iw7x bundle web        # Web app pentest
    iw7x bundle ad         # Active Directory
    iw7x bundles           # list every kit

Each bundle lists tool names that resolve against the catalog (the curated
flagship entries carry correct, Kali-ready install commands). Anything already
installed is skipped by the underlying package manager.
"""

from __future__ import annotations

# name -> {title, tools:[catalog tool names]}
ALL: dict[str, dict] = {
    "web": {"title": "Web App Pentest", "tools": [
        "nmap", "httpx", "nuclei", "ffuf", "feroxbuster", "dirsearch", "whatweb",
        "wafw00f", "wpscan", "sqlmap", "dalfox", "xsstrike", "gobuster", "gau",
        "katana", "dirb"]},
    "ad": {"title": "Active Directory", "tools": [
        "netexec", "impacket", "bloodhound.py", "certipy", "kerbrute", "responder",
        "mitm6", "ldapdomaindump", "pypykatz", "lsassy", "coercer", "adidnsdump",
        "evil-winrm"]},
    "osint": {"title": "OSINT Recon", "tools": [
        "theharvester", "amass", "subfinder", "spiderfoot", "sherlock", "holehe",
        "maigret", "assetfinder", "waybackurls", "dnsx", "ghunt", "recon-ng",
        "sublist3r"]},
    "wireless": {"title": "Wi-Fi / Wireless", "tools": [
        "aircrack-ng", "wifite", "hcxdumptool", "hcxtools", "reaver", "bully",
        "pixiewps", "kismet", "mdk4", "airgeddon", "wifiphisher"]},
    "pwn": {"title": "Binary Exploitation / CTF", "tools": [
        "pwntools", "gef", "pwndbg", "ropper", "ropgadget", "one_gadget", "checksec",
        "pwninit", "angr", "ghidra", "radare2", "ropr", "rsactftool"]},
    "forensics": {"title": "Forensics / DFIR", "tools": [
        "volatility 3", "binwalk", "bulk_extractor", "exiftool", "foremost", "scalpel",
        "wireshark", "tshark", "regripper", "plaso"]},
    "cloud": {"title": "Cloud & Kubernetes", "tools": [
        "prowler", "scoutsuite", "pacu", "cloudfox", "s3scanner", "cloudbrute",
        "enumerate-iam", "trivy", "kube-hunter", "kube-bench", "kubescape",
        "cloudsplaining"]},
    "passwords": {"title": "Password Cracking", "tools": [
        "hashcat", "john the ripper", "hydra", "medusa", "ncrack", "crunch", "cewl",
        "name-that-hash", "hashid", "crowbar", "rsmangler"]},
    "c2": {"title": "Post-Exploitation / C2", "tools": [
        "sliver", "villain", "pwncat-cs", "chisel", "ligolo-ng", "powershell-empire"]},
    "mobile": {"title": "Mobile Security", "tools": [
        "mobsf", "frida-tools", "objection", "apktool", "jadx", "apkid", "apkleaks",
        "mobsfscan"]},
    "recon": {"title": "Fast Recon Pipeline", "tools": [
        "subfinder", "assetfinder", "amass", "dnsx", "httpx", "httprobe", "naabu",
        "katana", "gau", "waybackurls", "nuclei"]},
    "bugbounty": {"title": "Bug Bounty", "tools": [
        "subfinder", "httpx", "nuclei", "ffuf", "katana", "gau", "waybackurls",
        "dalfox", "gf", "qsreplace", "anew", "arjun", "gowitness"]},
    "malware": {"title": "Malware Analysis", "tools": [
        "yara", "capa", "floss", "binwalk", "radare2", "jadx", "apktool", "exiftool"]},
    "container": {"title": "Container & K8s Security", "tools": [
        "trivy", "kube-hunter", "kube-bench", "kubescape", "kubeaudit", "popeye",
        "peirates", "grype", "syft"]},
    "stego": {"title": "Steganography", "tools": [
        "steghide", "zsteg", "stegseek", "outguess", "exiftool", "binwalk",
        "stegcracker"]},
}


def get(name: str) -> dict | None:
    return ALL.get((name or "").strip().lower())

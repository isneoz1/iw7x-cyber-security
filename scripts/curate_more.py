#!/usr/bin/env python3
"""Add extra curated tool packs to catalog.json.

Second curation batch on top of ``curate_flagships.py``: deep Red Team / AD,
CTF (pwn / crypto / stego / forensics), Cloud & Kubernetes, Web, Recon and
evasion tooling — every entry with correct, Kali-ready install/run commands.

Idempotent: upgrades an existing tool in place (matched by normalized title)
or appends it to its category if missing.

Run:  python scripts/curate_more.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def git_note(folder: str, how: str) -> str:
    return f"echo 'Installed to ./{folder} — {how}'"


PACKS: dict[str, list[dict]] = {
    # ── Red Team / Active Directory (deep) ──────────────────────────────────
    "active_directory": [
        {"title": "ldapdomaindump", "description": "Dump Active Directory info over LDAP into readable HTML/JSON/greppable files.",
         "install": ["pipx install ldapdomaindump"], "run": ["ldapdomaindump -h"], "url": "https://github.com/dirkjanm/ldapdomaindump", "tags": ["active-directory"]},
        {"title": "mitm6", "description": "Abuse IPv6 to become the primary DNS server and relay Windows auth.",
         "install": ["pipx install mitm6"], "run": ["mitm6 -h"], "url": "https://github.com/dirkjanm/mitm6", "tags": ["active-directory", "network"]},
        {"title": "pypykatz", "description": "Pure-Python implementation of Mimikatz — parse LSASS dumps and secrets.",
         "install": ["pipx install pypykatz"], "run": ["pypykatz --help"], "url": "https://github.com/skelsec/pypykatz", "tags": ["active-directory", "credentials"]},
        {"title": "lsassy", "description": "Remotely extract credentials from LSASS memory across a network.",
         "install": ["pipx install lsassy"], "run": ["lsassy --help"], "url": "https://github.com/Hackndo/lsassy", "tags": ["active-directory", "credentials"]},
        {"title": "enum4linux-ng", "description": "Next-gen SMB/RPC enumeration of Windows and Samba hosts.",
         "install": ["pipx install enum4linux-ng"], "run": ["enum4linux-ng -h"], "url": "https://github.com/cddmp/enum4linux-ng", "tags": ["active-directory", "recon"]},
        {"title": "adidnsdump", "description": "Enumerate and dump Active Directory Integrated DNS via LDAP.",
         "install": ["pipx install adidnsdump"], "run": ["adidnsdump -h"], "url": "https://github.com/dirkjanm/adidnsdump", "tags": ["active-directory"]},
        {"title": "ldeep", "description": "In-depth LDAP enumeration utility for Active Directory.",
         "install": ["pipx install ldeep"], "run": ["ldeep --help"], "url": "https://github.com/franc-pentest/ldeep", "tags": ["active-directory"]},
        {"title": "pywerview", "description": "Python port of PowerView for AD reconnaissance from Linux.",
         "install": ["pipx install pywerview"], "run": ["pywerview --help"], "url": "https://github.com/the-useless-one/pywerview", "tags": ["active-directory"]},
        {"title": "Adalanche", "description": "Instantly visualize Active Directory ACL attack paths and permissions.",
         "install": ["go install github.com/lkarlslund/adalanche@latest"], "run": ["adalanche -h"], "url": "https://github.com/lkarlslund/Adalanche", "tags": ["active-directory"]},
        {"title": "krbrelayx", "description": "Kerberos relaying and unconstrained-delegation abuse toolkit.",
         "install": ["git clone https://github.com/dirkjanm/krbrelayx.git"], "run": [git_note("krbrelayx", "run: python3 krbrelayx.py -h")], "url": "https://github.com/dirkjanm/krbrelayx", "tags": ["active-directory"]},
        {"title": "targetedKerberoast", "description": "Kerberoast without a target list by abusing write permissions on SPNs.",
         "install": ["git clone https://github.com/ShutdownRepo/targetedKerberoast.git"], "run": [git_note("targetedKerberoast", "run: python3 targetedKerberoast.py -h")], "url": "https://github.com/ShutdownRepo/targetedKerberoast", "tags": ["active-directory", "credentials"]},
        {"title": "PetitPotam", "description": "Coerce Windows hosts to authenticate via MS-EFSRPC (NTLM relay).",
         "install": ["git clone https://github.com/topotam/PetitPotam.git"], "run": [git_note("PetitPotam", "run: python3 PetitPotam.py -h")], "url": "https://github.com/topotam/PetitPotam", "tags": ["active-directory"]},
        {"title": "gMSADumper", "description": "Read and compute Group Managed Service Account (gMSA) passwords.",
         "install": ["git clone https://github.com/micahvandeusen/gMSADumper.git"], "run": [git_note("gMSADumper", "run: python3 gMSADumper.py -h")], "url": "https://github.com/micahvandeusen/gMSADumper", "tags": ["active-directory", "credentials"]},
    ],
    # ── CTF: binary exploitation / pwn ──────────────────────────────────────
    "binary_exploitation": [
        {"title": "GEF", "description": "GDB Enhanced Features — a modern exploit-dev and RE plugin for GDB.",
         "install": ["wget -q -O ~/.gdbinit-gef.py https://gef.blah.cat/py", "echo 'source ~/.gdbinit-gef.py' >> ~/.gdbinit"], "run": ["echo 'Launch gdb; GEF loads automatically'"], "url": "https://github.com/hugsy/gef", "tags": ["exploit", "reversing"]},
        {"title": "Ropper", "description": "Display info about binaries and search for ROP/JOP gadgets.",
         "install": ["pipx install ropper"], "run": ["ropper --help"], "url": "https://github.com/sashs/Ropper", "tags": ["exploit", "reversing"]},
        {"title": "angr", "description": "Powerful binary analysis and symbolic-execution framework.",
         "install": ["pipx install angr || pip3 install --user angr"], "run": ["echo 'import angr in Python to use the framework'"], "url": "https://github.com/angr/angr", "tags": ["reversing", "exploit"]},
        {"title": "checksec", "description": "Check the security mitigations (NX, PIE, RELRO, canary) of binaries.",
         "install": ["sudo apt install -y checksec"], "run": ["checksec --help"], "url": "https://github.com/slimm609/checksec.sh", "tags": ["exploit", "reversing"]},
        {"title": "pwninit", "description": "Automate CTF pwn setup: patch the loader/libc and build a template.",
         "install": ["cargo install pwninit"], "run": ["pwninit --help"], "url": "https://github.com/io12/pwninit", "tags": ["exploit"]},
    ],
    # ── CTF: cryptography ───────────────────────────────────────────────────
    "cryptography": [
        {"title": "RsaCtfTool", "description": "Attack weak RSA keys and recover plaintext/private keys (CTF favourite).",
         "install": ["git clone https://github.com/RsaCtfTool/RsaCtfTool.git", "cd RsaCtfTool && pip3 install --user -r requirements.txt"], "run": [git_note("RsaCtfTool", "run: python3 RsaCtfTool.py --help")], "url": "https://github.com/RsaCtfTool/RsaCtfTool", "tags": ["credentials"]},
        {"title": "xortool", "description": "Analyse and break multi-byte XOR-encrypted data.",
         "install": ["pipx install xortool"], "run": ["xortool -h"], "url": "https://github.com/hellman/xortool", "tags": ["credentials"]},
    ],
    # ── CTF: steganography ──────────────────────────────────────────────────
    "steganography": [
        {"title": "Outguess", "description": "Universal steganographic tool to hide/extract data in redundant bits.",
         "install": ["sudo apt install -y outguess"], "run": ["outguess -h"], "url": "https://github.com/resurrecting-open-source-projects/outguess", "tags": ["steganography"]},
        {"title": "StegoVeritas", "description": "Throw-everything-at-it stego analyzer for images (metadata, LSB, channels).",
         "install": ["pipx install stegoveritas"], "run": ["stegoveritas -h"], "url": "https://github.com/bannsec/stegoVeritas", "tags": ["steganography"]},
        {"title": "Stegsolve", "description": "Java tool to inspect image bit planes and colour channels for hidden data.",
         "install": ["wget -q http://www.caesum.com/handbook/Stegsolve.jar -O stegsolve.jar", "chmod +x stegsolve.jar"], "run": ["java -jar stegsolve.jar"], "url": "http://www.caesum.com/handbook/stego.htm", "tags": ["steganography"]},
    ],
    # ── CTF / forensics carving ─────────────────────────────────────────────
    "forensics": [
        {"title": "TestDisk & PhotoRec", "description": "Recover lost partitions and carve deleted files from disks/images.",
         "install": ["sudo apt install -y testdisk"], "run": ["testdisk"], "url": "https://www.cgsecurity.org/wiki/TestDisk", "tags": ["forensics"]},
        {"title": "Scalpel", "description": "Fast file carver that recovers files by header/footer definitions.",
         "install": ["sudo apt install -y scalpel"], "run": ["scalpel -h"], "url": "https://github.com/sleuthkit/scalpel", "tags": ["forensics"]},
        {"title": "bulk_extractor", "description": "Scan disk images for emails, URLs, credit cards and other artifacts.",
         "install": ["sudo apt install -y bulk-extractor"], "run": ["bulk_extractor -h"], "url": "https://github.com/simsong/bulk_extractor", "tags": ["forensics"]},
        {"title": "pngcheck", "description": "Verify and dump the internal structure of PNG files (CTF stego triage).",
         "install": ["sudo apt install -y pngcheck"], "run": ["pngcheck -h"], "url": "http://www.libpng.org/pub/png/apps/pngcheck.html", "tags": ["forensics", "steganography"]},
    ],
    # ── Cloud security (deep) ───────────────────────────────────────────────
    "cloud_security": [
        {"title": "CloudFox", "description": "Find exploitable attack paths in cloud (AWS/Azure/GCP) environments.",
         "install": ["go install github.com/BishopFox/cloudfox@latest"], "run": ["cloudfox --help"], "url": "https://github.com/BishopFox/cloudfox", "tags": ["cloud"]},
        {"title": "S3Scanner", "description": "Scan for open/misconfigured S3 buckets and dump their contents.",
         "install": ["pipx install s3scanner"], "run": ["s3scanner --help"], "url": "https://github.com/sa7mon/S3Scanner", "tags": ["cloud"]},
        {"title": "CloudBrute", "description": "Find a company's infrastructure and buckets across cloud providers.",
         "install": ["go install github.com/0xsha/CloudBrute@latest"], "run": ["CloudBrute -h"], "url": "https://github.com/0xsha/CloudBrute", "tags": ["cloud", "recon"]},
        {"title": "enumerate-iam", "description": "Brute-force enumerate the permissions of a set of AWS credentials.",
         "install": ["git clone https://github.com/andresriancho/enumerate-iam.git", "cd enumerate-iam && pip3 install --user -r requirements.txt"], "run": [git_note("enumerate-iam", "run: python3 enumerate-iam.py --help")], "url": "https://github.com/andresriancho/enumerate-iam", "tags": ["cloud"]},
    ],
    # ── Containers / Kubernetes (deep) ──────────────────────────────────────
    "container_k8s": [
        {"title": "Kubescape", "description": "Kubernetes security platform: scan clusters, YAML and Helm against frameworks.",
         "install": ["curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash"], "run": ["kubescape"], "url": "https://github.com/kubescape/kubescape", "tags": ["cloud"]},
        {"title": "kubeaudit", "description": "Audit Kubernetes clusters against common security concerns.",
         "install": ["go install github.com/Shopify/kubeaudit@latest"], "run": ["kubeaudit -h"], "url": "https://github.com/Shopify/kubeaudit", "tags": ["cloud"]},
        {"title": "Popeye", "description": "Scan live Kubernetes clusters for misconfigurations and stale resources.",
         "install": ["go install github.com/derailed/popeye@latest"], "run": ["popeye --help"], "url": "https://github.com/derailed/popeye", "tags": ["cloud"]},
        {"title": "Peirates", "description": "Kubernetes penetration-testing tool for escalating from a pod.",
         "install": ["go install github.com/inguardians/peirates@latest"], "run": ["peirates"], "url": "https://github.com/inguardians/peirates", "tags": ["cloud"]},
    ],
    # ── Web attack (more) ───────────────────────────────────────────────────
    "web_attack": [
        {"title": "dirsearch", "description": "Feature-rich web path scanner / directory brute-forcer.",
         "install": ["pipx install dirsearch"], "run": ["dirsearch --help"], "url": "https://github.com/maurosoria/dirsearch", "tags": ["web", "bruteforce"]},
        {"title": "gowitness", "description": "Fast web screenshotting utility for large scopes.",
         "install": ["go install github.com/sensepost/gowitness@latest"], "run": ["gowitness --help"], "url": "https://github.com/sensepost/gowitness", "tags": ["web", "recon"]},
        {"title": "XSStrike", "description": "Advanced XSS detection suite with a fuzzing and payload-generation engine.",
         "install": ["git clone https://github.com/s0md3v/XSStrike.git", "cd XSStrike && pip3 install --user -r requirements.txt"], "run": [git_note("XSStrike", "run: python3 xsstrike.py -h")], "url": "https://github.com/s0md3v/XSStrike", "tags": ["web", "xss"]},
        {"title": "jwt_tool", "description": "Test, tamper and crack JSON Web Tokens for common vulnerabilities.",
         "install": ["git clone https://github.com/ticarpi/jwt_tool.git", "cd jwt_tool && pip3 install --user -r requirements.txt"], "run": [git_note("jwt_tool", "run: python3 jwt_tool.py -h")], "url": "https://github.com/ticarpi/jwt_tool", "tags": ["web", "api"]},
        {"title": "wafw00f", "description": "Identify and fingerprint Web Application Firewalls.",
         "install": ["pipx install wafw00f"], "run": ["wafw00f -h"], "url": "https://github.com/EnableSecurity/wafw00f", "tags": ["web", "recon"]},
    ],
    # ── OSINT / recon (more) ────────────────────────────────────────────────
    "osint": [
        {"title": "assetfinder", "description": "Find domains and subdomains related to a given domain.",
         "install": ["go install github.com/tomnomnom/assetfinder@latest"], "run": ["assetfinder -h"], "url": "https://github.com/tomnomnom/assetfinder", "tags": ["recon"]},
        {"title": "gau", "description": "Fetch known URLs from AlienVault OTX, Wayback and Common Crawl.",
         "install": ["go install github.com/lc/gau/v2/cmd/gau@latest"], "run": ["gau --help"], "url": "https://github.com/lc/gau", "tags": ["recon", "web"]},
        {"title": "waybackurls", "description": "Pull every URL the Wayback Machine knows for a domain.",
         "install": ["go install github.com/tomnomnom/waybackurls@latest"], "run": ["waybackurls -h"], "url": "https://github.com/tomnomnom/waybackurls", "tags": ["recon", "web"]},
        {"title": "gospider", "description": "Fast web spider written in Go for crawling and URL discovery.",
         "install": ["go install github.com/jaeles-project/gospider@latest"], "run": ["gospider -h"], "url": "https://github.com/jaeles-project/gospider", "tags": ["recon", "crawler", "web"]},
        {"title": "dnsrecon", "description": "Comprehensive DNS enumeration and zone-transfer testing tool.",
         "install": ["sudo apt install -y dnsrecon"], "run": ["dnsrecon -h"], "url": "https://github.com/darkoperator/dnsrecon", "tags": ["recon"]},
        {"title": "fierce", "description": "DNS reconnaissance tool for locating non-contiguous IP space.",
         "install": ["sudo apt install -y fierce"], "run": ["fierce -h"], "url": "https://github.com/mschwager/fierce", "tags": ["recon"]},
        {"title": "puredns", "description": "Fast, accurate subdomain bruteforcing and resolving with wildcard filtering.",
         "install": ["go install github.com/d3mondev/puredns/v2@latest"], "run": ["puredns --help"], "url": "https://github.com/d3mondev/puredns", "tags": ["recon", "bruteforce"]},
        {"title": "shuffledns", "description": "Massdns wrapper for subdomain enumeration and resolution.",
         "install": ["go install github.com/projectdiscovery/shuffledns/cmd/shuffledns@latest"], "run": ["shuffledns -h"], "url": "https://github.com/projectdiscovery/shuffledns", "tags": ["recon"]},
    ],
    # ── Vulnerability scanning (more) ───────────────────────────────────────
    "vuln_scanning": [
        {"title": "Wapiti", "description": "Black-box web application vulnerability scanner.",
         "install": ["sudo apt install -y wapiti"], "run": ["wapiti -h"], "url": "https://github.com/wapiti-scanner/wapiti", "tags": ["web", "scanner"]},
        {"title": "testssl.sh", "description": "Check a server's TLS/SSL ciphers, protocols and known flaws.",
         "install": ["sudo apt install -y testssl.sh"], "run": ["testssl.sh --help"], "url": "https://github.com/drwetter/testssl.sh", "tags": ["scanner", "web"]},
        {"title": "sslscan", "description": "Quickly enumerate SSL/TLS ciphers and certificate details of a service.",
         "install": ["sudo apt install -y sslscan"], "run": ["sslscan --help"], "url": "https://github.com/rbsec/sslscan", "tags": ["scanner", "web"]},
    ],
    # ── Payloads / evasion (more) ───────────────────────────────────────────
    "payload_creation": [
        {"title": "MSFPC", "description": "MSFvenom Payload Creator — generate payloads with a single command.",
         "install": ["git clone https://github.com/g0tmi1k/msfpc.git"], "run": [git_note("msfpc", "run: ./msfpc.sh")], "url": "https://github.com/g0tmi1k/msfpc", "tags": ["payload"]},
        {"title": "ScareCrow", "description": "Generate EDR-evading loaders for shellcode payloads.",
         "install": ["go install github.com/optiv/ScareCrow@latest"], "run": ["ScareCrow -h"], "url": "https://github.com/optiv/ScareCrow", "tags": ["payload"]},
    ],
}


def to_tool(d: dict) -> dict:
    return {
        "title": d["title"], "description": d["description"],
        "install": list(d.get("install", [])), "run": list(d.get("run", [])),
        "uninstall": list(d.get("uninstall", [])), "url": d.get("url", ""),
        "tags": list(d.get("tags", [])), "os": ["linux"],
        "archived": False, "archived_reason": "", "requires_root": False,
        "installable": True, "runnable": True, "subgroup": "", "flagship": True,
    }


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in data["categories"]}

    title_loc: dict[str, tuple[str, int]] = {}
    for cid, cat in cats.items():
        for i, tool in enumerate(cat.get("tools", [])):
            title_loc.setdefault(norm(tool.get("title", "")), (cid, i))

    added = upgraded = 0
    for cid, tools in PACKS.items():
        if cid not in cats:
            print(f"  ! unknown category {cid}, skipping")
            continue
        for spec in tools:
            new = to_tool(spec)
            key = norm(new["title"])
            if key in title_loc:
                loc_cid, idx = title_loc[key]
                existing = cats[loc_cid]["tools"][idx]
                existing.update({
                    "description": new["description"], "install": new["install"],
                    "run": new["run"], "url": new["url"] or existing.get("url", ""),
                    "tags": sorted(set(existing.get("tags", [])) | set(new["tags"])),
                    "os": ["linux"], "installable": True, "runnable": True,
                    "archived": False, "flagship": True,
                })
                upgraded += 1
            else:
                cats[cid].setdefault("tools", []).append(new)
                title_loc[key] = (cid, len(cats[cid]["tools"]) - 1)
                added += 1

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Extra packs upgraded: {upgraded}  |  added: {added}  |  total tools now: {total}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fifth curation wave — hand-added well-known tools with Kali-ready commands.

Upgrade-in-place if present, add if missing (dedup by alphanumeric key).
Run: python scripts/curate_essentials4.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / "catalog.json"


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def T(title, desc, install, run, url, tags, cat):
    return {"title": title, "description": desc, "install": install, "run": run,
            "url": url, "tags": tags, "_cat": cat}


TOOLS = [
    # recon / osint
    T("Findomain", "Fast cross-platform subdomain enumerator.", ["sudo apt install -y findomain"], ["findomain -h"], "https://github.com/Findomain/Findomain", ["recon"], "information_gathering"),
    T("shuffledns", "Wrapper around massdns for fast subdomain brute/resolve.", ["go install github.com/projectdiscovery/shuffledns/v2/cmd/shuffledns@latest"], ["shuffledns -h"], "https://github.com/projectdiscovery/shuffledns", ["recon"], "information_gathering"),
    T("dnsgen", "Generate DNS permutations for subdomain discovery.", ["pipx install dnsgen"], ["dnsgen -h"], "https://github.com/AlephNullSK/dnsgen", ["recon"], "information_gathering"),
    T("dnstwist", "Domain-name permutation engine to detect typosquatting/phishing.", ["pipx install dnstwist"], ["dnstwist --help"], "https://github.com/elceef/dnstwist", ["recon", "osint"], "information_gathering"),
    T("cero", "Scrape domain names from TLS certificates.", ["go install github.com/glebarez/cero@latest"], ["cero -h"], "https://github.com/glebarez/cero", ["recon"], "information_gathering"),
    T("aquatone", "Visual inspection of websites across many hosts.", ["go install github.com/michenriksen/aquatone@latest"], ["aquatone -h"], "https://github.com/michenriksen/aquatone", ["recon", "web"], "information_gathering"),
    T("gospider", "Fast web spider written in Go.", ["go install github.com/jaeles-project/gospider@latest"], ["gospider -h"], "https://github.com/jaeles-project/gospider", ["recon", "web"], "information_gathering"),
    T("LinkFinder", "Discover endpoints and their parameters in JavaScript files.", ["pipx install linkfinder || git clone https://github.com/GerbenJavado/LinkFinder"], ["linkfinder -h"], "https://github.com/GerbenJavado/LinkFinder", ["recon", "web"], "web_attack"),
    T("SecretFinder", "Find sensitive data (API keys, tokens) in JavaScript files.", ["git clone https://github.com/m4ll0k/SecretFinder"], ["python3 SecretFinder/SecretFinder.py -h"], "https://github.com/m4ll0k/SecretFinder", ["recon", "credentials"], "information_gathering"),
    T("cariddi", "Crawl endpoints, secrets, tokens and juicy info from a list of hosts.", ["go install github.com/edoardottt/cariddi/cmd/cariddi@latest"], ["cariddi -h"], "https://github.com/edoardottt/cariddi", ["recon", "web"], "information_gathering"),
    # web
    T("CMSeeK", "CMS detection and exploitation suite (WordPress, Joomla, Drupal…).", ["git clone https://github.com/Tuhinshubhra/CMSeeK"], ["python3 CMSeeK/cmseek.py -h"], "https://github.com/Tuhinshubhra/CMSeeK", ["web", "scanner"], "web_attack"),
    T("Ghauri", "Advanced automatic SQL injection detection and exploitation.", ["pipx install ghauri"], ["ghauri -h"], "https://github.com/r0oth3x49/ghauri", ["web"], "sql_injection"),
    T("NoSQLMap", "Automated NoSQL database enumeration and injection.", ["git clone https://github.com/codingo/NoSQLMap"], ["python3 NoSQLMap/nosqlmap.py"], "https://github.com/codingo/NoSQLMap", ["web"], "sql_injection"),
    T("tplmap", "Server-Side Template Injection detection and exploitation.", ["git clone https://github.com/epinna/tplmap"], ["python3 tplmap/tplmap.py -h"], "https://github.com/epinna/tplmap", ["web"], "web_attack"),
    T("SSRFmap", "Automatic SSRF fuzzer and exploitation tool.", ["git clone https://github.com/swisskyrepo/SSRFmap"], ["python3 SSRFmap/ssrfmap.py -h"], "https://github.com/swisskyrepo/SSRFmap", ["web"], "web_attack"),
    T("kxss", "Scan for reflected parameters (XSS discovery helper).", ["go install github.com/Emoe/kxss@latest"], ["kxss -h"], "https://github.com/Emoe/kxss", ["web"], "xss_attack"),
    T("XSpear", "Powerful XSS scanning and parameter analysis (Ruby).", ["sudo gem install XSpear"], ["xspear -h"], "https://github.com/hahwul/XSpear", ["web"], "xss_attack"),
    T("jwt-cracker", "Brute-force HS256 JWT secrets.", ["sudo npm install -g jwt-cracker"], ["jwt-cracker"], "https://github.com/lmammino/jwt-cracker", ["web", "credentials"], "web_attack"),
    # AD / network
    T("smbmap", "Enumerate SMB shares and permissions across a domain.", ["sudo apt install -y smbmap"], ["smbmap -h"], "https://github.com/ShawnDEvans/smbmap", ["active-directory"], "active_directory"),
    T("windapsearch", "Enumerate Active Directory users/groups via LDAP.", ["git clone https://github.com/ropnop/windapsearch"], ["python3 windapsearch/windapsearch.py -h"], "https://github.com/ropnop/windapsearch", ["active-directory"], "active_directory"),
    T("bloodyAD", "Active Directory privilege escalation swiss-army knife.", ["pipx install bloodyAD"], ["bloodyAD -h"], "https://github.com/CravateRouge/bloodyAD", ["active-directory"], "active_directory"),
    T("Certipy", "Enumerate and abuse Active Directory Certificate Services.", ["pipx install certipy-ad"], ["certipy -h"], "https://github.com/ly4k/Certipy", ["active-directory"], "active_directory"),
    T("enum4linux-ng", "Next-gen Windows/Samba enumeration tool.", ["pipx install enum4linux-ng"], ["enum4linux-ng -h"], "https://github.com/cddmp/enum4linux-ng", ["active-directory"], "active_directory"),
    T("kerbrute", "Quickly brute-force and enumerate valid AD accounts via Kerberos.", ["go install github.com/ropnop/kerbrute@latest"], ["kerbrute -h"], "https://github.com/ropnop/kerbrute", ["active-directory", "bruteforce"], "active_directory"),
    # privesc
    T("pspy", "Monitor Linux processes without root (spot cron/privesc).", ["sudo apt install -y pspy || (curl -sL https://github.com/DominicBreuker/pspy/releases/latest/download/pspy64 -o /usr/local/bin/pspy && chmod +x /usr/local/bin/pspy)"], ["pspy"], "https://github.com/DominicBreuker/pspy", ["privesc"], "privilege_escalation"),
    T("linux-exploit-suggester", "Suggest kernel/privesc exploits for a Linux host.", ["git clone https://github.com/The-Z-Labs/linux-exploit-suggester"], ["bash linux-exploit-suggester/linux-exploit-suggester.sh"], "https://github.com/The-Z-Labs/linux-exploit-suggester", ["privesc"], "privilege_escalation"),
    T("linux-smart-enumeration", "Linux enumeration with increasing verbosity levels.", ["git clone https://github.com/diego-treitos/linux-smart-enumeration"], ["bash linux-smart-enumeration/lse.sh"], "https://github.com/diego-treitos/linux-smart-enumeration", ["privesc"], "privilege_escalation"),
    T("traitor", "Automatic Linux local privilege escalation via known exploits.", ["go install github.com/liamg/traitor/cmd/traitor@latest"], ["traitor -h"], "https://github.com/liamg/traitor", ["privesc"], "privilege_escalation"),
    T("Sudo-Killer", "Find sudo misconfigurations for privilege escalation.", ["git clone https://github.com/TH3xACE/SUDO_KILLER"], ["bash SUDO_KILLER/sudo_killer.sh -h"], "https://github.com/TH3xACE/SUDO_KILLER", ["privesc"], "privilege_escalation"),
    # c2 / pivot
    T("Sliver", "Powerful cross-platform adversary emulation / C2 framework.", ["curl https://sliver.sh/install | sudo bash"], ["sliver-server"], "https://github.com/BishopFox/sliver", ["c2"], "post_exploitation"),
    T("chisel", "Fast TCP/UDP tunnel over HTTP (pivoting).", ["go install github.com/jpillora/chisel@latest"], ["chisel -h"], "https://github.com/jpillora/chisel", ["c2", "network"], "post_exploitation"),
    T("ligolo-ng", "Advanced, tunneling/pivoting tool using a TUN interface.", ["go install github.com/nicocha30/ligolo-ng/cmd/agent@latest", "go install github.com/nicocha30/ligolo-ng/cmd/proxy@latest"], ["ligolo-ng -h"], "https://github.com/nicocha30/ligolo-ng", ["c2", "network"], "post_exploitation"),
    T("sshuttle", "Transparent proxy / poor-man's VPN over SSH (pivoting).", ["sudo apt install -y sshuttle"], ["sshuttle --help"], "https://github.com/sshuttle/sshuttle", ["network"], "post_exploitation"),
    # RE / pwn
    T("Rizin", "Free reverse-engineering framework (radare2 fork).", ["sudo apt install -y rizin"], ["rizin -h"], "https://github.com/rizinorg/rizin", ["reversing"], "reverse_engineering"),
    T("Cutter", "Free reverse-engineering GUI powered by Rizin.", ["sudo apt install -y cutter"], ["cutter"], "https://github.com/rizinorg/cutter", ["reversing"], "reverse_engineering"),
    T("pwndbg", "GDB plugin that makes debugging and exploit-dev much easier.", ["git clone https://github.com/pwndbg/pwndbg && ./pwndbg/setup.sh"], ["gdb"], "https://github.com/pwndbg/pwndbg", ["reversing", "pwn"], "binary_exploitation"),
    T("pwntools", "CTF framework and exploit development library for Python.", ["pipx install pwntools"], ["pwn --help"], "https://github.com/Gallopsled/pwntools", ["pwn", "reversing"], "binary_exploitation"),
    T("one_gadget", "Find one-shot RCE gadgets in libc.", ["sudo gem install one_gadget"], ["one_gadget"], "https://github.com/david942j/one_gadget", ["pwn"], "binary_exploitation"),
    T("Ropper", "Display info about binaries and find ROP/JOP gadgets.", ["pipx install ropper"], ["ropper -h"], "https://github.com/sashs/Ropper", ["pwn", "reversing"], "binary_exploitation"),
    T("dex2jar", "Convert Android .dex files to .jar for analysis.", ["sudo apt install -y dex2jar"], ["d2j-dex2jar -h"], "https://github.com/pxb1988/dex2jar", ["mobile", "reversing"], "mobile_security"),
    # forensics
    T("Chainsaw", "Fast Windows event-log and MFT hunting with Sigma rules.", ["curl -sL https://github.com/WithSecureLabs/chainsaw/releases/latest/download/chainsaw_all_platforms+rules.zip -o /tmp/chainsaw.zip && sudo unzip -o /tmp/chainsaw.zip -d /opt/chainsaw"], ["/opt/chainsaw/chainsaw/chainsaw --help"], "https://github.com/WithSecureLabs/chainsaw", ["forensics", "blue_team"], "forensics"),
    T("NetworkMiner", "Network forensic analysis tool (PCAP parsing).", ["sudo apt install -y networkminer || echo 'Run via mono: mono NetworkMiner.exe'"], ["networkminer"], "https://www.netresec.com/?page=NetworkMiner", ["forensics", "network"], "forensics"),
    T("ssdeep", "Fuzzy hashing to identify similar/altered files.", ["sudo apt install -y ssdeep"], ["ssdeep -h"], "https://ssdeep-project.github.io/ssdeep/", ["forensics"], "forensics"),
    # cloud
    T("CloudBrute", "Find a company's cloud infrastructure and buckets.", ["go install github.com/0xsha/CloudBrute@latest"], ["cloudbrute -h"], "https://github.com/0xsha/CloudBrute", ["cloud"], "cloud_security"),
    T("CloudFox", "Find exploitable attack paths in cloud infrastructure.", ["go install github.com/BishopFox/cloudfox@latest"], ["cloudfox -h"], "https://github.com/BishopFox/cloudfox", ["cloud"], "cloud_security"),
    T("S3Scanner", "Scan for open S3 buckets and dump their contents.", ["pipx install s3scanner"], ["s3scanner -h"], "https://github.com/sa7mon/S3Scanner", ["cloud"], "cloud_security"),
    T("kdigger", "Context-discovery tool for Kubernetes penetration testing.", ["go install github.com/quarkslab/kdigger/cmd/kdigger@latest"], ["kdigger -h"], "https://github.com/quarkslab/kdigger", ["cloud"], "container_k8s"),
    # phishing / SE
    T("Evilginx2", "Man-in-the-middle framework for phishing with 2FA bypass.", ["go install github.com/kgretzky/evilginx2@latest"], ["evilginx2 -h"], "https://github.com/kgretzky/evilginx2", ["social-engineering"], "phishing_attack"),
    T("GoPhish", "Open-source phishing framework for awareness testing.", ["curl -sL https://github.com/gophish/gophish/releases/latest/download/gophish-v0.12.1-linux-64bit.zip -o /tmp/gophish.zip && sudo unzip -o /tmp/gophish.zip -d /opt/gophish"], ["/opt/gophish/gophish"], "https://github.com/gophish/gophish", ["social-engineering"], "phishing_attack"),
    # fuzzing
    T("boofuzz", "Network protocol fuzzing framework (Sulley successor).", ["pipx install boofuzz"], ["python3 -c 'import boofuzz'"], "https://github.com/jtpereyda/boofuzz", ["fuzzing"], "fuzzing"),
    # stego
    T("StegSeek", "Lightning-fast steghide cracker.", ["sudo apt install -y stegseek || (curl -sL https://github.com/RickdeJager/stegseek/releases/latest/download/stegseek_0.6-1.deb -o /tmp/ss.deb && sudo dpkg -i /tmp/ss.deb)"], ["stegseek --help"], "https://github.com/RickdeJager/stegseek", ["steganography"], "steganography"),
    T("zsteg", "Detect stego data hidden in PNG and BMP files.", ["sudo gem install zsteg"], ["zsteg --help"], "https://github.com/zed-0xff/zsteg", ["steganography"], "steganography"),
    # crypto / ctf
    T("RsaCtfTool", "Attack weak RSA keys / recover private keys in CTFs.", ["git clone https://github.com/RsaCtfTool/RsaCtfTool && pipx install ./RsaCtfTool"], ["RsaCtfTool -h"], "https://github.com/RsaCtfTool/RsaCtfTool", ["crypto", "ctf"], "cryptography"),
    T("Ciphey", "Automated decryption/decoding tool using AI and heuristics.", ["pipx install ciphey"], ["ciphey --help"], "https://github.com/Ciphey/Ciphey", ["crypto"], "cryptography"),
    T("featherduster", "Automated, modular cryptanalysis tool.", ["git clone https://github.com/nccgroup/featherduster && pipx install ./featherduster"], ["featherduster -h"], "https://github.com/nccgroup/featherduster", ["crypto"], "cryptography"),
]


def to_tool(d):
    return {"title": d["title"], "description": d["description"], "install": list(d["install"]),
            "run": list(d["run"]), "uninstall": [], "url": d["url"], "tags": list(d["tags"]),
            "os": ["linux"], "archived": False, "archived_reason": "", "requires_root": False,
            "installable": True, "runnable": True, "subgroup": "", "flagship": True}


def main() -> None:
    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    cats = {c["id"]: c for c in data["categories"]}
    loc = {}
    for cid, c in cats.items():
        for i, t in enumerate(c.get("tools", [])):
            loc.setdefault(norm(t.get("title", "")), (cid, i))

    added = upgraded = 0
    added_names = []
    for d in TOOLS:
        cid = d["_cat"]
        if cid not in cats:
            print("  ! unknown category", cid)
            continue
        new = to_tool(d)
        k = norm(new["title"])
        if k in loc:
            lc, idx = loc[k]
            cats[lc]["tools"][idx].update({
                "description": new["description"], "install": new["install"], "run": new["run"],
                "url": new["url"] or cats[lc]["tools"][idx].get("url", ""),
                "tags": sorted(set(cats[lc]["tools"][idx].get("tags", [])) | set(new["tags"])),
                "os": ["linux"], "installable": True, "runnable": True, "archived": False, "flagship": True,
            })
            upgraded += 1
        else:
            cats[cid].setdefault("tools", []).append(new)
            loc[k] = (cid, len(cats[cid]["tools"]) - 1)
            added += 1
            added_names.append(new["title"])

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wave 5 — upgraded: {upgraded} | added: {added} | total: {total}")
    if added_names:
        print("Newly added:", ", ".join(added_names))


if __name__ == "__main__":
    main()

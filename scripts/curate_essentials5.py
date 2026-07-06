#!/usr/bin/env python3
"""Sixth curation wave — utilities often missing from scrapes, Kali-ready.
Upgrade-in-place if present, add if missing. Run: python scripts/curate_essentials5.py
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
    # ProjectDiscovery utilities
    T("interactsh-client", "Out-of-band interaction gathering (OOB/SSRF/blind) client.", ["go install github.com/projectdiscovery/interactsh/cmd/interactsh-client@latest"], ["interactsh-client -h"], "https://github.com/projectdiscovery/interactsh", ["recon", "web"], "information_gathering"),
    T("notify", "Stream tool output to Slack/Discord/Telegram/webhooks.", ["go install github.com/projectdiscovery/notify/cmd/notify@latest"], ["notify -h"], "https://github.com/projectdiscovery/notify", ["recon"], "information_gathering"),
    T("mapcidr", "Perform multiple operations on CIDR/IP ranges.", ["go install github.com/projectdiscovery/mapcidr/cmd/mapcidr@latest"], ["mapcidr -h"], "https://github.com/projectdiscovery/mapcidr", ["recon"], "information_gathering"),
    T("tlsx", "Fast, versatile TLS data-gathering and analysis tool.", ["go install github.com/projectdiscovery/tlsx/cmd/tlsx@latest"], ["tlsx -h"], "https://github.com/projectdiscovery/tlsx", ["recon"], "information_gathering"),
    T("cdncheck", "Detect whether a host is behind a CDN/WAF/cloud provider.", ["go install github.com/projectdiscovery/cdncheck/cmd/cdncheck@latest"], ["cdncheck -h"], "https://github.com/projectdiscovery/cdncheck", ["recon"], "information_gathering"),
    T("uncover", "Discover exposed hosts via Shodan/Censys/Fofa search engines.", ["go install github.com/projectdiscovery/uncover/cmd/uncover@latest"], ["uncover -h"], "https://github.com/projectdiscovery/uncover", ["recon", "osint"], "osint"),
    T("proxify", "Swiss-army-knife HTTP/HTTPS proxy for capturing traffic.", ["go install github.com/projectdiscovery/proxify/cmd/proxify@latest"], ["proxify -h"], "https://github.com/projectdiscovery/proxify", ["web", "network"], "network_sniffing"),
    T("chaos-client", "Query ProjectDiscovery's Chaos subdomain dataset.", ["go install github.com/projectdiscovery/chaos-client/cmd/chaos@latest"], ["chaos -h"], "https://github.com/projectdiscovery/chaos-client", ["recon"], "information_gathering"),
    T("subjs", "Fetch JavaScript file URLs from a list of hosts.", ["go install github.com/lc/subjs@latest"], ["subjs -h"], "https://github.com/lc/subjs", ["recon", "web"], "information_gathering"),
    T("gauplus", "Fetch known URLs (improved gau) from web archives.", ["go install github.com/bp0lr/gauplus@latest"], ["gauplus -h"], "https://github.com/bp0lr/gauplus", ["recon", "web"], "information_gathering"),
    # 403 / bypass / web
    T("byp4xx", "Bypass 40x HTTP responses (verbs, headers, paths, case).", ["git clone https://github.com/lobuhi/byp4xx"], ["python3 byp4xx/byp4xx.py -h"], "https://github.com/lobuhi/byp4xx", ["web"], "web_attack"),
    T("nomore403", "Automate the exploitation of 403 forbidden bypass techniques.", ["go install github.com/devploit/nomore403@latest"], ["nomore403 -h"], "https://github.com/devploit/nomore403", ["web"], "web_attack"),
    T("Corsy", "CORS misconfiguration scanner.", ["git clone https://github.com/s0md3v/Corsy"], ["python3 Corsy/corsy.py -h"], "https://github.com/s0md3v/Corsy", ["web"], "web_attack"),
    T("smuggler", "HTTP request smuggling / desync detection tool.", ["git clone https://github.com/defparam/smuggler"], ["python3 smuggler/smuggler.py -h"], "https://github.com/defparam/smuggler", ["web"], "web_attack"),
    T("Bypass-403", "Bypass 403/401 access controls with header/path tricks.", ["git clone https://github.com/iamj0ker/bypass-403"], ["bash bypass-403/bypass-403.sh"], "https://github.com/iamj0ker/bypass-403", ["web"], "web_attack"),
    # AD python tooling
    T("krbrelayx", "Kerberos relaying and unconstrained-delegation abuse toolkit.", ["git clone https://github.com/dirkjanm/krbrelayx"], ["python3 krbrelayx/krbrelayx.py -h"], "https://github.com/dirkjanm/krbrelayx", ["active-directory"], "active_directory"),
    T("gMSADumper", "Dump gMSA passwords from Active Directory.", ["git clone https://github.com/micahvandeusen/gMSADumper"], ["python3 gMSADumper/gMSADumper.py -h"], "https://github.com/micahvandeusen/gMSADumper", ["active-directory"], "active_directory"),
    T("targetedKerberoast", "Kerberoast without SPNs by editing accounts you control.", ["git clone https://github.com/ShutdownRepo/targetedKerberoast"], ["python3 targetedKerberoast/targetedKerberoast.py -h"], "https://github.com/ShutdownRepo/targetedKerberoast", ["active-directory"], "active_directory"),
    T("pywerview", "Python port of PowerView for AD reconnaissance.", ["pipx install pywerview"], ["pywerview -h"], "https://github.com/the-useless-one/pywerview", ["active-directory"], "active_directory"),
    T("adPEAS", "Automated Active Directory enumeration (PEAS for AD).", ["git clone https://github.com/61106960/adPEAS"], ["echo 'Import adPEAS.ps1 in PowerShell on the target'"], "https://github.com/61106960/adPEAS", ["active-directory", "privesc"], "active_directory"),
    # privesc
    T("BeRoot", "Post-exploitation tool to check common local privesc paths.", ["git clone https://github.com/AlessandroZ/BeRoot"], ["python3 BeRoot/Linux/beroot.py"], "https://github.com/AlessandroZ/BeRoot", ["privesc"], "privilege_escalation"),
    T("LinEnum", "Scripted local Linux enumeration and privesc checks.", ["git clone https://github.com/rebootuser/LinEnum"], ["bash LinEnum/LinEnum.sh -h"], "https://github.com/rebootuser/LinEnum", ["privesc"], "privilege_escalation"),
    T("GTFOBins-cli", "Look up GTFOBins entries from the command line.", ["pipx install gtfobins || pipx install gtfolookup"], ["gtfoblookup -h"], "https://gtfobins.github.io", ["privesc"], "privilege_escalation"),
    # RE / pwn
    T("pwninit", "Automate starting a binary exploit challenge (libc, loader, template).", ["cargo install pwninit"], ["pwninit --help"], "https://github.com/io12/pwninit", ["pwn", "reversing"], "binary_exploitation"),
    T("peda", "Python Exploit Development Assistance for GDB.", ["git clone https://github.com/longld/peda ~/peda && echo 'source ~/peda/peda.py' >> ~/.gdbinit"], ["gdb"], "https://github.com/longld/peda", ["pwn", "reversing"], "binary_exploitation"),
    T("r2ghidra", "Ghidra decompiler as a radare2/rizin plugin.", ["sudo apt install -y rizin-plugins || r2pm -ci r2ghidra"], ["echo 'In radare2/rizin: pdg'"], "https://github.com/rizinorg/r2ghidra", ["reversing"], "reverse_engineering"),
    # crypto
    T("haiti", "Hash-type identifier (CLI) with hashcat/john modes.", ["sudo gem install haiti-hash"], ["haiti -h"], "https://github.com/noraj/haiti", ["crypto", "credentials"], "cryptography"),
    # wordlists / misc
    T("SecLists", "The security tester's companion — huge collection of wordlists.", ["sudo apt install -y seclists"], ["ls /usr/share/seclists"], "https://github.com/danielmiessler/SecLists", ["wordlist"], "wordlist_generator"),
    T("Interlace", "Turn single-threaded tools into fast multi-threaded scans.", ["pipx install interlace || git clone https://github.com/codingo/Interlace"], ["interlace -h"], "https://github.com/codingo/Interlace", ["recon"], "other_tools"),
    T("proxychains-ng", "Force any TCP program through a proxy chain (Tor/SOCKS).", ["sudo apt install -y proxychains4"], ["proxychains4 -h"], "https://github.com/rofl0r/proxychains-ng", ["network"], "anonymously_hiding"),
    T("macchanger", "View and manipulate the MAC address of network interfaces.", ["sudo apt install -y macchanger"], ["macchanger -h"], "https://github.com/alobbs/macchanger", ["network"], "anonymously_hiding"),
    T("nipe", "Route all traffic through the Tor network for anonymity.", ["git clone https://github.com/htrgouvea/nipe"], ["perl nipe/nipe.pl"], "https://github.com/htrgouvea/nipe", ["network"], "anonymously_hiding"),
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
            print("  ! unknown category", cid); continue
        new = to_tool(d)
        k = norm(new["title"])
        if k in loc:
            lc, idx = loc[k]
            cats[lc]["tools"][idx].update({
                "description": new["description"], "install": new["install"], "run": new["run"],
                "url": new["url"] or cats[lc]["tools"][idx].get("url", ""),
                "tags": sorted(set(cats[lc]["tools"][idx].get("tags", [])) | set(new["tags"])),
                "os": ["linux"], "installable": True, "runnable": True, "archived": False, "flagship": True})
            upgraded += 1
        else:
            cats[cid].setdefault("tools", []).append(new)
            loc[k] = (cid, len(cats[cid]["tools"]) - 1)
            added += 1; added_names.append(new["title"])

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wave 6 — upgraded: {upgraded} | added: {added} | total: {total}")
    if added_names:
        print("Newly added:", ", ".join(added_names))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fill the thinner categories with well-known real tools (Kali-ready).
Upgrade-in-place if present, add if missing. Run: python scripts/curate_thin.py
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
    # AI / ML security
    T("PyRIT", "Python Risk Identification Tool for generative AI (Microsoft).", ["pipx install pyrit"], ["python3 -c 'import pyrit'"], "https://github.com/Azure/PyRIT", ["ai"], "ai_ml_security"),
    T("Counterfit", "Automation tool for security-testing AI systems (Azure).", ["git clone https://github.com/Azure/counterfit && pipx install ./counterfit"], ["counterfit -h"], "https://github.com/Azure/counterfit", ["ai"], "ai_ml_security"),
    T("Adversarial Robustness Toolbox", "Library for ML security: evasion, poisoning, extraction defenses.", ["pipx install adversarial-robustness-toolbox"], ["python3 -c 'import art'"], "https://github.com/Trusted-AI/adversarial-robustness-toolbox", ["ai"], "ai_ml_security"),
    T("Foolbox", "Create adversarial examples to fool machine-learning models.", ["pipx install foolbox"], ["python3 -c 'import foolbox'"], "https://github.com/bethgelab/foolbox", ["ai"], "ai_ml_security"),
    T("TextAttack", "Adversarial attacks and data augmentation for NLP models.", ["pipx install textattack"], ["textattack --help"], "https://github.com/QData/TextAttack", ["ai"], "ai_ml_security"),
    T("Giskard", "Open-source testing framework for ML models and LLMs.", ["pipx install giskard"], ["python3 -c 'import giskard'"], "https://github.com/Giskard-AI/giskard", ["ai"], "ai_ml_security"),
    T("LLM Guard", "Security toolkit for LLM interactions (prompt-injection, PII, toxicity).", ["pipx install llm-guard"], ["python3 -c 'import llm_guard'"], "https://github.com/protectai/llm-guard", ["ai"], "ai_ml_security"),
    T("promptmap", "Automatically test prompt-injection attacks on LLM apps.", ["git clone https://github.com/utkusen/promptmap"], ["python3 promptmap/promptmap.py -h"], "https://github.com/utkusen/promptmap", ["ai"], "ai_ml_security"),
    # ICS / SCADA / OT
    T("Conpot", "Low-interactive ICS/SCADA honeypot.", ["pipx install conpot"], ["conpot --help"], "https://github.com/mushorg/conpot", ["ics"], "ics_scada"),
    T("plcscan", "Scan for PLC devices over s7comm/modbus.", ["git clone https://github.com/meeas/plcscan"], ["python2 plcscan/plcscan.py -h"], "https://github.com/meeas/plcscan", ["ics"], "ics_scada"),
    T("pymodbus", "Full Modbus protocol implementation with a console client.", ["pipx install 'pymodbus[repl]'"], ["pymodbus.console -h"], "https://github.com/pymodbus-dev/pymodbus", ["ics"], "ics_scada"),
    T("ISF", "Industrial Control System Exploitation Framework.", ["git clone https://github.com/dark-lbp/isf"], ["python2 isf/isf.py"], "https://github.com/dark-lbp/isf", ["ics", "exploit"], "ics_scada"),
    T("s7scan", "Scan and enumerate Siemens S7 PLCs on a network.", ["git clone https://github.com/klsecservices/s7scan"], ["python3 s7scan/s7scan.py -h"], "https://github.com/klsecservices/s7scan", ["ics"], "ics_scada"),
    T("OpenPLC", "Open-source programmable logic controller for ICS labs.", ["git clone https://github.com/thiagoralves/OpenPLC_v3"], ["bash OpenPLC_v3/install.sh"], "https://github.com/thiagoralves/OpenPLC_v3", ["ics"], "ics_scada"),
    # Satellite / GNSS / Space
    T("GNSS-SDR", "Open-source GNSS software-defined receiver.", ["sudo apt install -y gnss-sdr"], ["gnss-sdr --help"], "https://github.com/gnss-sdr/gnss-sdr", ["wireless"], "satellite"),
    T("gr-gsm", "GNU Radio blocks to receive GSM/telecom signals.", ["sudo apt install -y gr-gsm"], ["grgsm_livemon --help"], "https://github.com/ptrkrysik/gr-gsm", ["wireless"], "satellite"),
    T("gpredict", "Real-time satellite tracking and orbit prediction.", ["sudo apt install -y gpredict"], ["gpredict"], "https://github.com/csete/gpredict", ["wireless"], "satellite"),
    T("SatDump", "Universal satellite data processing software.", ["git clone https://github.com/SatDump/SatDump"], ["satdump --help"], "https://github.com/SatDump/SatDump", ["wireless"], "satellite"),
    T("gps-sdr-sim", "Generate GPS baseband signals for SDR transmitters (labs).", ["git clone https://github.com/osqzss/gps-sdr-sim && (cd gps-sdr-sim && gcc gpssim.c -lm -O3 -o gps-sdr-sim)"], ["./gps-sdr-sim/gps-sdr-sim -h"], "https://github.com/osqzss/gps-sdr-sim", ["wireless"], "satellite"),
    # Game hacking
    T("PINCE", "Reverse-engineering and memory-manipulation tool for Linux (Cheat-Engine-like).", ["git clone https://github.com/korcankaraokcu/PINCE && bash PINCE/install.sh"], ["bash PINCE/PINCE.sh"], "https://github.com/korcankaraokcu/PINCE", ["reversing"], "game_hacking"),
    T("Il2CppDumper", "Extract metadata and dump structures from Unity IL2CPP games.", ["git clone https://github.com/Perfare/Il2CppDumper"], ["echo 'Build with dotnet; run Il2CppDumper on GameAssembly.dll + global-metadata.dat'"], "https://github.com/Perfare/Il2CppDumper", ["reversing"], "game_hacking"),
    T("BepInEx", "Unity/XNA game patcher and plugin framework used for modding/RE.", ["echo 'Download a BepInEx release and unzip it into the game folder'"], ["echo 'See https://github.com/BepInEx/BepInEx'"], "https://github.com/BepInEx/BepInEx", ["reversing"], "game_hacking"),
    # VoIP
    T("sngrep", "Terminal SIP messages flow viewer and analyser.", ["sudo apt install -y sngrep"], ["sngrep -h"], "https://github.com/irontec/sngrep", ["network"], "voip"),
    T("SIPp", "Open-source SIP traffic generator and load-testing tool.", ["sudo apt install -y sip-tester"], ["sipp -h"], "https://github.com/SIPp/sipp", ["network"], "voip"),
    T("sipsak", "SIP swiss-army knife for testing SIP applications and devices.", ["sudo apt install -y sipsak"], ["sipsak --help"], "https://github.com/nils-ohlmeier/sipsak", ["network"], "voip"),
    T("rtpbreak", "Detect, reconstruct and analyse any RTP session (VoIP eavesdropping).", ["sudo apt install -y rtpbreak"], ["rtpbreak -h"], "https://github.com/Pafcholini/rtpbreak", ["network"], "voip"),
    T("Mr.SIP", "SIP-based audit and attack tool (spoofing, DoS, enumeration).", ["git clone https://github.com/meliht/Mr.SIP"], ["python3 Mr.SIP/mr.sip.py -h"], "https://github.com/meliht/Mr.SIP", ["network"], "voip"),
    # DDoS / stress test
    T("GoldenEye", "HTTP/S layer-7 denial-of-service stress-testing tool.", ["git clone https://github.com/jseidl/GoldenEye"], ["python3 GoldenEye/goldeneye.py -h"], "https://github.com/jseidl/GoldenEye", ["ddos"], "ddos_attack"),
    T("HULK", "HTTP Unbearable Load King — web server stress tester.", ["git clone https://github.com/grafov/hulk"], ["go run hulk/hulk.go"], "https://github.com/grafov/hulk", ["ddos"], "ddos_attack"),
    T("Torshammer", "Slow-POST layer-7 DoS testing tool routed over Tor.", ["git clone https://github.com/dotfighter/torshammer"], ["python3 torshammer/torshammer.py -h"], "https://github.com/dotfighter/torshammer", ["ddos"], "ddos_attack"),
    T("UFONet", "Layer 7 DDoS toolkit abusing open redirects (botnet stress test).", ["pipx install ufonet"], ["ufonet --help"], "https://github.com/epsylon/ufonet", ["ddos"], "ddos_attack"),
    T("MHDDoS", "DDoS attack script with many layer-4/7 methods (stress testing).", ["git clone https://github.com/MatrixTM/MHDDoS && pip install -r MHDDoS/requirements.txt"], ["python3 MHDDoS/start.py help"], "https://github.com/MatrixTM/MHDDoS", ["ddos"], "ddos_attack"),
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
    names = []
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
            added += 1; names.append(new["title"])

    total = sum(len(c.get("tools", [])) for c in data["categories"])
    data.setdefault("meta", {})["tools"] = total
    CATALOG.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Thin-category wave — upgraded: {upgraded} | added: {added} | total: {total}")
    if names:
        print("Newly added:", ", ".join(names))


if __name__ == "__main__":
    main()

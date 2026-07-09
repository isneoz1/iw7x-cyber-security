# iw7x — runs on ANY device through Docker (Windows, macOS, Linux, ARM/Apple
# Silicon, Raspberry Pi, cloud). The Kali base gives real install/launch power
# regardless of the host OS. Build:  docker build -t iw7x .
# Run:    docker run -it --rm iw7x
FROM kalilinux/kali-rolling

LABEL org.opencontainers.image.title="iw7x" \
      org.opencontainers.image.description="Install and run any of 30,000+ security tools from one terminal." \
      org.opencontainers.image.source="https://github.com/isneoz1/iw7x-cyber-security" \
      org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Core toolchain the installers rely on (git/python/pipx/go), kept lean.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        git python3 python3-pip python3-venv pipx golang-go \
        ca-certificates curl sudo \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/iw7x
COPY requirements.txt ./
# PEP 668: Kali marks the system env "externally managed"; allow the override.
RUN pip3 install --no-cache-dir --break-system-packages -r requirements.txt \
 || pip3 install --no-cache-dir -r requirements.txt

COPY . /opt/iw7x

# Interactive arsenal by default; pass args (e.g. `nmap`, `--update`) to override.
ENTRYPOINT ["python3", "neoz.py"]

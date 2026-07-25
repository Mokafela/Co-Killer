import base64
import json
import os
import re
import socket
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ── config ────────────────────────────────────────────────────────────────────
CHANNEL_URL   = os.getenv("CHANNEL_URL", "")  # comma-separated subscription URLs
TCP_TIMEOUT   = 3    # seconds for the fast TCP pre-filter
KNIFE_TIMEOUT = 15   # seconds xray-knife is allowed per config
MAX_WORKERS   = 20   # parallel xray-knife workers (each spawns a process)
IP_API_BATCH  = 100  # ip-api.com free batch limit
OUTPUT_DIR    = "split"

# xray-knife binary: prefer the one next to this script, then PATH
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_KNIFE_CANDIDATES = [
    os.path.join(_SCRIPT_DIR, "knife_win", "xray-knife.exe"),  # Windows
    os.path.join(_SCRIPT_DIR, "knife_dir", "xray-knife"),      # Linux/Mac
    "xray-knife",                                               # PATH fallback
]
KNIFE_BIN = next((p for p in _KNIFE_CANDIDATES if os.path.isfile(p)), "xray-knife")
# ──────────────────────────────────────────────────────────────────────────────


# ── subscription helpers ──────────────────────────────────────────────────────

def decode_subscription(raw: str) -> list[str]:
    """Return individual config lines from a raw subscription body."""
    raw = raw.strip()
    try:
        padded = raw + "=" * ((4 - len(raw) % 4) % 4)
        decoded = base64.b64decode(padded).decode("utf-8")
        lines = [l.strip() for l in decoded.splitlines() if l.strip()]
        if any(l.startswith(("vmess://", "vless://", "trojan://", "ss://")) for l in lines):
            return lines
    except Exception:
        pass
    return [l.strip() for l in raw.splitlines() if l.strip()]


def fetch_subscription(url: str) -> list[str]:
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        r.raise_for_status()
        return decode_subscription(r.text)
    except Exception as e:
        print(f"  [WARN] Could not fetch {url}: {e}")
        return []


# ── config parsing ────────────────────────────────────────────────────────────

def parse_host_port(config: str):
    """Return (host, port) or None."""
    try:
        if config.startswith("vmess://"):
            b64 = config[8:] + "=="
            data = json.loads(base64.b64decode(b64).decode("utf-8"))
            return str(data.get("add", "")), int(data.get("port", 0))
        elif config.startswith(("vless://", "trojan://", "ss://")):
            p = urllib.parse.urlparse(config)
            return p.hostname, p.port
    except Exception:
        pass
    return None


# ── step 1: TCP alive ─────────────────────────────────────────────────────────

def tcp_alive(config: str) -> bool:
    parsed = parse_host_port(config)
    if not parsed:
        return False
    host, port = parsed
    if not host or not port:
        return False
    try:
        with socket.create_connection((host, port), timeout=TCP_TIMEOUT):
            return True
    except Exception:
        return False


# ── step 2: exit-IP via xray-knife ───────────────────────────────────────────

# Cloudflare's trace endpoint returns plain text like:
#   ip=1.2.3.4
#   ...
_IP_RE = re.compile(r"\bip=(\d{1,3}(?:\.\d{1,3}){3})\b")


def get_exit_ip(config: str) -> str | None:
    """
    Route a request through the config using xray-knife and return the
    exit IP reported by Cloudflare's cdn-cgi/trace.  Returns None on failure.
    """
    try:
        proc = subprocess.run(
            [
                KNIFE_BIN, "http",
                "-c", config,
                "-u", "https://cloudflare.com/cdn-cgi/trace",
                "-d", str(KNIFE_TIMEOUT * 1000),  # xray-knife uses ms
                "-b",   # show response body (contains ip=…)
                "--rip",
            ],
            capture_output=True,
            text=True,
            timeout=KNIFE_TIMEOUT + 5,  # hard process timeout
        )
        combined = proc.stdout + proc.stderr
        m = _IP_RE.search(combined)
        if m:
            return m.group(1)
    except Exception:
        pass
    return None


# ── step 3: country lookup via ip-api.com ────────────────────────────────────

def country_to_flag(cc: str) -> str:
    if not cc or len(cc) != 2:
        return "🏳️"
    return chr(ord(cc[0].upper()) + 127397) + chr(ord(cc[1].upper()) + 127397)


def lookup_countries_by_ip(ip_list: list[str]) -> dict[str, str]:
    """Return {ip: country_code} using ip-api.com free batch endpoint."""
    result: dict[str, str] = {}
    unique_ips = list(set(ip_list))
    for i in range(0, len(unique_ips), IP_API_BATCH):
        batch = [{"query": ip} for ip in unique_ips[i : i + IP_API_BATCH]]
        try:
            r = requests.post("http://ip-api.com/batch", json=batch, timeout=15)
            for item in r.json():
                if item.get("status") == "success":
                    result[item["query"]] = item.get("countryCode", "XX")
        except Exception as e:
            print(f"  [WARN] ip-api.com error: {e}")
    return result


# ── output ────────────────────────────────────────────────────────────────────

def write_split(by_country: dict[str, list[str]]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for cc, cfgs in by_country.items():
        b64 = base64.b64encode("\n".join(cfgs).encode()).decode()
        path = os.path.join(OUTPUT_DIR, f"sub-{cc}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(b64)
        print(f"  Wrote {len(cfgs):>4} configs → {path}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    if not CHANNEL_URL:
        print("CHANNEL_URL is not set. Export it as an env variable.")
        sys.exit(1)

    # ── 1. fetch & deduplicate ────────────────────────────────────────────────
    all_configs: list[str] = []
    for url in [u.strip() for u in CHANNEL_URL.split(",") if u.strip()]:
        print(f"Fetching: {url}")
        cfgs = fetch_subscription(url)
        print(f"  → {len(cfgs)} configs")
        all_configs.extend(cfgs)

    seen: set[str] = set()
    unique = [c for c in all_configs if not (c in seen or seen.add(c))]  # type: ignore[func-returns-value]
    print(f"\nTotal unique configs: {len(unique)}")

    # ── 2. TCP alive (fast pre-filter) ────────────────────────────────────────
    print(f"\n[1/3] TCP check  ({MAX_WORKERS * 2} workers, {TCP_TIMEOUT}s timeout)…")
    alive: list[str] = []
    total = len(unique)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS * 2) as ex:
        futures = {ex.submit(tcp_alive, c): c for c in unique}
        done = 0
        for fut in as_completed(futures):
            done += 1
            if fut.result():
                alive.append(futures[fut])
            if done % 200 == 0 or done == total:
                print(f"  {done}/{total} checked — {len(alive)} alive")

    print(f"  → {len(alive)} alive out of {total}")
    if not alive:
        print("No alive configs. Exiting.")
        return

    # ── 3. get real exit IP via xray-knife ────────────────────────────────────
    print(f"\n[2/3] Exit-IP probe  ({MAX_WORKERS} workers, {KNIFE_TIMEOUT}s each)…")
    # map: config → exit_ip (or None)
    exit_ip_map: dict[str, str | None] = {}
    total = len(alive)
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(get_exit_ip, c): c for c in alive}
        done = 0
        found = 0
        for fut in as_completed(futures):
            done += 1
            cfg = futures[fut]
            ip = fut.result()
            exit_ip_map[cfg] = ip
            if ip:
                found += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} probed — {found} exit IPs obtained")

    print(f"  → {found} exit IPs, {total - found} failed (will be marked XX)")

    # ── 4. country lookup for exit IPs ───────────────────────────────────────
    print(f"\n[3/3] Country lookup via ip-api.com…")
    all_ips = [ip for ip in exit_ip_map.values() if ip]
    ip_to_cc = lookup_countries_by_ip(all_ips)

    by_country: dict[str, list[str]] = {}
    for cfg in alive:
        ip = exit_ip_map.get(cfg)
        cc = ip_to_cc.get(ip, "XX") if ip else "XX"
        by_country.setdefault(cc, []).append(cfg)

    print("Country breakdown:")
    for cc, cfgs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        print(f"  {country_to_flag(cc)} {cc}: {len(cfgs)}")

    # ── 5. write split/ ───────────────────────────────────────────────────────
    print(f"\nWriting to ./{OUTPUT_DIR}/")
    write_split(by_country)
    print("\nDone.")


if __name__ == "__main__":
    main()

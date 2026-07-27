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
KNIFE_TIMEOUT = 30   # seconds xray-knife is allowed per config (increased from 15)
MAX_WORKERS   = 10   # parallel xray-knife workers (reduced since timeout is longer)
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

# We try two endpoints:
# 1. ipify.org - simple, just returns the IP as plain text
# 2. Cloudflare trace - returns "ip=x.x.x.x" format
_IP_RE = re.compile(r"\b(?:ip=)?(\d{1,3}(?:\.\d{1,3}){3})\b")


def get_exit_ip(config: str) -> str | None:
    """
    Route a request through the config using xray-knife and return the
    exit IP. Tries ipify.org first (simple), then Cloudflare trace as fallback.
    """
    # Try 1: ipify (returns just the IP, e.g. "1.2.3.4")
    for url in ["https://api.ipify.org", "https://cloudflare.com/cdn-cgi/trace"]:
        try:
            proc = subprocess.run(
                [
                    KNIFE_BIN, "http",
                    "-c", config,
                    "-u", url,
                    "-d", str(KNIFE_TIMEOUT * 1000),
                    "-b",
                    "--rip",
                ],
                capture_output=True,
                text=True,
                timeout=KNIFE_TIMEOUT + 5,
            )
            combined = proc.stdout + proc.stderr
            m = _IP_RE.search(combined)
            if m:
                return m.group(1)
        except Exception:
            continue
    
    # Debug first failure
    if os.getenv("DEBUG"):
        try:
            proc = subprocess.run(
                [KNIFE_BIN, "http", "-c", config, "-u", "https://api.ipify.org",
                 "-d", str(KNIFE_TIMEOUT * 1000), "-b", "--rip"],
                capture_output=True, text=True, timeout=KNIFE_TIMEOUT + 5,
            )
            print(f"[DEBUG] xray-knife failed (exit={proc.returncode}):")
            print(f"  stdout: {proc.stdout[:300]}")
            print(f"  stderr: {proc.stderr[:300]}")
        except Exception as e:
            print(f"[DEBUG] Exception: {e}")
    
    return None


def get_server_ip(config: str) -> str | None:
    """Fallback: resolve the server's host to an IP."""
    parsed = parse_host_port(config)
    if not parsed or not parsed[0]:
        return None
    host = parsed[0]
    try:
        # If already an IP, return it
        socket.inet_aton(host)
        return host
    except socket.error:
        # Resolve hostname
        try:
            return socket.gethostbyname(host)
        except Exception:
            return None


# ── step 3: country lookup via ip-api.com ────────────────────────────────────

UNKNOWN_CC   = "XX"
UNKNOWN_FLAG = "🌐"
UNKNOWN_NAME = "Unknown"


def country_to_flag(cc: str) -> str:
    if not cc or len(cc) != 2 or cc == UNKNOWN_CC:
        return UNKNOWN_FLAG
    return chr(ord(cc[0].upper()) + 127397) + chr(ord(cc[1].upper()) + 127397)


def country_flag_img(cc: str) -> str:
    """Small flag image from flagcdn.com for GitHub markdown tables."""
    if not cc or len(cc) != 2 or cc == UNKNOWN_CC:
        return ""
    return f'<img src="https://flagcdn.com/20x15/{cc.lower()}.png" alt="{cc}">'


def cc_display(cc: str) -> str:
    """Human-readable country label."""
    return UNKNOWN_NAME if cc == UNKNOWN_CC else cc


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

REPO_RAW = "https://raw.githubusercontent.com/Mokafela/Co-Killer/master/split"


def write_split(by_country: dict[str, list[str]]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Per-country files
    for cc, cfgs in by_country.items():
        b64 = base64.b64encode("\n".join(cfgs).encode()).decode()
        path = os.path.join(OUTPUT_DIR, f"sub-{cc}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(b64)
        print(f"  Wrote {len(cfgs):>4} configs → {path}")

    # Combined ALL file
    all_cfgs = [cfg for cfgs in by_country.values() for cfg in cfgs]
    b64_all = base64.b64encode("\n".join(all_cfgs).encode()).decode()
    all_path = os.path.join(OUTPUT_DIR, "sub-ALL.txt")
    with open(all_path, "w", encoding="utf-8") as f:
        f.write(b64_all)
    print(f"  Wrote {len(all_cfgs):>4} configs → {all_path}")


def _build_table(by_country: dict[str, list[str]], total: int) -> str:
    sorted_cc = sorted(by_country.items(), key=lambda x: -len(x[1]))
    all_url = f"{REPO_RAW}/sub-ALL.txt"

    lines = [
        f"> **{total} configs** across **{len(by_country)} countries** — updated every 15 minutes.",
        "",
        "### � All Configs",
        "",
        "| | | Link |",
        "| :---: | :---: | :--- |",
        f"| 🌍 | **{total}** | `{all_url}` |",
        "",
        "### 🗺️ By Country",
        "",
        "| 🏳️ | Country | Configs | Link |",
        "| :---: | :--- | :---: | :--- |",
    ]
    for cc, cfgs in sorted_cc:
        flag = country_flag_img(cc) if cc != UNKNOWN_CC else "🌐"
        name = cc_display(cc)
        url = f"{REPO_RAW}/sub-{cc}.txt"
        lines.append(f"| {flag} | {name} | **{len(cfgs)}** | `{url}` |")

    return "\n".join(lines)


def update_readme(by_country: dict[str, list[str]]) -> None:
    base = os.path.dirname(os.path.abspath(__file__))
    total = sum(len(v) for v in by_country.values())
    block = _build_table(by_country, total)

    for filename, start_tag, end_tag in [
        ("README.md",    "<!-- SUBS_START -->",    "<!-- SUBS_END -->"),
        ("README.fa.md", "<!-- SUBS_START_FA -->", "<!-- SUBS_END_FA -->"),
    ]:
        path = os.path.join(base, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except FileNotFoundError:
            print(f"  [WARN] {filename} not found, skipping.")
            continue

        updated = re.sub(
            re.escape(start_tag) + r".*?" + re.escape(end_tag),
            f"{start_tag}\n{block}\n{end_tag}",
            content,
            flags=re.DOTALL,
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(updated)
        print(f"  {filename} updated.")


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

    # ── 3. get real exit IP via xray-knife (with server IP fallback) ─────────
    print(f"\n[2/3] Exit-IP probe  ({MAX_WORKERS} workers, {KNIFE_TIMEOUT}s each)…")
    ip_map: dict[str, str | None] = {}  # config → IP (exit or server)
    total = len(alive)
    
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = {ex.submit(get_exit_ip, c): c for c in alive}
        done = 0
        exit_found = 0
        for fut in as_completed(futures):
            done += 1
            cfg = futures[fut]
            ip = fut.result()
            ip_map[cfg] = ip
            if ip:
                exit_found += 1
            if done % 50 == 0 or done == total:
                print(f"  {done}/{total} probed — {exit_found} exit IPs obtained")

    print(f"  → {exit_found} exit IPs via xray-knife")
    
    # Fallback: for configs where xray-knife failed, use server IP
    failed = [c for c, ip in ip_map.items() if not ip]
    if failed:
        print(f"  → Falling back to server IP for {len(failed)} configs...")
        for cfg in failed:
            ip_map[cfg] = get_server_ip(cfg)
        server_found = sum(1 for ip in ip_map.values() if ip)
        print(f"  → {server_found - exit_found} server IPs resolved")

    # ── 4. country lookup for all IPs ────────────────────────────────────────
    print(f"\n[3/3] Country lookup via ip-api.com…")
    all_ips = [ip for ip in ip_map.values() if ip]
    ip_to_cc = lookup_countries_by_ip(all_ips)

    by_country: dict[str, list[str]] = {}
    for cfg in alive:
        ip = ip_map.get(cfg)
        cc = ip_to_cc.get(ip, UNKNOWN_CC) if ip else UNKNOWN_CC
        by_country.setdefault(cc, []).append(cfg)

    print("Country breakdown:")
    for cc, cfgs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        print(f"  {country_to_flag(cc)} {cc}: {len(cfgs)}")

    # ── 5. write split/ and update README ────────────────────────────────────
    print(f"\nWriting to ./{OUTPUT_DIR}/")
    write_split(by_country)
    print("\nUpdating README…")
    update_readme(by_country)
    print("\nDone.")


if __name__ == "__main__":
    main()

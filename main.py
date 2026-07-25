import base64
import json
import os
import re
import socket
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ── config ────────────────────────────────────────────────────────────────────
CHANNEL_URL  = os.getenv("CHANNEL_URL", "")   # comma-separated subscription URLs
TIMEOUT      = 3    # TCP connect timeout (seconds)
MAX_WORKERS  = 50   # parallel TCP checkers
IP_API_BATCH = 100  # ip-api.com max batch size
OUTPUT_DIR   = "split"
# ──────────────────────────────────────────────────────────────────────────────


# ── helpers ───────────────────────────────────────────────────────────────────

def decode_subscription(raw: str) -> list[str]:
    """Return individual config lines from a raw subscription body."""
    raw = raw.strip()
    # Try base64 first
    try:
        padded = raw + "=" * ((4 - len(raw) % 4) % 4)
        decoded = base64.b64decode(padded).decode("utf-8")
        lines = [l.strip() for l in decoded.splitlines() if l.strip()]
        if any(l.startswith(("vmess://", "vless://", "trojan://", "ss://")) for l in lines):
            return lines
    except Exception:
        pass
    # Plain text
    return [l.strip() for l in raw.splitlines() if l.strip()]


def fetch_subscription(url: str) -> list[str]:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        return decode_subscription(r.text)
    except Exception as e:
        print(f"  [WARN] Could not fetch {url}: {e}")
        return []


def parse_host_port(config: str):
    """Return (host, port) tuple or None."""
    try:
        if config.startswith("vmess://"):
            b64 = config[8:]
            b64 += "=" * ((4 - len(b64) % 4) % 4)
            data = json.loads(base64.b64decode(b64).decode("utf-8"))
            return str(data.get("add", "")), int(data.get("port", 0))
        elif config.startswith(("vless://", "trojan://", "ss://")):
            p = urllib.parse.urlparse(config)
            return p.hostname, p.port
    except Exception:
        pass
    return None


def tcp_alive(config: str) -> bool:
    """Return True if the config's host:port accepts a TCP connection."""
    parsed = parse_host_port(config)
    if not parsed:
        return False
    host, port = parsed
    if not host or not port:
        return False
    try:
        with socket.create_connection((host, port), timeout=TIMEOUT):
            return True
    except Exception:
        return False


def country_to_flag(cc: str) -> str:
    if not cc or len(cc) != 2:
        return "🏳️"
    return chr(ord(cc[0].upper()) + 127397) + chr(ord(cc[1].upper()) + 127397)


def lookup_countries(configs: list[str]) -> dict[str, str]:
    """
    Returns {config: country_code} for every config whose host resolves.
    Uses ip-api.com free batch endpoint (no key required, 45 req/min).
    """
    host_map: dict[str, str] = {}   # config → host
    for cfg in configs:
        parsed = parse_host_port(cfg)
        if parsed and parsed[0]:
            host_map[cfg] = parsed[0]

    # Resolve hostnames to IPs for the API (it accepts hostnames too, but
    # explicit IPs are faster and avoid double-resolution on their side).
    queries = [{"query": host} for host in host_map.values()]
    ip_to_cc: dict[str, str] = {}

    for i in range(0, len(queries), IP_API_BATCH):
        batch = queries[i : i + IP_API_BATCH]
        try:
            r = requests.post("http://ip-api.com/batch", json=batch, timeout=15)
            for item in r.json():
                if item.get("status") == "success":
                    ip_to_cc[item["query"]] = item.get("countryCode", "XX")
        except Exception as e:
            print(f"  [WARN] ip-api.com batch error: {e}")

    return {cfg: ip_to_cc.get(host, "XX") for cfg, host in host_map.items()}


def write_split(by_country: dict[str, list[str]]) -> None:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for cc, cfgs in by_country.items():
        content = "\n".join(cfgs)
        b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
        path = os.path.join(OUTPUT_DIR, f"sub-{cc}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(b64)
        print(f"  Wrote {len(cfgs):>4} configs → {path}")

# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    # ── 1. collect configs ────────────────────────────────────────────────────
    if not CHANNEL_URL:
        print("CHANNEL_URL is not set. Export it as an env variable.")
        return

    urls = [u.strip() for u in CHANNEL_URL.split(",") if u.strip()]
    all_configs: list[str] = []
    for url in urls:
        print(f"Fetching: {url}")
        configs = fetch_subscription(url)
        print(f"  → {len(configs)} configs extracted")
        all_configs.extend(configs)

    # deduplicate while preserving order
    seen: set[str] = set()
    unique: list[str] = []
    for c in all_configs:
        if c not in seen:
            seen.add(c)
            unique.append(c)

    print(f"\nTotal unique configs: {len(unique)}")

    # ── 2. TCP alive check ────────────────────────────────────────────────────
    print(f"\nChecking TCP connectivity ({MAX_WORKERS} workers, timeout={TIMEOUT}s)…")
    alive: list[str] = []
    total = len(unique)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        future_to_cfg = {ex.submit(tcp_alive, cfg): cfg for cfg in unique}
        done = 0
        for future in as_completed(future_to_cfg):
            done += 1
            cfg = future_to_cfg[future]
            if future.result():
                alive.append(cfg)
            if done % 100 == 0 or done == total:
                print(f"  {done}/{total} tested — {len(alive)} alive so far")

    print(f"\nAlive: {len(alive)} / {total}")

    if not alive:
        print("No alive configs found. Exiting.")
        return

    # ── 3. country lookup ─────────────────────────────────────────────────────
    print(f"\nLooking up countries via ip-api.com…")
    cc_map = lookup_countries(alive)   # config → country_code

    # group by country
    by_country: dict[str, list[str]] = {}
    for cfg in alive:
        cc = cc_map.get(cfg, "XX")
        by_country.setdefault(cc, []).append(cfg)

    print("Country breakdown:")
    for cc, cfgs in sorted(by_country.items(), key=lambda x: -len(x[1])):
        print(f"  {country_to_flag(cc)} {cc}: {len(cfgs)}")

    # ── 4. write split/ files ─────────────────────────────────────────────────
    print(f"\nWriting split files to ./{OUTPUT_DIR}/")
    write_split(by_country)
    print("\nDone.")


if __name__ == "__main__":
    main()

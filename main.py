import requests
from bs4 import BeautifulSoup
import base64
import json
import urllib.parse
import socket
import re
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

CHANNEL_URL = os.getenv("CHANNEL_URL", "")
TIMEOUT = 3  # seconds for TCP ping
MAX_WORKERS = 20

def get_channel_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching channel: {e}")
        return None

def extract_configs(html):
    soup = BeautifulSoup(html, 'html.parser')
    configs = []
    
    text = soup.get_text()
    search_text = text
    
    # Attempt Base64 decode for sub links
    try:
        clean_text = text.strip()
        clean_text += "=" * ((4 - len(clean_text) % 4) % 4)
        decoded = base64.b64decode(clean_text).decode('utf-8')
        if 'vmess://' in decoded or 'vless://' in decoded:
            search_text += "\n" + decoded
    except Exception:
        pass
    
    # Regex to match vmess, vless, trojan, ss URLs
    pattern = re.compile(r'(vmess://[a-zA-Z0-9+/=]+)|((?:vless|trojan|ss)://[^\s<"\'>]+)')
    matches = pattern.findall(search_text)
    
    for match in matches:
        if match[0]:
            configs.append(match[0])
        elif match[1]:
            configs.append(match[1])
            
    # Remove duplicates
    return list(set(configs))

def parse_config(config):
    """Parses a config and returns (host, port) if possible, else None."""
    try:
        if config.startswith('vmess://'):
            b64_data = config[8:]
            # pad if needed
            b64_data += "=" * ((4 - len(b64_data) % 4) % 4)
            json_data = base64.b64decode(b64_data).decode('utf-8')
            data = json.loads(json_data)
            return data.get('add'), int(data.get('port', 0))
        
        elif config.startswith(('vless://', 'trojan://', 'ss://')):
            # Format: protocol://uuid@host:port?query#name
            parsed = urllib.parse.urlparse(config)
            return parsed.hostname, parsed.port
    except Exception as e:
        # Silently fail on invalid parse
        pass
    return None

def rename_config(config, name):
    """Renames a config's alias/remark to the given name."""
    try:
        if config.startswith('vmess://'):
            b64_data = config[8:]
            b64_data += "=" * ((4 - len(b64_data) % 4) % 4)
            json_data = base64.b64decode(b64_data).decode('utf-8')
            data = json.loads(json_data)
            data['ps'] = name
            new_json_data = json.dumps(data)
            new_b64 = base64.b64encode(new_json_data.encode('utf-8')).decode('utf-8')
            return f"vmess://{new_b64}"
            
        elif config.startswith(('vless://', 'trojan://', 'ss://')):
            parsed = urllib.parse.urlparse(config)
            new_parsed = parsed._replace(fragment=urllib.parse.quote(name))
            return urllib.parse.urlunparse(new_parsed)
    except Exception:
        pass
    return config

def test_config(config):
    """Tests if a config's IP/port is reachable. Returns config if true, else None."""
    parsed = parse_config(config)
    if not parsed:
        return None
        
    host, port = parsed
    if not host or not port:
        return None
        
    tcp_pass = False
    try:
        # Basic TCP Ping
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            tcp_pass = True
    except Exception:
        pass
    
    if not tcp_pass:
        return None

    # Google 403 test using xray-knife
    try:
        proc = subprocess.run(
            ["xray-knife", "http", "-c", config, "-u", "https://www.google.com", "-d", "10000"],
            capture_output=True,
            text=True,
            timeout=15
        )
        out_lower = proc.stdout.lower() + proc.stderr.lower()
        if ("delay" in out_lower or "valid" in out_lower or "✅" in out_lower) and "❌" not in out_lower and "failed" not in out_lower:
            return config, True
        else:
            print(f"HTTP Failed | RC: {proc.returncode} | OUT: {proc.stdout.strip()} | ERR: {proc.stderr.strip()}")
    except Exception as e:
        print(f"HTTP Exception: {e}")

    return config, False

def main():
    channel_env = os.getenv("CHANNEL_URL", "")
    if not channel_env:
        print("CHANNEL_URL environment variable is missing.")
        return

    urls = [url.strip() for url in channel_env.split(",") if url.strip()]
    all_configs = []
    
    for url in urls:
        print(f"Fetching configs from channel...")
        html = get_channel_html(url)
        if html:
            extracted = extract_configs(html)
            print(f"Extracted {len(extracted)} from this channel.")
            all_configs.extend(extracted)
            
    # Remove duplicates across all channels
    configs = list(set(all_configs))
    total = len(configs)
    print(f"Total unique configs extracted: {total}. Testing them now...")
    
    working_configs = []
    passed_configs = set()
    
    # Initialize xray-knife DB in single thread to prevent race condition
    try:
        subprocess.run(["xray-knife", "http", "-c", "vless://00000000-0000-0000-0000-000000000000@1.1.1.1:8080?encryption=none&security=none&type=tcp#dummy"], capture_output=True, timeout=5)
    except Exception:
        pass

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        for i, res in enumerate(executor.map(test_config, configs), 1):
            if i % 10 == 0 or i == total:
                print(f"Progress: Tested {i}/{total} configs...")
            if res:
                cfg, http_pass = res
                working_configs.append(cfg)
                if http_pass:
                    passed_configs.add(cfg)
                
    print(f"Found {len(working_configs)} working configs ({len(passed_configs)} passed HTTP test).")
    
    # Limit to 60 configs
    working_configs = working_configs[:60]
    
    # Add dummy config for repo name
    dummy_config = "vless://00000000-0000-0000-0000-000000000000@1.1.1.1:8080?encryption=none&security=none&type=tcp#" + urllib.parse.quote("Mokafela/Co-Killer")
    renamed_configs = [dummy_config]
    
    # Get country flags via IP-API batch endpoint
    def country_to_flag(code):
        if not code or len(code) != 2: return "🏳️"
        return chr(ord(code[0].upper()) + 127397) + chr(ord(code[1].upper()) + 127397)
        
    queries = []
    host_to_cfg = {}
    for cfg in working_configs:
        parsed = parse_config(cfg)
        if parsed and parsed[0]:
            queries.append({"query": parsed[0]})
            host_to_cfg[cfg] = parsed[0]
            
    flag_map = {}
    if queries:
        try:
            res = requests.post("http://ip-api.com/batch", json=queries, timeout=10)
            for item in res.json():
                if item.get("status") == "success":
                    flag_map[item["query"]] = country_to_flag(item.get("countryCode", ""))
        except Exception as e:
            print(f"Error fetching IP data: {e}")

    for i, cfg in enumerate(working_configs, 1):
        host = host_to_cfg.get(cfg, "")
        flag = flag_map.get(host, "🏳️")
        pass_tag = " [PASS]" if cfg in passed_configs else ""
        renamed = rename_config(cfg, f"{flag} Mokafela#{i}{pass_tag}")
        renamed_configs.append(renamed)
    
    if len(renamed_configs) > 1: # More than just the dummy config
        sub_content = "\n".join(renamed_configs)
        b64_sub = base64.b64encode(sub_content.encode('utf-8')).decode('utf-8')
        
        with open('sub.txt', 'w', encoding='utf-8') as f:
            f.write(b64_sub)
        print("Subscription saved to sub.txt")
    else:
        print("No working configs found.")

if __name__ == "__main__":
    main()

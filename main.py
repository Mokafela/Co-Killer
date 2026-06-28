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
    parsed = parse_config(config)
    if not parsed:
        return config, False, 0.0
        
    host, port = parsed
    if not host or not port:
        return config, False, 0.0
        
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
        return config, False, 0.0

    # Google 403 test using xray-knife
    try:
        proc = subprocess.run(
            ["xray-knife", "http", "-c", config, "-u", "https://gemini.google.com/app", "-d", "10000", "--speedtest"],
            capture_output=True,
            text=True,
            timeout=30
        )
        out_lower = proc.stdout.lower() + proc.stderr.lower()
        if ("delay" in out_lower or "valid" in out_lower or "✅" in out_lower or "speed" in out_lower) and "❌" not in out_lower and "failed" not in out_lower and "403" not in out_lower and "forbidden" not in out_lower and "region" not in out_lower:
            speed_mbps = 0.0
            match = re.search(r'speed:\s*([\d.]+)\s*(mbps|kbps|bps|mb/s|kb/s|b/s)', out_lower)
            if match:
                val = float(match.group(1))
                unit = match.group(2)
                if unit in ('mb/s', 'mbps'):
                    speed_mbps = val
                elif unit in ('kb/s', 'kbps'):
                    speed_mbps = val / 1024.0
                elif unit in ('b/s', 'bps'):
                    speed_mbps = val / (1024.0 * 1024.0)
            return config, True, speed_mbps
    except Exception as e:
        pass

    return config, False, 0.0

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
                print(f"Progress: Tested {i}/{total} configs (Remaining: {total - i})...")
            if res:
                if len(res) == 3:
                    cfg, http_pass, speed = res
                else:
                    cfg, http_pass = res
                    speed = 0.0
                if http_pass:
                    working_configs.append((cfg, speed))
                    passed_configs.add(cfg)
                
    print(f"Found {len(working_configs)} working configs ({len(passed_configs)} passed HTTP test).")
    
    # Sort by speed descending
    working_configs.sort(key=lambda x: x[1], reverse=True)
    
    # Limit to 60 configs removed
    
    # Add dummy config for repo name
    dummy_config = "vless://00000000-0000-0000-0000-000000000000@1.1.1.1:8080?encryption=none&security=none&type=tcp#" + urllib.parse.quote("Mokafela/Co-Killer")
    renamed_configs = [dummy_config]
    
    # Get country flags via IP-API batch endpoint
    def country_to_flag(code):
        if not code or len(code) != 2: return "🏳️"
        return chr(ord(code[0].upper()) + 127397) + chr(ord(code[1].upper()) + 127397)
        
    queries = []
    host_to_cfg = {}
    for cfg, speed in working_configs:
        parsed = parse_config(cfg)
        if parsed and parsed[0]:
            queries.append({"query": parsed[0]})
            host_to_cfg[cfg] = parsed[0]
            
    flag_map = {}
    country_map = {}
    if queries:
        try:
            for i in range(0, len(queries), 100):
                batch = queries[i:i+100]
                res = requests.post("http://ip-api.com/batch", json=batch, timeout=10)
                for item in res.json():
                    if item.get("status") == "success":
                        cc = item.get("countryCode", "")
                        if cc:
                            flag_map[item["query"]] = country_to_flag(cc)
                            country_map[item["query"]] = cc
        except Exception as e:
            print(f"Error fetching IP data: {e}")

    configs_by_country = {}
    all_renamed = [dummy_config]
    passed_renamed = [dummy_config]

    for i, (cfg, speed) in enumerate(working_configs, 1):
        host = host_to_cfg.get(cfg, "")
        flag = flag_map.get(host, "🏳️")
        cc = country_map.get(host, "Unknown")
        speed_tag = f" {speed:.2f}MB/s" if speed > 0 else ""
        pass_tag = " [PASS]" if cfg in passed_configs else ""
        renamed = rename_config(cfg, f"{flag} Mokafela#{i}{speed_tag}{pass_tag}")
        all_renamed.append(renamed)
        
        if cfg in passed_configs:
            passed_renamed.append(renamed)
        
        if cc not in configs_by_country:
            configs_by_country[cc] = [dummy_config]
        configs_by_country[cc].append(renamed)
    
    os.makedirs("subs", exist_ok=True)
    
    if len(all_renamed) > 1: # More than just the dummy config
        sub_content = "\n".join(all_renamed)
        b64_sub = base64.b64encode(sub_content.encode('utf-8')).decode('utf-8')
        
        with open('subs/sub.txt', 'w', encoding='utf-8') as f:
            f.write(b64_sub)
        print("Subscription saved to subs/sub.txt")

        # Write 403-passed sub
        passed_count = 0
        if len(passed_renamed) > 1:
            passed_count = len(passed_renamed) - 1
            passed_content = "\n".join(passed_renamed)
            b64_passed = base64.b64encode(passed_content.encode('utf-8')).decode('utf-8')
            with open('subs/sub-403.txt', 'w', encoding='utf-8') as f:
                f.write(b64_passed)
            print("Subscription saved to subs/sub-403.txt")

        # Write country subs
        country_counts = {}
        for cc, cfgs in configs_by_country.items():
            if len(cfgs) > 1:
                cc_count = len(cfgs) - 1
                country_counts[cc] = cc_count
                cc_content = "\n".join(cfgs)
                b64_cc = base64.b64encode(cc_content.encode('utf-8')).decode('utf-8')
                with open(f'subs/sub-{cc}.txt', 'w', encoding='utf-8') as f:
                    f.write(b64_cc)
                print(f"Subscription saved to subs/sub-{cc}.txt")

        # Update README
        base_url = "https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs"
        md = [
            "Copy the link below and import it into your V2Ray client (like v2rayNG, Shadowrocket, or NekoBox).",
            "",
            "### 🌍 All Configs",
            f"Contains **{len(all_renamed)-1}** configurations.",
            "```text",
            f"{base_url}/sub.txt",
            "```",
            "",
            "### ✅ 403 Passed Configs",
            f"Contains **{passed_count}** configurations.",
            "```text",
            f"{base_url}/sub-403.txt",
            "```",
            "",
            "### 🏳️ Country Specific Configs",
            "| Country | Count | Subscription Link |",
            "| :--- | :---: | :--- |"
        ]
        
        sorted_cc = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
        for cc, count in sorted_cc:
            flag = country_to_flag(cc) if cc != "Unknown" else "🏳️"
            md.append(f"| {flag} {cc} | {count} | `{base_url}/sub-{cc}.txt` |")
            
        new_md_content = "\n".join(md)
        
        try:
            with open('README.md', 'r', encoding='utf-8') as f:
                readme = f.read()
            readme = re.sub(r'<!-- SUBS_START -->.*?<!-- SUBS_END -->', 
                            f'<!-- SUBS_START -->\n{new_md_content}\n<!-- SUBS_END -->', 
                            readme, flags=re.DOTALL)
            with open('README.md', 'w', encoding='utf-8') as f:
                f.write(readme)
            print("README.md updated.")
        except Exception as e:
            print(f"Error updating README.md: {e}")

        # Write JSON for frontend
        json_data = [
            {
                "name": "All Configs",
                "flag": "🌍",
                "count": len(all_renamed) - 1,
                "url": f"{base_url}/sub.txt"
            }
        ]
        if passed_count > 0:
            json_data.append({
                "name": "403 Passed Configs",
                "flag": "✅",
                "count": passed_count,
                "url": f"{base_url}/sub-403.txt"
            })
            
        for cc, count in sorted_cc:
            flag = country_to_flag(cc) if cc != "Unknown" else "🏳️"
            json_data.append({
                "name": f"{cc} Configs",
                "flag": flag,
                "count": count,
                "url": f"{base_url}/sub-{cc}.txt"
            })
            
        with open('subs/subs.json', 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=2)
        print("Generated subs/subs.json for GitHub Pages.")

    else:
        print("No working configs found.")

if __name__ == "__main__":
    main()

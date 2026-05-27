import requests
from bs4 import BeautifulSoup
import base64
import json
import urllib.parse
import socket
import re
from concurrent.futures import ThreadPoolExecutor

CHANNEL_URL = "https://t.me/s/subioir"
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
    
    # Text in telegram channel messages often has vmess:// etc.
    text = soup.get_text()
    
    # Regex to match vmess, vless, trojan, ss URLs
    pattern = re.compile(r'(vmess://[a-zA-Z0-9+/=]+)|((?:vless|trojan|ss)://[^\s<]+)')
    matches = pattern.findall(text)
    
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
        
    try:
        # Basic TCP Ping
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)
        result = sock.connect_ex((host, port))
        sock.close()
        if result == 0:
            return config
    except Exception:
        pass
    
    return None

def main():
    print(f"Fetching configs from {CHANNEL_URL}...")
    html = get_channel_html(CHANNEL_URL)
    if not html:
        print("Failed to get HTML.")
        return
        
    configs = extract_configs(html)
    print(f"Extracted {len(configs)} configs. Testing them now...")
    
    working_configs = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        results = executor.map(test_config, configs)
        for res in results:
            if res:
                working_configs.append(res)
                
    print(f"Found {len(working_configs)} working configs.")
    
    renamed_configs = []
    for i, cfg in enumerate(working_configs, 1):
        renamed = rename_config(cfg, f"Mokafela-Config-{i}")
        renamed_configs.append(renamed)
    
    if renamed_configs:
        sub_content = "\n".join(renamed_configs)
        b64_sub = base64.b64encode(sub_content.encode('utf-8')).decode('utf-8')
        
        with open('sub.txt', 'w', encoding='utf-8') as f:
            f.write(b64_sub)
        print("Subscription saved to sub.txt")
    else:
        print("No working configs found.")

if __name__ == "__main__":
    main()

<div align="center">
  <h1>Config Killer - Fast V2Ray / VLESS / Trojan / Shadowsocks Configs for Iran</h1>
  <p>Automated tool to scrape, test, and curate the fastest and most reliable V2Ray proxy configs to bypass internet censorship in Iran.</p>
</div>

## 🚀 What is Config Killer?

**Config Killer** is a high-performance Python script designed to find, validate, and sort free **V2Ray, VLESS, VMess, Trojan, and Shadowsocks** configs. It ensures you always get the best download speeds and lowest latency for a free internet.

If you are searching for **V2Ray Iran**, **VLESS Iran**, **Free VMess**, or the best proxies to bypass filtering, this tool automates the heavy lifting. It uses [xray-knife](https://github.com/entynetproject/xray-knife) to perform deep HTTP tests (bypassing 403 errors) and real-time speed tests, delivering a curated subscription link.

## ✨ Features

- 🔍 **Automated Scraping**: Pulls the latest configs from multiple Telegram channels or web sources.
- ⚡ **Speed Testing**: Automatically tests the download speed of each config.
-  مرتب **Sorting**: Sorts configs from fastest to slowest (MB/s).
- 🇮🇷 **Iran Optimized**: Tests HTTP connectivity against Google/Gemini to ensure the IP isn't blocked or showing 403 Forbidden in Iran.
- 🔄 **Auto-Deduplication**: Removes dead or duplicate links.
- 🏳️ **Country Flags**: Automatically detects the server IP and adds the correct country flag to the config name.
- 📦 **Subscription Output**: Generates a standard Base64 `sub.txt` that can be imported directly into v2rayNG, Shadowrocket, NekoBox, or NapsternetV.

## 🔗 Subscription Links

<!-- SUBS_START -->
Copy the link below and import it into your V2Ray client (like v2rayNG, Shadowrocket, or NekoBox).

### 🌍 All Configs
Contains **915** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub.txt
```

### ✅ 403 Passed Configs
Contains **915** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-403.txt
```

### 🏳️ Country Specific Configs
| Country | Count | Subscription Link |
| :--- | :---: | :--- |
| 🇨🇦 CA | 288 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CA.txt` |
| 🏳️ Unknown | 148 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-Unknown.txt` |
| 🇺🇸 US | 127 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-US.txt` |
| 🇳🇱 NL | 82 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NL.txt` |
| 🇩🇪 DE | 51 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-DE.txt` |
| 🇸🇨 SC | 37 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SC.txt` |
| 🇬🇧 GB | 27 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GB.txt` |
| 🇫🇷 FR | 27 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FR.txt` |
| 🇹🇷 TR | 17 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TR.txt` |
| 🇯🇵 JP | 12 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-JP.txt` |
| 🇭🇺 HU | 12 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HU.txt` |
| 🇮🇹 IT | 8 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IT.txt` |
| 🇷🇺 RU | 7 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RU.txt` |
| 🇱🇻 LV | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LV.txt` |
| 🇪🇸 ES | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ES.txt` |
| 🇨🇭 CH | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CH.txt` |
| 🇫🇮 FI | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FI.txt` |
| 🇱🇹 LT | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LT.txt` |
| 🇦🇹 AT | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AT.txt` |
| 🇸🇪 SE | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SE.txt` |
| 🇪🇪 EE | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-EE.txt` |
| 🇳🇿 NZ | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NZ.txt` |
| 🇦🇺 AU | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AU.txt` |
| 🇿🇦 ZA | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ZA.txt` |
| 🇰🇷 KR | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KR.txt` |
| 🇮🇳 IN | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IN.txt` |
| 🇨🇴 CO | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CO.txt` |
| 🇷🇴 RO | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RO.txt` |
| 🇸🇬 SG | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SG.txt` |
| 🇭🇰 HK | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HK.txt` |
| 🇻🇳 VN | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-VN.txt` |
| 🇮🇩 ID | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ID.txt` |
| 🇰🇿 KZ | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KZ.txt` |
| 🇲🇽 MX | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-MX.txt` |
| 🇳🇴 NO | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NO.txt` |
| 🇸🇰 SK | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SK.txt` |
| 🇨🇳 CN | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CN.txt` |
| 🇨🇿 CZ | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CZ.txt` |
| 🇦🇪 AE | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AE.txt` |
| 🇵🇰 PK | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PK.txt` |
| 🇵🇭 PH | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PH.txt` |
| 🇵🇱 PL | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PL.txt` |
| 🇮🇪 IE | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IE.txt` |
| 🇮🇷 IR | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IR.txt` |
<!-- SUBS_END -->

## 📱 Supported Clients

The generated `sub.txt` works perfectly with:
- **v2rayNG** (Android)
- **V2RayN** (Windows)
- **Shadowrocket** (iOS)
- **NekoBox / NekoRay** (PC/Android)
- **NapsternetV** (iOS/Android)
- **Sing-Box**

## 🔑 Keywords for Search Engines
`v2ray iran` `vless iran` `vmess iran` `free v2ray` `bypass filtering iran` `iran internet censorship` `shadowsocks iran` `trojan iran` `xray proxy` `v2rayng configs` `shadowrocket configs iran` `telegram v2ray proxy`

## ⚠️ Disclaimer
This tool is for educational purposes and open internet access. Please use it responsibly.

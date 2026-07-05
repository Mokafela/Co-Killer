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
Contains **1222** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub.txt
```

### ✅ 403 Passed Configs
Contains **1222** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-403.txt
```

### 🏳️ Country Specific Configs
| Country | Count | Subscription Link |
| :--- | :---: | :--- |
| 🇨🇦 CA | 353 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CA.txt` |
| 🏳️ Unknown | 249 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-Unknown.txt` |
| 🇺🇸 US | 147 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-US.txt` |
| 🇳🇱 NL | 80 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NL.txt` |
| 🇫🇷 FR | 57 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FR.txt` |
| 🇩🇪 DE | 55 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-DE.txt` |
| 🇫🇮 FI | 44 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FI.txt` |
| 🇸🇨 SC | 33 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SC.txt` |
| 🇬🇧 GB | 25 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GB.txt` |
| 🇪🇸 ES | 23 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ES.txt` |
| 🇧🇿 BZ | 17 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BZ.txt` |
| 🇱🇹 LT | 16 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LT.txt` |
| 🇸🇬 SG | 14 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SG.txt` |
| 🇷🇺 RU | 14 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RU.txt` |
| 🇯🇵 JP | 11 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-JP.txt` |
| 🇮🇩 ID | 10 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ID.txt` |
| 🇹🇷 TR | 8 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TR.txt` |
| 🇨🇭 CH | 6 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CH.txt` |
| 🇮🇹 IT | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IT.txt` |
| 🇸🇪 SE | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SE.txt` |
| 🇱🇻 LV | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LV.txt` |
| 🇰🇷 KR | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KR.txt` |
| 🇿🇦 ZA | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ZA.txt` |
| 🇭🇺 HU | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HU.txt` |
| 🇨🇳 CN | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CN.txt` |
| 🇰🇿 KZ | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KZ.txt` |
| 🇦🇺 AU | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AU.txt` |
| 🇮🇪 IE | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IE.txt` |
| 🇷🇴 RO | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RO.txt` |
| 🇵🇭 PH | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PH.txt` |
| 🇧🇷 BR | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BR.txt` |
| 🇭🇰 HK | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HK.txt` |
| 🇳🇿 NZ | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NZ.txt` |
| 🇦🇪 AE | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AE.txt` |
| 🇵🇱 PL | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PL.txt` |
| 🇲🇾 MY | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-MY.txt` |
| 🇨🇿 CZ | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CZ.txt` |
| 🇦🇹 AT | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AT.txt` |
| 🇮🇳 IN | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IN.txt` |
| 🇳🇴 NO | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NO.txt` |
| 🇧🇬 BG | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BG.txt` |
| 🇹🇼 TW | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TW.txt` |
| 🇻🇳 VN | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-VN.txt` |
| 🇵🇰 PK | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PK.txt` |
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

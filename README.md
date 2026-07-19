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
Contains **1525** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub.txt
```

### ✅ 403 Passed Configs
Contains **1525** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-403.txt
```

### 🏳️ Country Specific Configs
| Country | Count | Subscription Link |
| :--- | :---: | :--- |
| 🏳️ Unknown | 523 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-Unknown.txt` |
| 🇨🇦 CA | 380 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CA.txt` |
| 🇺🇸 US | 154 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-US.txt` |
| 🇳🇱 NL | 130 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NL.txt` |
| 🇩🇪 DE | 69 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-DE.txt` |
| 🇸🇨 SC | 38 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SC.txt` |
| 🇫🇷 FR | 35 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FR.txt` |
| 🇬🇧 GB | 34 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GB.txt` |
| 🇪🇪 EE | 17 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-EE.txt` |
| 🇸🇪 SE | 16 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SE.txt` |
| 🇵🇱 PL | 14 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PL.txt` |
| 🇱🇹 LT | 10 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LT.txt` |
| 🇷🇺 RU | 10 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RU.txt` |
| 🇫🇮 FI | 10 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FI.txt` |
| 🇸🇬 SG | 9 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SG.txt` |
| 🇯🇵 JP | 8 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-JP.txt` |
| 🇪🇸 ES | 7 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ES.txt` |
| 🇮🇹 IT | 6 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IT.txt` |
| 🇰🇿 KZ | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KZ.txt` |
| 🇸🇦 SA | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SA.txt` |
| 🇱🇻 LV | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LV.txt` |
| 🇦🇹 AT | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AT.txt` |
| 🇰🇷 KR | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KR.txt` |
| 🇮🇪 IE | 4 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IE.txt` |
| 🇧🇿 BZ | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BZ.txt` |
| 🇳🇿 NZ | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NZ.txt` |
| 🇨🇳 CN | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CN.txt` |
| 🇹🇷 TR | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TR.txt` |
| 🇬🇪 GE | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GE.txt` |
| 🇦🇺 AU | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AU.txt` |
| 🇵🇭 PH | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PH.txt` |
| 🇿🇦 ZA | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ZA.txt` |
| 🇦🇲 AM | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AM.txt` |
| 🇭🇰 HK | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HK.txt` |
| 🇦🇱 AL | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AL.txt` |
| 🇧🇷 BR | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BR.txt` |
| 🇮🇷 IR | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IR.txt` |
| 🇨🇾 CY | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CY.txt` |
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

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
Contains **1716** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub.txt
```

### ✅ 403 Passed Configs
Contains **1716** configurations.
```text
https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-403.txt
```

### 🏳️ Country Specific Configs
| Country | Count | Subscription Link |
| :--- | :---: | :--- |
| 🇺🇸 US | 263 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-US.txt` |
| 🇨🇦 CA | 255 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CA.txt` |
| 🇳🇱 NL | 215 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NL.txt` |
| 🏳️ Unknown | 178 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-Unknown.txt` |
| 🇩🇪 DE | 125 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-DE.txt` |
| 🇬🇧 GB | 104 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GB.txt` |
| 🇸🇨 SC | 91 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SC.txt` |
| 🇫🇮 FI | 70 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FI.txt` |
| 🇮🇹 IT | 63 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IT.txt` |
| 🇱🇹 LT | 59 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LT.txt` |
| 🇫🇷 FR | 43 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-FR.txt` |
| 🇹🇷 TR | 35 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TR.txt` |
| 🇯🇵 JP | 27 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-JP.txt` |
| 🇷🇺 RU | 24 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RU.txt` |
| 🇪🇸 ES | 21 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ES.txt` |
| 🇦🇪 AE | 16 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AE.txt` |
| 🇸🇪 SE | 13 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SE.txt` |
| 🇮🇷 IR | 13 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IR.txt` |
| 🇱🇻 LV | 12 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-LV.txt` |
| 🇭🇺 HU | 10 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HU.txt` |
| 🇨🇭 CH | 8 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CH.txt` |
| 🇸🇬 SG | 7 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-SG.txt` |
| 🇦🇺 AU | 6 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AU.txt` |
| 🇮🇪 IE | 6 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IE.txt` |
| 🇵🇱 PL | 6 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PL.txt` |
| 🇦🇹 AT | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AT.txt` |
| 🇰🇷 KR | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KR.txt` |
| 🇿🇦 ZA | 5 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ZA.txt` |
| 🇨🇳 CN | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CN.txt` |
| 🇮🇸 IS | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IS.txt` |
| 🇮🇳 IN | 3 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-IN.txt` |
| 🇳🇴 NO | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-NO.txt` |
| 🇬🇪 GE | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-GE.txt` |
| 🇹🇼 TW | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TW.txt` |
| 🇦🇱 AL | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AL.txt` |
| 🇦🇷 AR | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-AR.txt` |
| 🇮🇩 ID | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-ID.txt` |
| 🇪🇪 EE | 2 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-EE.txt` |
| 🇲🇴 MO | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-MO.txt` |
| 🇧🇷 BR | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-BR.txt` |
| 🇭🇰 HK | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-HK.txt` |
| 🇷🇸 RS | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-RS.txt` |
| 🇰🇿 KZ | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-KZ.txt` |
| 🇨🇿 CZ | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-CZ.txt` |
| 🇹🇭 TH | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-TH.txt` |
| 🇵🇹 PT | 1 | `https://raw.githubusercontent.com/Mokafela/Co-Killer/master/subs/sub-PT.txt` |
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

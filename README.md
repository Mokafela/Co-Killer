<div align="center">
  <h1>Config Killer</h1>
  <p>Automated tool to collect, verify, and split free V2Ray / VLESS / VMess / Trojan / Shadowsocks configs by their real exit country.</p>
</div>

## How it works

1. **Fetch** — pulls configs from subscription URLs (set via `CHANNEL_URL` secret).
2. **TCP check** — fast pre-filter that drops dead hosts.
3. **Exit-IP probe** — routes a request through each alive config using [xray-knife](https://github.com/lilendian0x00/xray-knife) and reads the real exit IP from Cloudflare's `/cdn-cgi/trace`.
4. **Country split** — looks up each exit IP on ip-api.com and writes a per-country subscription file to `split/`.

The pipeline runs automatically every 15 minutes via GitHub Actions and on every push.

## 🔗 Subscription Links

Import any link below directly into v2rayNG, Shadowrocket, NekoBox, or any V2Ray-compatible client.

<!-- SUBS_START -->
_Subscriptions will appear here after the first pipeline run._
<!-- SUBS_END -->

## 📱 Supported Clients

- **v2rayNG** (Android)
- **V2RayN** (Windows)
- **Shadowrocket** (iOS)
- **NekoBox / NekoRay** (PC / Android)
- **NapsternetV** (iOS / Android)
- **Sing-Box**

## ⚠️ Disclaimer

For educational purposes and open internet access only. Use responsibly.

# Redmi 10 (2022) ADB toolkit

Restore **Face Unlock** and **Fingerprint** after an earlier ADB change, then freeze ads / unused preinstalled apps and apply a few safe speed and battery tweaks.

No root. No bootloader unlock. Nothing writes to the `/system` partition. Every freeze can be undone.

This cloud environment cannot talk to your phone. Run the toolkit on **your PC** with the Redmi 10 plugged in.

## What it does

| Step | Action | Safe? |
| --- | --- | --- |
| Diagnose | Lists disabled apps and Face / Fingerprint package state | Read-only |
| Restore biometrics | Re-enables `com.miui.face` and related services; turns Face Unlock settings back on | Yes — this is the fix for the earlier disable |
| Debloat | Freezes Xiaomi ads, analytics, GetApps, Mi Browser, Facebook stubs, and similar extras | Reversible |
| Enhance | 0.5× animation speed, stop always-on Wi-Fi/Bluetooth scans, allow 90 Hz | Reversible |
| Undo | Re-enables everything this toolkit froze in the current session | Yes |

**Never touched:** Find Device, Security / Phone Manager, Xiaomi Account, SystemUI, Settings, Phone, Play Store, Gallery, Camera, and other packages that can bootloop or lock a Xiaomi phone.

## Phone setup (once)

1. Settings → About phone → tap **MIUI version** (or **OS version**) 7 times.
2. Settings → Additional settings → Developer options.
3. Enable **USB debugging**.
4. Enable **USB debugging (Security settings)** — required on MIUI 13+ / HyperOS or `pm` / `settings` commands are rejected.
5. Unlock the phone, plug in USB, choose **File transfer (MTP)**.
6. Tap **Allow** on the RSA fingerprint prompt. Check **Always allow**.

On the PC, `adb devices` must show `device` (not `unauthorized` or empty).

## PC setup

Install [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) so `adb` is on your PATH. Python 3.9+ is required for the menu.

### Windows

1. Unzip platform-tools (for example to `C:\platform-tools`).
2. Add that folder to PATH, **or** copy `adb.exe` next to these scripts.
3. Double-click `run.bat`, or in PowerShell:

```powershell
cd path\to\redmi10-adb
py -3 redmi10.py
```

### Linux / macOS

```bash
# Debian / Ubuntu
sudo apt install adb python3

cd redmi10-adb
chmod +x run.sh
./run.sh
```

## Recommended order

```bash
python3 redmi10.py diagnose      # see what the last ADB session disabled
python3 redmi10.py restore       # Face Unlock + Fingerprint back on
python3 redmi10.py recommended   # restore + ads/unused-app freeze + enhancements
```

Or use the menu (`python3 redmi10.py`) and pick **[6]**.

After restore:

1. Reboot the phone once if Face Unlock is still missing from Settings.
2. Settings → Passwords & security → **Face unlock** → add your face again.
3. Settings → Passwords & security → **Fingerprint** → add a finger again.

If you previously used `pm uninstall --user 0 com.miui.face`, the restore step runs `cmd package install-existing com.miui.face` to bring that system app back.

## Debloat scope

**Ads / analytics (always in recommended):** MSA ads, Analytics, Joyose, GetApps discovery, bugreport, wallpaper carousel ads, and similar daemons.

**Unused apps (included in recommended):** Mi Browser, Mi Music, Mi Video, ShareMe, Yellow Pages, GetApps, Mi Credit, Quick Ball, Facebook stubs, FM radio, Compass, and a few store / partner apps.

**Left installed on purpose:** Gallery, Camera, Security, Phone, Messages, Mi Account, Mi Cloud, Find Device. Those are easy to break on Redmi phones.

Ads-only (keep unused Xiaomi apps):

```bash
python3 redmi10.py debloat --ads-only
```

Undo the last freeze from this toolkit:

```bash
python3 redmi10.py undo
```

Re-enable **every** currently disabled package (useful if you do not remember what the old ADB session turned off):

```bash
python3 redmi10.py restore --all-disabled
```

## Manual ADB (no Python)

See [commands/manual-adb.md](commands/manual-adb.md).

## Device

Written for **Redmi 10 2022** (selene, models such as 22011119TI / 22011119UY), MIUI 13/14 or HyperOS. Package names that are not installed are skipped.

## Safety

- Do not disable Find Device (`com.xiaomi.finddevice`) or Security (`com.miui.securitycenter`). That can bootloop or factory-reset-lock the phone.
- A factory reset returns every frozen or user-uninstalled system app.
- Official OTA updates still arrive. After a big MIUI → HyperOS upgrade, freeze ads again if they come back.
- Banking apps and Play Integrity are not affected: the bootloader stays locked and `/system` is not modified.

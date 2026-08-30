# No ads (no APK patching)

Two layers:

1. Freeze Xiaomi ad / analytics apps.
2. Android **Private DNS** → AdGuard, which blocks most ad servers used inside games (including Chess Lv.100).

This does not modify any APK. The official in-app purchase still exists if you want UNBALANCE Premium instead.

Undo DNS: **Settings → Connection & sharing → Private DNS → Automatic**

## PowerShell (from platform-tools)

```powershell
cd F:\ADB\platform-tools-latest-windows\platform-tools

.\adb shell pm disable-user --user 0 com.miui.msa.global
.\adb shell pm disable-user --user 0 com.miui.systemAdSolution
.\adb shell pm disable-user --user 0 com.xiaomi.adserver
.\adb shell pm disable-user --user 0 com.miui.analytics
.\adb shell pm disable-user --user 0 com.xiaomi.joyose
.\adb shell pm disable-user --user 0 com.miui.daemon
.\adb shell pm disable-user --user 0 com.xiaomi.discover
.\adb shell pm disable-user --user 0 com.miui.android.fashiongallery
.\adb shell pm disable-user --user 0 com.xiaomi.glgm
.\adb shell pm disable-user --user 0 com.xiaomi.gamecenter.sdk.service
.\adb shell pm disable-user --user 0 com.xiaomi.mipicks
.\adb shell pm disable-user --user 0 com.miui.hybrid

.\adb shell settings put global personalized_ad_enabled 0
.\adb shell settings put system passport_ad_status OFF
.\adb shell settings put global private_dns_mode hostname
.\adb shell settings put global private_dns_specifier dns.adguard-dns.com
```

Then **force-close** The Chess Lv.100 (Settings → Apps → The Chess Lv.100 → Force stop) and open it again.

If Wi-Fi or an app breaks, turn Private DNS back to Automatic.

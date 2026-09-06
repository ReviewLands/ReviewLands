# The Chess Lv.100 — cleaner on Redmi 10

App: **The Chess Lv.100 (plus Online)**  
Package: `jp.co.unbalance.android.chessunbcc`

Turns off Xiaomi ads and sets Private DNS (AdGuard) so most in-game ad servers are blocked. It does **not** patch the Chess APK.

Fingerprint is not changed.

## PowerShell (from platform-tools)

```powershell
cd F:\ADB\platform-tools-latest-windows\platform-tools
.\adb devices

.\adb shell pm path jp.co.unbalance.android.chessunbcc

.\adb shell pm disable-user --user 0 com.miui.msa.global
.\adb shell pm disable-user --user 0 com.miui.analytics
.\adb shell pm disable-user --user 0 com.xiaomi.joyose
.\adb shell pm disable-user --user 0 com.miui.daemon
.\adb shell pm disable-user --user 0 com.xiaomi.discover
.\adb shell pm disable-user --user 0 com.miui.bugreport
.\adb shell pm disable-user --user 0 com.miui.android.fashiongallery
.\adb shell pm disable-user --user 0 com.xiaomi.glgm
.\adb shell pm disable-user --user 0 com.xiaomi.gamecenter.sdk.service
.\adb shell pm disable-user --user 0 com.xiaomi.mipicks

.\adb shell dumpsys deviceidle whitelist +jp.co.unbalance.android.chessunbcc
.\adb shell cmd appops set jp.co.unbalance.android.chessunbcc RUN_IN_BACKGROUND allow
.\adb shell cmd appops set jp.co.unbalance.android.chessunbcc RUN_ANY_IN_BACKGROUND allow
```

Then open **The Chess Lv.100** and play.

Or, if `redmi10.cmd` is next to `adb.exe`:

```powershell
.\redmi10.cmd chess
```

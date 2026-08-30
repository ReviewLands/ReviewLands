# Manual ADB commands

Use these from your `platform-tools` folder in PowerShell. Prefix with `.\` so Windows uses `adb.exe` in that folder. USB debugging (including **Security settings**) must be on.

## 1. See what is disabled

```powershell
.\adb devices
.\adb shell getprop ro.product.model
.\adb shell getprop ro.product.device
.\adb shell getprop ro.miui.ui.version.name
.\adb shell pm list packages -d
.\adb shell pm path com.miui.face
.\adb shell settings get secure face_unlock_keyguard_enabled
```

## 2. Restore Face Unlock and Fingerprint

```powershell
.\adb shell pm unhide com.miui.face
.\adb shell pm enable --user 0 com.miui.face
.\adb shell cmd package install-existing com.miui.face

.\adb shell pm enable --user 0 com.android.facelock
.\adb shell cmd package install-existing com.android.facelock

.\adb shell pm enable --user 0 com.xiaomi.fido
.\adb shell cmd package install-existing com.xiaomi.fido

.\adb shell pm enable --user 0 org.ifaa.aidl.manager
.\adb shell cmd package install-existing org.ifaa.aidl.manager

.\adb shell settings put secure face_unlock_keyguard_enabled 1
.\adb shell settings put global face_unlock_keyguard_enabled 1
.\adb shell settings put secure face_unlock_disabled 0
```

Then on the phone: **Settings → Passwords & security → Face unlock** and **Fingerprint**. Reboot once if the menus are still missing.

To turn **every** disabled package back on, list them and enable each name:

```bash
adb shell pm list packages -d
adb shell pm enable --user 0 com.example.package
adb shell cmd package install-existing com.example.package
```

## 3. Freeze ads and unused apps

Prefer disable (easy undo) over uninstall:

```bash
adb shell pm disable-user --user 0 com.miui.msa.global
adb shell pm disable-user --user 0 com.miui.analytics
adb shell pm disable-user --user 0 com.xiaomi.joyose
adb shell pm disable-user --user 0 com.miui.daemon
adb shell pm disable-user --user 0 com.xiaomi.discover
adb shell pm disable-user --user 0 com.miui.bugreport
adb shell pm disable-user --user 0 com.miui.android.fashiongallery
adb shell pm disable-user --user 0 com.mi.globalbrowser
adb shell pm disable-user --user 0 com.miui.player
adb shell pm disable-user --user 0 com.miui.videoplayer
adb shell pm disable-user --user 0 com.xiaomi.midrop
adb shell pm disable-user --user 0 com.xiaomi.mipicks
adb shell pm disable-user --user 0 com.facebook.appmanager
adb shell pm disable-user --user 0 com.facebook.services
adb shell pm disable-user --user 0 com.facebook.system
```

Undo one package:

```bash
adb shell pm enable --user 0 com.miui.msa.global
```

**Do not run** disable/uninstall on:

- `com.xiaomi.finddevice`
- `com.miui.securitycenter`
- `com.miui.securityadd`
- `com.xiaomi.xmsf`
- `com.xiaomi.account`
- `com.miui.face`

## 4. Enhancements

```bash
adb shell settings put global window_animation_scale 0.5
adb shell settings put global transition_animation_scale 0.5
adb shell settings put global animator_duration_scale 0.5
adb shell settings put global wifi_scan_always_enabled 0
adb shell settings put global ble_scan_always_enabled 0
adb shell settings put system peak_refresh_rate 90
```

Restore stock animation speed:

```bash
adb shell settings put global window_animation_scale 1
adb shell settings put global transition_animation_scale 1
adb shell settings put global animator_duration_scale 1
```

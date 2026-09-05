# Fix "Install secure call from null" during calls

That banner is a **ghost second call**. Google Phone shows it when a SIM / RCS / caller-ID service was frozen. The account label becomes `null`.

Tap **DECLINE** (not ANSWER — Answer ends your real call).

## PowerShell (from platform-tools)

```powershell
cd F:\ADB\platform-tools-latest-windows\platform-tools
.\adb devices

.\adb shell pm enable --user 0 com.xiaomi.simactivate.service
.\adb shell cmd package install-existing com.xiaomi.simactivate.service

.\adb shell pm enable --user 0 com.xiaomi.mircs
.\adb shell cmd package install-existing com.xiaomi.mircs

.\adb shell pm enable --user 0 com.miui.yellowpage
.\adb shell cmd package install-existing com.miui.yellowpage

.\adb shell pm enable --user 0 com.xiaomi.mi_connect_service
.\adb shell cmd package install-existing com.xiaomi.mi_connect_service

.\adb shell pm enable --user 0 com.google.android.ims
.\adb shell cmd package install-existing com.google.android.ims

.\adb shell pm enable --user 0 com.google.android.dialer
.\adb shell cmd package install-existing com.google.android.dialer

.\adb reboot
```

After reboot, make a test call. The fake banner should be gone.

If it is still there, Private DNS may be breaking verified/secure-call lookups:

```powershell
.\adb shell settings put global private_dns_mode opportunistic
```

Or on the phone: **Settings → Connection & sharing → Private DNS → Automatic**.

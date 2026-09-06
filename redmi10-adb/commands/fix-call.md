# Fix "Install secure call from null" + line stays busy

The banner is a **ghost second call**. After you hang up, Telecom still thinks a call is active, so other people hear **busy** until you clear the Phone app cache.

Tap **DECLINE** on the banner (not ANSWER).

`com.xiaomi.mircs` and `com.xiaomi.mi_connect_service` do not exist on Global Redmi 10. Ignore those errors.

## Strong fix (PowerShell)

```powershell
cd F:\ADB\platform-tools-latest-windows\platform-tools
.\adb devices

# 1) Stop AdGuard DNS from breaking verified / secure-call lookups
.\adb shell settings put global private_dns_mode opportunistic

# 2) Turn off call-screening role (spam/"secure call" injector)
.\adb shell cmd role clear-role-holders android.app.role.CALL_SCREENING

# 3) Bring back call-related apps (skip any "Unknown package")
foreach ($p in @(
  'com.xiaomi.simactivate.service',
  'com.miui.yellowpage',
  'com.google.android.ims',
  'com.android.carrierdefaultapp',
  'com.google.android.dialer',
  'com.android.phone',
  'com.android.incallui',
  'com.android.contacts',
  'com.google.android.contacts',
  'com.android.stk',
  'com.android.stk2',
  'com.facebook.services',
  'com.facebook.system',
  'com.truecaller'
)) {
  .\adb shell pm enable --user 0 $p
  .\adb shell cmd package install-existing $p
}

# 4) Re-enable any still-disabled telephony-looking package
.\adb shell pm list packages -d

# 5) End the stuck call the same way cache-clear does
.\adb shell am force-stop com.google.android.dialer
.\adb shell am force-stop com.android.phone
.\adb shell am force-stop com.google.android.ims
.\adb shell pm clear --cache-only com.google.android.dialer
.\adb shell pm clear --cache-only com.android.phone
.\adb shell pm clear com.google.android.dialer

.\adb reboot
```

`pm clear com.google.android.dialer` resets Phone app settings only (not your system call log). That is what actually drops the stuck "secure call from null" account.

After reboot, make one test call, hang up, then have someone call you. You should not be busy.

## If it is still there

Paste this output back:

```powershell
.\adb shell cmd telecom get-default-dialer
.\adb shell cmd role get-role-holders android.app.role.DIALER
.\adb shell cmd role get-role-holders android.app.role.CALL_SCREENING
.\adb shell pm list packages -d
.\adb shell settings get global private_dns_mode
.\adb shell dumpsys telecom
```

The last command is long; that is OK.

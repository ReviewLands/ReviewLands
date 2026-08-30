@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Redmi 10 ADB toolkit
cd /d "%~dp0"

rem Prefer adb.exe beside this script (drop this file into platform-tools).
if exist "%~dp0adb.exe" (
  set "ADB=%~dp0adb.exe"
) else if exist ".\adb.exe" (
  set "ADB=.\adb.exe"
) else (
  set "ADB=adb"
)

set "UNDO=%~dp0redmi10-undo.txt"
set "ACTION=%~1"

"%ADB%" version >nul 2>&1
if errorlevel 1 (
  echo adb not found.
  echo Copy redmi10.cmd into your platform-tools folder, next to adb.exe.
  echo Example: F:\ADB\platform-tools-latest-windows\platform-tools\
  call :maybe_pause
  exit /b 1
)

if /i "%ACTION%"=="diagnose" goto :do_diagnose
if /i "%ACTION%"=="restore" goto :do_restore
if /i "%ACTION%"=="debloat" goto :do_debloat
if /i "%ACTION%"=="enhance" goto :do_enhance
if /i "%ACTION%"=="undo" goto :do_undo
if /i "%ACTION%"=="recommended" goto :do_recommended
if /i "%ACTION%"=="restore-all" goto :do_restore_all
if /i "%ACTION%"=="menu" goto :menu
if not "%ACTION%"=="" (
  echo Unknown action: %ACTION%
  echo Use: diagnose  restore  restore-all  debloat  enhance  undo  recommended
  exit /b 1
)

:menu
echo.
echo ================================================================
echo  Redmi 10 ADB toolkit  ^(no Python needed^)
echo ================================================================
call :show_device
echo.
echo   [1] Diagnose ^(read-only^)
echo   [2] Restore Face Unlock + Fingerprint
echo   [3] Debloat ads + unused apps
echo   [4] Enhancements
echo   [5] Undo last debloat from this script
echo   [6] Recommended: restore + debloat + enhance
echo   [7] Restore ALL currently disabled packages
echo   [0] Quit
echo.
set /p "CHOICE=Choose: "
if "%CHOICE%"=="1" goto :do_diagnose
if "%CHOICE%"=="2" goto :do_restore
if "%CHOICE%"=="3" goto :do_debloat
if "%CHOICE%"=="4" goto :do_enhance
if "%CHOICE%"=="5" goto :do_undo
if "%CHOICE%"=="6" goto :do_recommended
if "%CHOICE%"=="7" goto :do_restore_all
if "%CHOICE%"=="0" exit /b 0
echo Unknown choice.
goto :menu

:do_diagnose
call :need_device
if errorlevel 1 goto :fail
echo.
echo ================================================================
echo  Diagnose
echo ================================================================
call :show_device
echo.
echo Disabled packages:
"%ADB%" shell pm list packages -d
echo.
echo Face Unlock package:
"%ADB%" shell pm path com.miui.face
echo.
echo Settings:
"%ADB%" shell settings get secure face_unlock_keyguard_enabled
"%ADB%" shell settings get global face_unlock_keyguard_enabled
"%ADB%" shell settings get secure face_unlock_disabled
echo.
echo Next:  redmi10.cmd restore
goto :finish

:do_restore
call :need_device
if errorlevel 1 goto :fail
call :restore_work
goto :finish

:do_restore_all
call :need_device
if errorlevel 1 goto :fail
echo.
echo Re-enabling every disabled package...
for /f "tokens=2 delims=:" %%P in ('"%ADB%" shell pm list packages -d') do (
  call :enable_pkg %%P
)
call :face_settings
goto :finish

:do_debloat
call :need_device
if errorlevel 1 goto :fail
call :debloat_work
goto :finish

:do_enhance
call :need_device
if errorlevel 1 goto :fail
call :enhance_work
goto :finish

:do_undo
call :need_device
if errorlevel 1 goto :fail
if not exist "%UNDO%" (
  echo No undo file yet. Use restore-all if you want every disabled app back.
  goto :finish
)
echo Re-enabling packages from %UNDO%
for /f "usebackq tokens=* delims=" %%P in ("%UNDO%") do (
  if not "%%P"=="" call :enable_pkg %%P
)
echo Undo finished.
goto :finish

:do_recommended
call :need_device
if errorlevel 1 goto :fail
call :restore_work
call :debloat_work
call :enhance_work
echo.
echo Recommended setup finished.
goto :finish

:restore_work
echo.
echo ================================================================
echo  Restore Face Unlock + Fingerprint
echo ================================================================
for %%P in (
  com.miui.face
  com.android.facelock
  com.xiaomi.fido
  com.xiaomi.fidoauth
  com.miui.biometricauth
  com.fingerprints.service
  com.fingerprints.serviceext
  com.fingerprints.extension.service
  com.goodix.fingerprint
  com.goodix.fingerprint.setting
  com.goodix.gftest
  org.ifaa.aidl.manager
  vendor.xiaomi.hardware.fingerprintextension
  com.android.server.biometrics
  com.mlab.faceunlock
  com.xiaomi.biometric
  com.fingerprints.sensortest
) do call :enable_pkg %%P
call :face_settings
echo.
echo On the phone:
echo   Settings - Passwords ^& security - Face unlock
echo   Settings - Passwords ^& security - Fingerprint
echo Reboot once if those menus are still missing.
goto :eof

:face_settings
echo Turning Face Unlock settings back on...
"%ADB%" shell settings put secure face_unlock_keyguard_enabled 1
"%ADB%" shell settings put global face_unlock_keyguard_enabled 1
"%ADB%" shell settings put secure face_unlock_disabled 0
"%ADB%" shell settings put secure lockscreen.face_unlock 1
goto :eof

:debloat_work
echo.
echo ================================================================
echo  Debloat ^(freeze, reversible^)
echo ================================================================
for %%P in (
  com.miui.msa.global
  com.miui.systemAdSolution
  com.miui.analytics
  com.xiaomi.joyose
  com.miui.daemon
  com.xiaomi.discover
  com.miui.bugreport
  com.miui.miservice
  com.xiaomi.ab
  com.miui.android.fashiongallery
  com.mfashiongallery.emag
  com.xiaomi.glgm
  com.miui.translation.kingsoft
  com.miui.translation.youdao
  com.miui.translationservice
  com.xiaomi.gamecenter.sdk.service
  com.xiaomi.migameservice
  com.xiaomi.aiasst.service
  com.miui.contentcatcher
  com.miui.audiomonitor
  com.miui.voicetrigger
  com.xiaomi.mi_connect_service
  com.xiaomi.powerchecker
  com.mi.globalbrowser
  com.android.browser
  com.miui.player
  com.miui.videoplayer
  com.miui.video
  com.xiaomi.midrop
  com.miui.yellowpage
  com.xiaomi.mipicks
  com.xiaomi.payment
  com.mipay.wallet.in
  com.mipay.wallet.id
  com.duokan.phone.remotecontroller
  com.duokan.phone.remotecontroller.peel.plugin
  com.miui.hybrid
  com.miui.hybrid.accessory
  com.miui.compass
  com.xiaomi.scanner
  com.miui.fm
  com.miui.fmservice
  com.mi.global.bbs
  com.mi.global.shop
  com.xiaomi.smarthome
  com.miui.enbbs
  com.miui.phrase
  com.facebook.appmanager
  com.facebook.services
  com.facebook.system
  com.facebook.katana
  com.linkedin.android
  com.netflix.partner.activation
  com.netflix.mediaclient
  com.amazon.appmanager
  com.amazon.mShop.android.shopping
  cn.wps.xiaomi.abroad.lite
  com.miui.touchassistant
  com.xiaomi.mirecycle
  com.xiaomi.calendar
  com.miui.weather2
  com.xiaomi.vipaccount
  com.xiaomi.mircs
  com.xiaomi.mirror
  com.xiaomi.simactivate.service
) do call :disable_pkg %%P
echo.
echo Undo with:  redmi10.cmd undo
goto :eof

:enhance_work
echo.
echo ================================================================
echo  Enhancements
echo ================================================================
"%ADB%" shell settings put global window_animation_scale 0.5
"%ADB%" shell settings put global transition_animation_scale 0.5
"%ADB%" shell settings put global animator_duration_scale 0.5
"%ADB%" shell settings put global wifi_scan_always_enabled 0
"%ADB%" shell settings put global ble_scan_always_enabled 0
"%ADB%" shell settings put system peak_refresh_rate 90
echo Done. Animations are 0.5x. Background Wi-Fi/Bluetooth scans are off.
goto :eof

:need_device
"%ADB%" start-server >nul 2>&1
echo.
"%ADB%" devices
"%ADB%" devices | findstr /e /i "device" >nul
if errorlevel 1 (
  echo Phone is not connected in ADB device mode.
  echo Unlock the phone, enable USB debugging + USB debugging ^(Security settings^),
  echo tap Allow on the prompt, then run this again.
  exit /b 1
)
exit /b 0

:show_device
echo   Brand/model:
"%ADB%" shell getprop ro.product.brand
"%ADB%" shell getprop ro.product.model
echo   Device:
"%ADB%" shell getprop ro.product.device
echo   Android:
"%ADB%" shell getprop ro.build.version.release
echo   MIUI:
"%ADB%" shell getprop ro.miui.ui.version.name
echo   HyperOS:
"%ADB%" shell getprop ro.mi.os.version.name
goto :eof

:enable_pkg
set "PKG=%~1"
if "%PKG%"=="" goto :eof
echo   restore %PKG%
"%ADB%" shell pm unhide %PKG% >nul 2>&1
"%ADB%" shell pm enable --user 0 %PKG%
"%ADB%" shell cmd package install-existing %PKG%
goto :eof

:disable_pkg
set "PKG=%~1"
if "%PKG%"=="" goto :eof
echo %PKG% | findstr /i "face fingerprint biometric fido goodix ifaa facelock" >nul
if not errorlevel 1 (
  echo   [keep] %PKG% ^(biometric^)
  goto :eof
)
echo %PKG% | findstr /x /i "com.xiaomi.finddevice com.miui.securitycenter com.miui.securityadd com.miui.securitycore com.xiaomi.xmsf com.xiaomi.account" >nul
if not errorlevel 1 (
  echo   [keep] %PKG% ^(protected^)
  goto :eof
)
"%ADB%" shell pm path %PKG% 2>nul | findstr /i "package:" >nul
if errorlevel 1 (
  echo   [skip] %PKG%
  goto :eof
)
echo   freeze %PKG%
"%ADB%" shell pm disable-user --user 0 %PKG%
>>"%UNDO%" echo %PKG%
goto :eof

:finish
if "%ACTION%"=="" (
  echo.
  pause
  goto :menu
)
exit /b 0

:fail
call :maybe_pause
exit /b 2

:maybe_pause
if "%ACTION%"=="" pause
goto :eof

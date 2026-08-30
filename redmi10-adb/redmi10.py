#!/usr/bin/env python3
"""Redmi 10 (2022) ADB toolkit: restore biometrics, debloat, enhance.

Works without root. Freeze (disable-user) is preferred over uninstall so
every change can be reversed. Critical Xiaomi packages are never touched.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LISTS = ROOT / "lists"
LOGS = ROOT / "logs"
SESSION_RESTORE = ROOT / ".session-restore.txt"

BIOMETRIC_RE = re.compile(
    r"face|fingerprint|biometric|fido|goodix|ifaa|soter|facelock",
    re.IGNORECASE,
)


class AdbError(RuntimeError):
    pass


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def ensure_logs() -> Path:
    LOGS.mkdir(exist_ok=True)
    return LOGS / f"session-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.log"


class Logger:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(exist_ok=True)

    def write(self, line: str) -> None:
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp()}] {line}\n")


def load_list(name: str) -> list[str]:
    path = LISTS / name
    packages: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if line:
            packages.append(line)
    return packages


def run_adb(args: list[str], timeout: int = 45) -> subprocess.CompletedProcess[str]:
    adb = shutil.which("adb")
    if not adb:
        raise AdbError(
            "adb was not found on PATH. Install Android platform-tools "
            "and try again: https://developer.android.com/tools/releases/platform-tools"
        )
    return subprocess.run(
        [adb, *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )


def adb_ok() -> str:
    result = run_adb(["version"])
    if result.returncode != 0:
        raise AdbError(result.stderr.strip() or "adb version failed")
    return result.stdout.splitlines()[0] if result.stdout else "adb"


def connected_devices() -> list[str]:
    result = run_adb(["devices"])
    devices: list[str] = []
    for line in result.stdout.splitlines()[1:]:
        parts = line.split()
        if len(parts) >= 2 and parts[1] == "device":
            devices.append(parts[0])
    return devices


def shell(command: str, timeout: int = 45) -> subprocess.CompletedProcess[str]:
    return run_adb(["shell", command], timeout=timeout)


def getprop(key: str) -> str:
    result = shell(f"getprop {key}")
    return (result.stdout or "").strip()


def settings_get(namespace: str, key: str) -> str:
    result = shell(f"settings get {namespace} {key}")
    return (result.stdout or "").strip()


def settings_put(namespace: str, key: str, value: str) -> tuple[bool, str]:
    result = shell(f"settings put {namespace} {key} {value}")
    err = (result.stderr or "").strip()
    if result.returncode != 0 or "Exception" in err or "Error" in err:
        return False, err or (result.stdout or "").strip() or "settings put failed"
    return True, "ok"


def package_installed(package: str) -> bool:
    result = shell(f"pm path {package}")
    return "package:" in (result.stdout or "")


def list_packages(flag: str = "") -> list[str]:
    cmd = "pm list packages" if not flag else f"pm list packages {flag}"
    result = shell(cmd)
    names: list[str] = []
    for line in (result.stdout or "").splitlines():
        if line.startswith("package:"):
            names.append(line.split("package:", 1)[1].strip())
    return sorted(names)


def record_restore(package: str, action: str) -> None:
    with SESSION_RESTORE.open("a", encoding="utf-8") as handle:
        handle.write(f"{action}\t{package}\n")


def enable_package(package: str) -> tuple[str, str]:
    """Re-enable or reinstall a package for user 0. Enabling protected apps is allowed."""
    hide = shell(f"pm unhide {package}")
    enable = shell(f"pm enable --user 0 {package}")
    existing = shell(f"cmd package install-existing {package}")
    enable_out = ((enable.stdout or "") + (enable.stderr or "")).strip()
    existing_out = ((existing.stdout or "") + (existing.stderr or "")).strip()
    hide_out = ((hide.stdout or "") + (hide.stderr or "")).strip()
    detail = existing_out or enable_out or hide_out

    now_installed = package_installed(package)
    enabled_ok = "enabled" in enable_out.lower() or (
        enable.returncode == 0 and now_installed
    )
    installed_ok = existing.returncode == 0 and (
        "installed" in existing_out.lower() or now_installed
    )
    if enabled_ok or installed_ok:
        return "restored", detail or "enabled"
    if not now_installed:
        return "missing", detail or "not on this device"
    return "failed", detail or "could not restore"


def disable_package(package: str) -> tuple[str, str]:
    if package in load_never():
        return "blocked", "protected package"
    if BIOMETRIC_RE.search(package):
        return "blocked", "biometric-related — skipped to keep Face / Fingerprint working"
    if not package_installed(package):
        return "missing", "not installed"

    result = shell(f"pm disable-user --user 0 {package}")
    out = ((result.stdout or "") + (result.stderr or "")).strip()
    if "disabled" in out.lower() or result.returncode == 0:
        record_restore(package, "enable")
        return "disabled", out or "disabled"
    if "SecurityException" in out or "not allowed" in out.lower():
        uninstall = shell(f"pm uninstall -k --user 0 {package}")
        uout = ((uninstall.stdout or "") + (uninstall.stderr or "")).strip()
        if "Success" in uout or uninstall.returncode == 0:
            record_restore(package, "install-existing")
            return "uninstalled-user", uout or "uninstalled for user 0"
        return "failed", out + " | " + uout
    return "failed", out or "disable failed"


_never_cache: list[str] | None = None


def load_never() -> list[str]:
    global _never_cache
    if _never_cache is None:
        _never_cache = load_list("never-touch.txt")
    return _never_cache


def print_header(title: str) -> None:
    print()
    print("=" * 64)
    print(title)
    print("=" * 64)


def device_info() -> dict[str, str]:
    keys = {
        "brand": "ro.product.brand",
        "model": "ro.product.model",
        "device": "ro.product.device",
        "name": "ro.product.name",
        "android": "ro.build.version.release",
        "sdk": "ro.build.version.sdk",
        "miui": "ro.miui.ui.version.name",
        "hyperos": "ro.mi.os.version.name",
        "incremental": "ro.build.version.incremental",
    }
    info = {label: getprop(prop) for label, prop in keys.items()}
    return info


def show_device(info: dict[str, str]) -> None:
    os_name = info.get("hyperos") or info.get("miui") or "unknown"
    print(f"  Brand / model : {info.get('brand', '?')} {info.get('model', '?')}")
    print(f"  Codename      : {info.get('device', '?')} ({info.get('name', '?')})")
    print(f"  Android       : {info.get('android', '?')} (SDK {info.get('sdk', '?')})")
    print(f"  MIUI / OS     : {os_name}")
    print(f"  Build         : {info.get('incremental', '?')}")


def diagnose(log: Logger) -> None:
    print_header("Diagnose (read-only)")
    info = device_info()
    show_device(info)
    log.write(f"device={info}")

    print("\nDisabled packages:")
    disabled = list_packages("-d")
    if not disabled:
        print("  (none)")
    else:
        for pkg in disabled:
            mark = "  [biometric?]" if BIOMETRIC_RE.search(pkg) else ""
            print(f"  - {pkg}{mark}")
    log.write(f"disabled={disabled}")

    print("\nBiometric packages on this phone:")
    wanted = load_list("restore-biometrics.txt")
    disabled_set = set(disabled)
    for pkg in wanted:
        if package_installed(pkg):
            state = "DISABLED" if pkg in disabled_set else "enabled"
        else:
            # install-existing may still work if the APK is on /system
            state = "not visible (may still be restorable)"
        print(f"  - {pkg}: {state}")

    extra_disabled = [p for p in disabled if BIOMETRIC_RE.search(p) and p not in wanted]
    if extra_disabled:
        print("\nOther disabled packages that look biometric-related:")
        for pkg in extra_disabled:
            print(f"  - {pkg}")

    print("\nFace / lock settings:")
    for ns, key in (
        ("secure", "face_unlock_keyguard_enabled"),
        ("global", "face_unlock_keyguard_enabled"),
        ("secure", "face_unlock_disabled"),
        ("secure", "lockscreen.face_unlock"),
        ("system", "peak_refresh_rate"),
        ("system", "min_refresh_rate"),
        ("global", "window_animation_scale"),
        ("global", "transition_animation_scale"),
        ("global", "animator_duration_scale"),
    ):
        value = settings_get(ns, key)
        print(f"  {ns}/{key} = {value}")
        log.write(f"setting {ns}/{key}={value}")

    print("\nNext step: choose [2] to restore Face Unlock and Fingerprint.")


def restore_biometrics(log: Logger, restore_all_disabled: bool = False) -> None:
    print_header("Restore Face Unlock + Fingerprint")
    restored: list[str] = []
    missing: list[str] = []
    failed: list[str] = []

    targets = load_list("restore-biometrics.txt")
    if restore_all_disabled:
        targets = sorted(set(targets) | set(list_packages("-d")))

    extra = [p for p in list_packages("-d") if BIOMETRIC_RE.search(p)]
    targets = sorted(set(targets) | set(extra))

    for pkg in targets:
        status, detail = enable_package(pkg)
        log.write(f"restore {pkg} -> {status} {detail}")
        if status in {"restored", "enabled"}:
            print(f"  [ok]   {pkg}")
            restored.append(pkg)
        elif status == "missing":
            print(f"  [skip] {pkg} (not on this device)")
            missing.append(pkg)
        elif status == "blocked":
            print(f"  [skip] {pkg} ({detail})")
        else:
            print(f"  [fail] {pkg}: {detail}")
            failed.append(pkg)

    print("\nTurning Face Unlock settings back on...")
    for ns, key, value in (
        ("secure", "face_unlock_keyguard_enabled", "1"),
        ("global", "face_unlock_keyguard_enabled", "1"),
        ("secure", "face_unlock_disabled", "0"),
        ("secure", "lockscreen.face_unlock", "1"),
    ):
        ok, detail = settings_put(ns, key, value)
        mark = "ok" if ok else "warn"
        print(f"  [{mark}] {ns}/{key}={value} {'' if ok else detail}")
        log.write(f"settings put {ns} {key} {value} -> {detail}")

    print()
    print(f"Restored/enabled: {len(restored)}")
    print(f"Not on device:    {len(missing)}")
    print(f"Failed:           {len(failed)}")
    print()
    print("On the phone now:")
    print("  Settings → Passwords & security → Face unlock  → add your face again")
    print("  Settings → Passwords & security → Fingerprint  → add a finger again")
    print("If Face unlock is still missing, reboot once, then open that menu again.")


def debloat(log: Logger, include_apps: bool) -> None:
    print_header("Debloat (reversible freeze)")
    packages = load_list("debloat-ads.txt")
    if include_apps:
        packages += load_list("debloat-apps.txt")

    counts = {"disabled": 0, "uninstalled-user": 0, "missing": 0, "blocked": 0, "failed": 0}
    for pkg in packages:
        status, detail = disable_package(pkg)
        log.write(f"debloat {pkg} -> {status} {detail}")
        counts[status] = counts.get(status, 0) + 1
        label = {
            "disabled": "ok",
            "uninstalled-user": "ok-user",
            "missing": "skip",
            "blocked": "keep",
            "failed": "fail",
        }.get(status, status)
        extra = f" ({detail})" if status in {"failed", "blocked"} else ""
        print(f"  [{label:7}] {pkg}{extra}")

    print()
    print(
        "Disabled {disabled}, user-uninstalled {uninstalled-user}, "
        "skipped missing {missing}, blocked {blocked}, failed {failed}.".format(**counts)
    )
    print(f"Undo file: {SESSION_RESTORE}")
    print("Use menu [5] to restore everything this session froze.")


CHESS_PACKAGE = "jp.co.unbalance.android.chessunbcc"


def chess_clean(log: Logger) -> None:
    print_header("The Chess Lv.100 — Xiaomi ads off, game protected")
    print("Blocks Xiaomi ads and ad servers. Does not patch the Chess APK.")
    print()

    if package_installed(CHESS_PACKAGE):
        print(f"Found The Chess Lv.100 ({CHESS_PACKAGE})")
    else:
        print(f"Not installed as {CHESS_PACKAGE}")
        matches = [p for p in list_packages() if "chess" in p.lower() or "unbalance" in p.lower()]
        if matches:
            print("Packages matching chess / unbalance:")
            for pkg in matches:
                print(f"  - {pkg}")
        else:
            print("No chess package found. Install The Chess Lv.100 from Play Store.")
        return

    ads_off(log)

    print("\nProtecting the chess app from MIUI background killing...")
    for command in (
        f"dumpsys deviceidle whitelist +{CHESS_PACKAGE}",
        f"cmd appops set {CHESS_PACKAGE} RUN_IN_BACKGROUND allow",
        f"cmd appops set {CHESS_PACKAGE} RUN_ANY_IN_BACKGROUND allow",
    ):
        result = shell(command)
        out = ((result.stdout or "") + (result.stderr or "")).strip()
        print(f"  {command}")
        if out:
            print(f"    {out}")
        log.write(f"{command} -> {out or 'ok'}")

    print()
    print("Force-close The Chess Lv.100 if it is open, then play again.")


def ads_off(log: Logger) -> None:
    print_header("No ads — Xiaomi services + Private DNS")
    print("Does not patch any APK. Blocks Xiaomi ad apps and ad servers.")
    extra = (
        "com.xiaomi.mipicks",
        "com.miui.hybrid",
        "com.miui.hybrid.accessory",
        "com.facebook.appmanager",
        "com.facebook.services",
        "com.facebook.system",
    )
    for pkg in load_list("debloat-ads.txt") + list(extra):
        status, detail = disable_package(pkg)
        log.write(f"ads-off {pkg} -> {status} {detail}")
        label = "ok" if status in {"disabled", "uninstalled-user"} else status
        print(f"  [{label:7}] {pkg}")

    print("\nXiaomi ad settings + AdGuard Private DNS...")
    for ns, key, value in (
        ("global", "personalized_ad_enabled", "0"),
        ("system", "passport_ad_status", "OFF"),
        ("global", "private_dns_mode", "hostname"),
        ("global", "private_dns_specifier", "dns.adguard-dns.com"),
    ):
        ok, detail = settings_put(ns, key, value)
        print(f"  [{'ok' if ok else 'warn'}] {ns}/{key}={value}" + ("" if ok else f" ({detail})"))
        log.write(f"ads-off {ns}/{key}={value} -> {detail}")

    print()
    print("If a site or app breaks: Settings → Connection & sharing → Private DNS → Automatic.")


def enhance(log: Logger) -> None:
    print_header("Enhancements (safe, reversible)")
    tweaks = [
        ("global", "window_animation_scale", "0.5", "Slightly faster window animation"),
        ("global", "transition_animation_scale", "0.5", "Slightly faster transitions"),
        ("global", "animator_duration_scale", "0.5", "Slightly faster UI motion"),
        ("global", "wifi_scan_always_enabled", "0", "Stop background Wi-Fi scanning"),
        ("global", "ble_scan_always_enabled", "0", "Stop background Bluetooth scanning"),
        ("system", "peak_refresh_rate", "90", "Allow 90 Hz if the panel supports it"),
    ]
    for ns, key, value, note in tweaks:
        ok, detail = settings_put(ns, key, value)
        mark = "ok" if ok else "warn"
        print(f"  [{mark}] {note}")
        print(f"         {ns}/{key}={value}" + ("" if ok else f"  ({detail})"))
        log.write(f"enhance {ns}/{key}={value} -> {detail}")

    print()
    print("To undo animations later:")
    print("  adb shell settings put global window_animation_scale 1")
    print("  adb shell settings put global transition_animation_scale 1")
    print("  adb shell settings put global animator_duration_scale 1")


def undo_session(log: Logger) -> None:
    print_header("Undo last debloat session")
    if not SESSION_RESTORE.exists():
        print("No session undo file found. Nothing to restore from this toolkit.")
        print("You can still run [2] to restore Face / Fingerprint,")
        print("or enable a package by name:  adb shell pm enable --user 0 <package>")
        return

    lines = SESSION_RESTORE.read_text(encoding="utf-8").splitlines()
    if not lines:
        print("Undo file is empty.")
        return

    ok = 0
    fail = 0
    for line in lines:
        if not line.strip() or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        action, package = parts
        if action == "enable":
            status, detail = enable_package(package)
        else:
            result = shell(f"cmd package install-existing {package}")
            out = ((result.stdout or "") + (result.stderr or "")).strip()
            status = "restored" if result.returncode == 0 else "failed"
            detail = out
        log.write(f"undo {package} -> {status} {detail}")
        if status in {"restored", "enabled"}:
            print(f"  [ok]   {package}")
            ok += 1
        else:
            print(f"  [fail] {package}: {detail}")
            fail += 1

    print(f"\nRestored {ok}, failed {fail}.")
    SESSION_RESTORE.rename(
        LOGS / f"restored-{dt.datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
    )


def require_device() -> None:
    devices = connected_devices()
    if not devices:
        raise AdbError(
            "No phone in ADB device mode.\n"
            "1. Unlock the phone\n"
            "2. Settings → Additional settings → Developer options\n"
            "3. Enable USB debugging AND USB debugging (Security settings)\n"
            "4. Plug in USB, tap Allow on the RSA prompt\n"
            "5. Run: adb devices   (must say 'device', not 'unauthorized')"
        )
    if len(devices) > 1:
        print(f"Multiple devices: {', '.join(devices)}. Using the first.")


def confirm(prompt: str) -> bool:
    if not sys.stdin.isatty():
        return True
    answer = input(f"{prompt} [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def menu_loop(log: Logger) -> None:
    while True:
        print_header("Redmi 10 (2022) ADB toolkit")
        try:
            require_device()
            show_device(device_info())
        except AdbError as exc:
            print(str(exc))
            print("You can still quit, or plug the phone in and pick an action.")
        print()
        print("  [1] Diagnose (read-only — start here)")
        print("  [2] Restore Face Unlock + Fingerprint")
        print("  [3] Debloat ads + unused apps (reversible)")
        print("  [4] Enhancements (faster UI, less background scanning)")
        print("  [5] Undo the last debloat from this toolkit")
        print("  [6] Recommended: restore biometrics + ads debloat + enhance")
        print("  [7] Restore ALL currently disabled packages")
        print("  [8] The Chess Lv.100 — freeze Xiaomi ads, protect the game")
        print("  [9] No ads — Xiaomi ads off + Private DNS ad block")
        print("  [0] Quit")
        print()
        choice = input("Choose: ").strip() if sys.stdin.isatty() else "0"

        if choice == "1":
            require_device()
            diagnose(log)
        elif choice == "2":
            require_device()
            if confirm("Re-enable Face Unlock and Fingerprint packages?"):
                restore_biometrics(log, restore_all_disabled=False)
        elif choice == "3":
            require_device()
            if confirm("Freeze ads/analytics and unused preinstalled apps?"):
                debloat(log, include_apps=True)
        elif choice == "4":
            require_device()
            if confirm("Apply UI / battery enhancements?"):
                enhance(log)
        elif choice == "5":
            require_device()
            if confirm("Undo packages this toolkit froze?"):
                undo_session(log)
        elif choice == "6":
            require_device()
            if confirm("Restore biometrics, freeze ads+unused apps, then enhance?"):
                restore_biometrics(log, restore_all_disabled=False)
                debloat(log, include_apps=True)
                enhance(log)
        elif choice == "7":
            require_device()
            print("This re-enables every disabled package, not only biometrics.")
            if confirm("Restore ALL disabled packages?"):
                restore_biometrics(log, restore_all_disabled=True)
        elif choice == "8":
            require_device()
            if confirm("Freeze Xiaomi ads and protect The Chess Lv.100?"):
                chess_clean(log)
        elif choice == "9":
            require_device()
            if confirm("Turn off Xiaomi ads and enable Private DNS ad blocking?"):
                ads_off(log)
        elif choice == "0":
            print("Done. Unplug the phone when you are finished.")
            return
        else:
            print("Unknown choice.")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Redmi 10 (2022) ADB toolkit — restore Face Unlock, debloat, enhance."
    )
    parser.add_argument(
        "action",
        nargs="?",
        choices=[
            "menu",
            "diagnose",
            "restore",
            "debloat",
            "enhance",
            "undo",
            "recommended",
            "chess",
            "ads-off",
        ],
        default="menu",
        help="Command to run (default: interactive menu)",
    )
    parser.add_argument(
        "--ads-only",
        action="store_true",
        help="With debloat: freeze ads/analytics only, keep unused Xiaomi apps",
    )
    parser.add_argument(
        "--all-disabled",
        action="store_true",
        help="With restore: also re-enable every currently disabled package",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    log_path = ensure_logs()
    log = Logger(log_path)
    log.write(f"start action={args.action}")
    print(f"Log: {log_path}")

    try:
        print(adb_ok())
        if args.action == "menu":
            menu_loop(log)
            return 0

        require_device()
        if args.action == "diagnose":
            diagnose(log)
        elif args.action == "restore":
            restore_biometrics(log, restore_all_disabled=args.all_disabled)
        elif args.action == "debloat":
            debloat(log, include_apps=not args.ads_only)
        elif args.action == "enhance":
            enhance(log)
        elif args.action == "undo":
            undo_session(log)
        elif args.action == "recommended":
            restore_biometrics(log, restore_all_disabled=False)
            debloat(log, include_apps=True)
            enhance(log)
        elif args.action == "chess":
            chess_clean(log)
        elif args.action == "ads-off":
            ads_off(log)
        return 0
    except AdbError as exc:
        print(f"\nError: {exc}", file=sys.stderr)
        log.write(f"error {exc}")
        return 2
    except subprocess.TimeoutExpired:
        print("\nError: adb timed out. Unplug/replug the phone and try again.", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())

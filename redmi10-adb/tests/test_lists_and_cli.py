#!/usr/bin/env python3
"""Offline checks: package lists stay safe, CLI parses, helpers stay consistent."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import redmi10  # noqa: E402


def _pkgs(name: str) -> set[str]:
    return set(redmi10.load_list(name))


class ListSafetyTests(unittest.TestCase):
    def test_lists_are_nonempty(self) -> None:
        self.assertGreater(len(_pkgs("never-touch.txt")), 10)
        self.assertIn("com.miui.face", _pkgs("restore-biometrics.txt"))
        self.assertIn("com.miui.msa.global", _pkgs("debloat-ads.txt"))
        self.assertIn("com.mi.globalbrowser", _pkgs("debloat-apps.txt"))

    def test_debloat_never_includes_protected(self) -> None:
        protected = _pkgs("never-touch.txt")
        frozen = _pkgs("debloat-ads.txt") | _pkgs("debloat-apps.txt")
        overlap = protected & frozen
        self.assertFalse(overlap, f"debloat list includes protected packages: {overlap}")

    def test_debloat_never_includes_face_unlock(self) -> None:
        frozen = _pkgs("debloat-ads.txt") | _pkgs("debloat-apps.txt")
        self.assertNotIn("com.miui.face", frozen)
        self.assertNotIn("com.android.facelock", frozen)

    def test_biometric_restore_not_in_never_touch(self) -> None:
        overlap = _pkgs("never-touch.txt") & _pkgs("restore-biometrics.txt")
        self.assertFalse(overlap, f"cannot restore packages marked never-touch: {overlap}")

    def test_finddevice_is_protected(self) -> None:
        self.assertIn("com.xiaomi.finddevice", _pkgs("never-touch.txt"))
        self.assertIn("com.miui.securitycenter", _pkgs("never-touch.txt"))

    def test_no_duplicate_packages_inside_a_list(self) -> None:
        for name in (
            "never-touch.txt",
            "restore-biometrics.txt",
            "debloat-ads.txt",
            "debloat-apps.txt",
        ):
            items = redmi10.load_list(name)
            self.assertEqual(len(items), len(set(items)), f"duplicates in {name}")

    def test_package_names_look_valid(self) -> None:
        for name in (
            "never-touch.txt",
            "restore-biometrics.txt",
            "debloat-ads.txt",
            "debloat-apps.txt",
        ):
            for pkg in redmi10.load_list(name):
                self.assertRegex(pkg, r"^[A-Za-z0-9_.]+$", f"bad package id {pkg} in {name}")


class HelperTests(unittest.TestCase):
    def test_biometric_regex_catches_face_and_fp(self) -> None:
        self.assertTrue(redmi10.BIOMETRIC_RE.search("com.miui.face"))
        self.assertTrue(redmi10.BIOMETRIC_RE.search("com.goodix.fingerprint"))
        self.assertTrue(redmi10.BIOMETRIC_RE.search("com.xiaomi.fidoauth"))
        self.assertFalse(redmi10.BIOMETRIC_RE.search("com.miui.msa.global"))

    def test_cli_defaults_to_menu(self) -> None:
        args = redmi10.parse_args([])
        self.assertEqual(args.action, "menu")
        self.assertFalse(args.ads_only)

    def test_cli_recommended_and_ads_only(self) -> None:
        args = redmi10.parse_args(["debloat", "--ads-only"])
        self.assertEqual(args.action, "debloat")
        self.assertTrue(args.ads_only)
        restore = redmi10.parse_args(["restore", "--all-disabled"])
        self.assertTrue(restore.all_disabled)

    def test_disable_blocks_protected_without_adb(self) -> None:
        status, detail = redmi10.disable_package("com.xiaomi.finddevice")
        self.assertEqual(status, "blocked")
        self.assertIn("protected", detail)

    def test_disable_blocks_biometric_name_without_adb(self) -> None:
        status, detail = redmi10.disable_package("com.miui.face")
        self.assertEqual(status, "blocked")
        self.assertIn("biometric", detail.lower())


class WindowsCmdTests(unittest.TestCase):
    def test_cmd_embeds_biometric_and_debloat_lists(self) -> None:
        cmd = (ROOT / "redmi10.cmd").read_text(encoding="utf-8", errors="replace")
        for pkg in _pkgs("restore-biometrics.txt") | _pkgs("debloat-ads.txt") | _pkgs(
            "debloat-apps.txt"
        ):
            self.assertIn(pkg, cmd, f"{pkg} missing from redmi10.cmd")

    def test_cmd_includes_chess_lv100(self) -> None:
        cmd = (ROOT / "redmi10.cmd").read_text(encoding="utf-8", errors="replace")
        self.assertIn("jp.co.unbalance.android.chessunbcc", cmd)
        self.assertIn("do_chess", cmd)
        self.assertIn("jp.co.unbalance.android.chessunbcc", _pkgs("keep-apps.txt"))

    def test_cmd_has_no_python_dependency(self) -> None:
        cmd = (ROOT / "redmi10.cmd").read_text(encoding="utf-8", errors="replace")
        lowered = cmd.lower()
        self.assertNotIn("python3", lowered)
        self.assertNotIn("python.exe", lowered)
        self.assertNotIn("py -3", lowered)
        self.assertIn("adb.exe", cmd)


if __name__ == "__main__":
    unittest.main()

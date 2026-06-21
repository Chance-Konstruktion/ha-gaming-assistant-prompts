from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def run_script(script: str, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(REPO_ROOT / script), *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


class GenerateManifestTests(unittest.TestCase):
    def test_check_fails_when_manifest_is_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs" / "base").mkdir(parents=True)
            pack = cwd / "packs" / "base" / "sample_game.json"
            pack.write_text('{"language":"de"}\n', encoding="utf-8")
            (cwd / "packs" / "_template.json").write_text("{}\n", encoding="utf-8")
            (cwd / "checksums.json").write_text("{}\n", encoding="utf-8")

            result = run_script("scripts/generate_manifest.py", "--check", cwd=cwd)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("checksums.json is stale", result.stdout)

    def test_writes_manifest_for_downloadable_packs_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs" / "base").mkdir(parents=True)
            pack = cwd / "packs" / "base" / "sample_game.json"
            pack_content = '{"language":"de"}\n'
            pack.write_text(pack_content, encoding="utf-8")
            (cwd / "packs" / "_template.json").write_text('{"language":"de"}\n', encoding="utf-8")

            result = run_script("scripts/generate_manifest.py", cwd=cwd)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads((cwd / "checksums.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["algorithm"], "sha256")
            self.assertEqual(
                manifest["packs"],
                {"base/sample_game.json": hashlib.sha256(pack_content.encode("utf-8")).hexdigest()},
            )


class ValidatePacksTests(unittest.TestCase):
    def test_strict_mode_fails_on_missing_language(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs").mkdir()
            (cwd / "packs" / "sample_game.json").write_text('{"system_prompt":"Hallo"}\n', encoding="utf-8")

            result = run_script("scripts/validate_packs.py", "--strict", cwd=cwd)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("missing 'language' field", result.stdout)

    def test_default_mode_allows_json_warnings_but_fails_naming_violations(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs").mkdir()
            (cwd / "packs" / "Bad-Name.json").write_text('{"language":"de"}\n', encoding="utf-8")
            (cwd / "packs" / "broken_json.json").write_text('{"language":', encoding="utf-8")

            result = run_script("scripts/validate_packs.py", cwd=cwd)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("Naming violations", result.stdout)
            self.assertIn("Bad-Name.json", result.stdout)
            self.assertIn("JSON parse issues", result.stdout)


class QaPacksTests(unittest.TestCase):
    def test_warn_only_findings_do_not_fail_default_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs").mkdir()
            prompt = (
                "You are the expert coach and you help the player with this route "
                "because they should understand what to do next."
            )
            (cwd / "packs" / "english_prompt.json").write_text(
                json.dumps({"language": "de", "system_prompt": prompt}),
                encoding="utf-8",
            )

            result = run_script("scripts/qa_packs.py", cwd=cwd)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("ERROR: 0", result.stdout)
            self.assertIn("WARN: 1", result.stdout)
            self.assertIn("reads as untranslated English", result.stdout)

    def test_errors_fail_and_report_groups_findings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            (cwd / "packs").mkdir()
            (cwd / "packs" / "template_leftover.json").write_text(
                json.dumps({"language": "de", "system_prompt": "Describe your expertise"}),
                encoding="utf-8",
            )
            report = cwd / "qa-report.md"

            result = run_script("scripts/qa_packs.py", "--report", str(report), cwd=cwd)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("## Errors", report.read_text(encoding="utf-8"))
            self.assertIn("template_leftover.json", report.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

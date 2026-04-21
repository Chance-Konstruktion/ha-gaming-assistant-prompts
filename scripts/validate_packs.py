#!/usr/bin/env python3
"""Validate prompt pack filenames and JSON quality.

Default mode enforces naming consistency and reports JSON/encoding issues as warnings.
Use --strict to fail on encoding/JSON issues too.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PACKS_DIR = Path("packs")
JSON_EXT = ".json"
NAME_RE = re.compile(r"^[a-z0-9_]+(?:\.[a-z0-9_]+)?\.json$")


def iter_json_files(root: Path):
    for path in sorted(root.rglob(f"*{JSON_EXT}")):
        if path.is_file():
            yield path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate pack filenames, encoding and JSON parseability.")
    parser.add_argument("--strict", action="store_true", help="Fail when UTF-8 decoding or JSON parsing fails.")
    args = parser.parse_args()

    if not PACKS_DIR.exists():
        print("❌ packs/ directory not found")
        return 2

    naming_errors: list[str] = []
    encoding_errors: list[str] = []
    json_errors: list[str] = []

    files = list(iter_json_files(PACKS_DIR))
    for path in files:
        rel = path.as_posix()
        fname = path.name

        if not NAME_RE.match(fname) or fname.startswith("pc_") or "-" in fname or any(c.isupper() for c in fname):
            naming_errors.append(rel)

        raw = path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            encoding_errors.append(f"{rel}: {exc}")
            continue

        try:
            json.loads(text)
        except json.JSONDecodeError as exc:
            json_errors.append(f"{rel}: line {exc.lineno}, col {exc.colno} ({exc.msg})")

    print(f"Scanned {len(files)} JSON files under packs/.")

    if naming_errors:
        print("\n❌ Naming violations:")
        for err in naming_errors:
            print(f"  - {err}")
    else:
        print("✅ Naming convention check passed.")

    if encoding_errors:
        print("\n⚠️ UTF-8 decoding issues:")
        for err in encoding_errors:
            print(f"  - {err}")

    if json_errors:
        print("\n⚠️ JSON parse issues:")
        for err in json_errors:
            print(f"  - {err}")

    if naming_errors:
        return 1

    if args.strict and (encoding_errors or json_errors):
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

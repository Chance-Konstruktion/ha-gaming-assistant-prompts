#!/usr/bin/env python3
"""Generate checksums.json: the SHA-256 of every downloadable pack.

The Home Assistant integration verifies each downloaded pack against this
manifest before writing it to its cache, so the manifest MUST be regenerated
whenever a pack changes. CI runs this with ``--check`` to fail the build if the
committed manifest is stale.

The set of hashed files mirrors what the integration actually downloads:
``packs/**/*.json`` excluding files whose name starts with ``_`` (e.g. the
``_template.json`` skeleton).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

PACKS_DIR = Path("packs")
OUT = Path("checksums.json")


def build() -> dict:
    packs: dict[str, str] = {}
    for path in sorted(PACKS_DIR.rglob("*.json")):
        if not path.is_file() or path.name.startswith("_"):
            continue
        rel = path.relative_to(PACKS_DIR).as_posix()
        packs[rel] = hashlib.sha256(path.read_bytes()).hexdigest()
    return {"algorithm": "sha256", "packs": packs}


def main() -> int:
    manifest = build()
    text = json.dumps(manifest, indent=2, ensure_ascii=False) + "\n"
    if "--check" in sys.argv:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        if current != text:
            print("❌ checksums.json is stale — run: python3 scripts/generate_manifest.py")
            return 1
        print("✅ checksums.json is up to date.")
        return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"Wrote {OUT} ({len(manifest['packs'])} pack hashes).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Quality-assurance checks for the (machine-translated) German prompt packs.

`validate_packs.py` proves a pack is *well-formed* (naming, encoding, JSON,
language declaration). This script asks a different question: is the German
*content* actually any good, or did the machine translation leave holes?

It targets the realistic failure modes of a bulk auto-translation:

  ERROR (high confidence, fails CI):
    - a required prose field is missing, empty, or stub-short
    - leftover translation/template scaffolding ("Your Game", "Describe your
      expertise", "Game knowledge (base):" ...)
    - object keys with stray leading/trailing whitespace

  WARN (needs a human eye, advisory):
    - a prose field that reads as predominantly *English* — i.e. the machine
      translation skipped it entirely (decided by an English-vs-German
      function-word ratio, so a stray English game term does not trip it)

Run:  python3 scripts/qa_packs.py [--strict] [--report out.md]
  --strict  also fail on WARN findings
  --report  additionally write a grouped Markdown report to the given path
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

PACKS_DIR = Path("packs")

# Fields whose string values are legitimately non-German or non-prose: game
# names, ids, enum levels, platform tags, dates, machine-readable schema hints.
# Their contents are never checked for "English-ness".
NON_PROSE_KEYS = {
    "id", "name", "language", "keywords", "type", "platforms", "version",
    "source_version", "created", "last_updated", "patch_note", "tool", "tools",
    "sources", "source_verification", "url", "downloads", "state_schema",
    "spoiler_defaults", "trophies", "achievements",
}

# A required prose field this short is a stub, not a translated coaching prompt.
MIN_SYSTEM_PROMPT_LEN = 40

# Scaffolding that should never survive into a shipped pack.
TEMPLATE_MARKERS = (
    "your game name", "your_game_id", "your game id", "describe your expertise",
    "any extra context", "helps the ai", "game knowledge (", "alternate name",
    "you are an expert coach for your",
)

# High-precision English function words: tokens that essentially never appear as
# standalone words in German prose. Deliberately excludes German homographs
# ("will", "war", "also", "man", "in", "die", "der", "rast" ...).
ENGLISH_TOKENS = {
    "the", "you", "your", "youre", "are", "with", "this", "that", "and", "for",
    "have", "has", "they", "their", "what", "when", "where", "which", "while",
    "there", "about", "into", "from", "been", "being", "would", "could",
    "should", "because", "through", "only", "very", "most", "some", "each",
    "both", "here", "make", "such", "well", "help", "helps", "describe",
    "expert", "expertise", "understand", "including", "knowledge", "player",
}

# German function words used to confirm a string really is German prose.
GERMAN_TOKENS = {
    "der", "die", "das", "und", "ist", "ein", "eine", "einen", "einem", "einer",
    "für", "mit", "von", "den", "dem", "des", "im", "zu", "auf", "sich", "nicht",
    "auch", "oder", "als", "wie", "du", "dein", "deine", "deinen", "bei", "aus",
    "nach", "über", "durch", "kann", "sind", "werden", "haben", "hat", "wird",
    "beim", "zum", "zur", "vom", "spielst", "achte", "nutze", "verwende",
}

_TOKEN_RE = re.compile(r"[A-Za-z']+")


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN_RE.findall(text)]


def classify_language(text: str) -> tuple[str, set[str], set[str]]:
    """Return ('english'|'german'|'mixed', english_hits, german_hits).

    'english' means the string reads as untranslated English prose: clearly more
    English than German function words, with enough English signal to be sure.
    """
    toks = _tokens(text)
    en = {t for t in toks if t in ENGLISH_TOKENS}
    de = {t for t in toks if t in GERMAN_TOKENS}
    if len(en) >= 3 and len(en) > len(de):
        return "english", en, de
    if len(en) >= 2 and not de:
        return "english", en, de
    if de:
        return "german", en, de
    return "mixed", en, de


class Finding:
    __slots__ = ("level", "pack", "field", "detail")

    def __init__(self, level: str, pack: str, field: str, detail: str):
        self.level = level
        self.pack = pack
        self.field = field
        self.detail = detail


def _check_string(pack: str, key: str, value: str, out: list[Finding]) -> None:
    if key in NON_PROSE_KEYS:
        return
    low = value.lower()
    for marker in TEMPLATE_MARKERS:
        if marker in low:
            out.append(Finding(
                "ERROR", pack, key, f"leftover template/translation scaffolding: {marker!r}"
            ))
            break
    kind, en, _de = classify_language(value)
    if kind == "english":
        snippet = re.sub(r"\s+", " ", value).strip()[:90]
        out.append(Finding(
            "WARN", pack, key,
            f"reads as untranslated English ({sorted(en)[:6]}): {snippet!r}",
        ))


def _walk(pack: str, obj, out: list[Finding], key: str | None = None) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(k, str) and k != k.strip():
                out.append(Finding(
                    "ERROR", pack, repr(k), "object key has leading/trailing whitespace"
                ))
            _walk(pack, v, out, k)
    elif isinstance(obj, list):
        for v in obj:
            _walk(pack, v, out, key)
    elif isinstance(obj, str) and key is not None:
        _check_string(pack, key, obj, out)


def check_pack(path: Path) -> list[Finding]:
    pack = path.name
    out: list[Finding] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        return [Finding("ERROR", pack, "<file>", f"unreadable: {exc}")]
    if not isinstance(data, dict):
        return [Finding("ERROR", pack, "<file>", "top level is not a JSON object")]

    sp = data.get("system_prompt")
    if not isinstance(sp, str) or not sp.strip():
        out.append(Finding("ERROR", pack, "system_prompt", "missing or empty"))
    elif len(sp.strip()) < MIN_SYSTEM_PROMPT_LEN:
        out.append(Finding(
            "ERROR", pack, "system_prompt",
            f"stub-short ({len(sp.strip())} chars < {MIN_SYSTEM_PROMPT_LEN})",
        ))

    _walk(pack, data, out)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Fail on WARN findings too.")
    parser.add_argument("--report", type=Path, help="Write a Markdown report to this path.")
    args = parser.parse_args()

    if not PACKS_DIR.exists():
        print("❌ packs/ directory not found")
        return 2

    findings: list[Finding] = []
    n = 0
    for path in sorted(PACKS_DIR.rglob("*.json")):
        if path.name == "_template.json":
            continue
        n += 1
        findings.extend(check_pack(path))

    errors = [f for f in findings if f.level == "ERROR"]
    warns = [f for f in findings if f.level == "WARN"]

    print(f"Checked {n} packs.")
    print(f"  ERROR: {len(errors)}   WARN: {len(warns)}\n")

    for level, group in (("ERROR", errors), ("WARN", warns)):
        if not group:
            continue
        icon = "❌" if level == "ERROR" else "⚠️"
        print(f"{icon} {level} ({len(group)}):")
        for f in sorted(group, key=lambda x: (x.pack, x.field)):
            print(f"  {f.pack} [{f.field}] {f.detail}")
        print()

    if not errors and not warns:
        print("✅ All packs passed content QA.")

    if args.report:
        _write_report(args.report, n, errors, warns)
        print(f"Report written to {args.report}")

    if errors:
        return 1
    if args.strict and warns:
        return 1
    return 0


def _write_report(path: Path, n: int, errors: list[Finding], warns: list[Finding]) -> None:
    lines = [
        "# Prompt pack content QA report",
        "",
        f"Checked **{n}** packs — **{len(errors)}** errors, **{len(warns)}** warnings.",
        "",
        "_Auto-generated by `scripts/qa_packs.py`. Errors fail CI; warnings are advisory._",
        "",
        "Warnings flag prose that reads as untranslated English. The remaining ones",
        "are almost all the embedded `additional_context` *knowledge blobs*: serialized",
        "structured data whose English content is mostly official proper nouns (quest,",
        "achievement and item names that should stay English). Translating those needs a",
        "human eye per pack, so they are tracked here rather than auto-rewritten.",
        "",
    ]
    for level, group in (("Errors", errors), ("Warnings (review)", warns)):
        lines.append(f"## {level} ({len(group)})")
        lines.append("")
        if not group:
            lines.append("_None._\n")
            continue
        lines.append("| Pack | Field | Detail |")
        lines.append("| --- | --- | --- |")
        for f in sorted(group, key=lambda x: (x.pack, x.field)):
            detail = f.detail.replace("|", "\\|")
            lines.append(f"| `{f.pack}` | `{f.field}` | {detail} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())

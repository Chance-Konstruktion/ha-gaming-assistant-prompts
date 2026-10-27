"""Regression tests for prompt-pack content QA tokenization."""

import importlib.util
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("qa_packs", REPO_ROOT / "scripts" / "qa_packs.py")
assert SPEC is not None and SPEC.loader is not None
qa_packs = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(qa_packs)


class TestUnicodeAwareTokenization(unittest.TestCase):
    def test_german_umlauts_are_preserved_for_language_classification(self):
        kind, english_hits, german_hits = qa_packs.classify_language("für über")

        self.assertEqual(kind, "german")
        self.assertEqual(english_hits, set())
        self.assertEqual(german_hits, {"für", "über"})

    def test_english_contractions_match_normalized_function_words(self):
        self.assertEqual(
            qa_packs._tokens("You're ready — you’re not alone."),
            ["youre", "ready", "youre", "not", "alone"],
        )


if __name__ == "__main__":
    unittest.main()

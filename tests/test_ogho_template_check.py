"""Regression tests for the OGHO template heading parser."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


CHECK_PATH = (
    Path(__file__).parents[1]
    / ".github"
    / "actions"
    / "ogho-template-check"
    / "check.py"
)
SPEC = importlib.util.spec_from_file_location("ogho_template_check", CHECK_PATH)
assert SPEC is not None and SPEC.loader is not None
CHECK = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK
SPEC.loader.exec_module(CHECK)


class NormalizeHeadingTests(unittest.TestCase):
    def test_leading_emoji_is_ignored(self) -> None:
        self.assertEqual(CHECK.normalize_heading("📦 Installation"), "installation")

    def test_emoji_with_variation_selector_is_ignored(self) -> None:
        self.assertEqual(CHECK.normalize_heading("⚙️ Documentation"), "documentation")

    def test_documentation_heading_can_include_additional_text(self) -> None:
        headings = {CHECK.normalize_heading("📚 Documentation & Resources")}
        self.assertTrue(
            CHECK.has_readme_section("Documentation", frozenset(("documentation",)), headings)
        )

    def test_examples_heading_can_include_additional_text(self) -> None:
        headings = {CHECK.normalize_heading("📘 Examples and notebooks")}
        self.assertTrue(CHECK.has_readme_section("Examples", frozenset(("examples",)), headings))

    def test_security_ignores_trailing_whitespace(self) -> None:
        canonical = b"# Security\n"
        self.assertTrue(CHECK.matches_canonical_security(b"# Security", canonical))
        self.assertTrue(CHECK.matches_canonical_security(b"# Security\r\n\t \f\v", canonical))
        self.assertFalse(CHECK.matches_canonical_security(b"# security", canonical))
        self.assertFalse(CHECK.matches_canonical_security(b"#  Security", canonical))

    def test_non_matching_heading_remains_non_matching(self) -> None:
        self.assertEqual(CHECK.normalize_heading("📚 Documentation & Resources"), "documentation & resources")


if __name__ == "__main__":
    unittest.main()

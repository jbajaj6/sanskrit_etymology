from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sanskrit_etymology.demo import build_demo_terms
from sanskrit_etymology.repository import load_demo_bundle, load_repository
from sanskrit_etymology.validation import validate_repository


class PipelineTestCase(unittest.TestCase):
    def test_repository_validates_without_errors(self) -> None:
        repo = load_repository()
        issues = validate_repository(repo)
        errors = [issue for issue in issues if issue.severity == "error"]
        self.assertEqual(errors, [])

    def test_demo_build_matches_seed_catalog(self) -> None:
        """The explorer is the bundle plus any term a canonical analysis covers."""
        repo = load_repository()
        demo_terms = build_demo_terms(repo)
        bundle_ids = {str(entry["id"]) for entry in load_demo_bundle()}
        analysis_ids = {analysis.id for analysis in repo.analyses}
        self.assertEqual({term.id for term in demo_terms}, bundle_ids | analysis_ids)
        # Every mapping in the canonical file should reach the explorer.
        mapped_slugs = {mapping.normalized_slug for mapping in repo.mappings}
        shown = {
            term.id
            for term in demo_terms
            if term.chinese_counterparts
        }
        self.assertEqual(len(shown), len(mapped_slugs))
        demo_ids = {term.id for term in demo_terms}
        self.assertTrue({"samadhi", "karma", "ahimsa", "viveka"}.issubset(demo_ids))
        self.assertTrue({"atman", "brahman", "turiya", "upanisad"}.issubset(demo_ids))

    def test_demo_audit_normalizes_known_edge_cases(self) -> None:
        repo = load_repository()
        demo_by_id = {term.id: term for term in build_demo_terms(repo)}

        self.assertEqual(
            demo_by_id["drashta"].segmentation,
            "√dṛś + -tṛ → nominative singular draṣṭā",
        )
        self.assertEqual(
            demo_by_id["svadhyaya"].segmentation,
            "sva + adhyāya",
        )
        self.assertEqual(
            demo_by_id["vyadhi"].segmentation,
            "vi + ā + √dhā + -i",
        )
        self.assertEqual(
            demo_by_id["purusa"].segmentation,
            "puruṣa (lexical noun; etymology disputed)",
        )
        self.assertIn("practice", demo_by_id["abhyasa"].literal_gloss)
        self.assertEqual(demo_by_id["nidra"].confidence, "medium")


if __name__ == "__main__":
    unittest.main()

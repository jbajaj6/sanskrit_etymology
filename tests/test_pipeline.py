from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sanskrit_etymology.demo import build_demo_terms
from sanskrit_etymology.repository import load_repository
from sanskrit_etymology.validation import validate_repository


class PipelineTestCase(unittest.TestCase):
    def test_repository_validates_without_errors(self) -> None:
        repo = load_repository()
        issues = validate_repository(repo)
        errors = [issue for issue in issues if issue.severity == "error"]
        self.assertEqual(errors, [])

    def test_demo_build_matches_seed_catalog(self) -> None:
        repo = load_repository()
        demo_terms = build_demo_terms(repo)
        self.assertEqual(len(demo_terms), 84)
        self.assertEqual(sum(1 for term in demo_terms if term.chinese_counterparts), 9)
        demo_ids = {term.id for term in demo_terms}
        self.assertTrue({"samadhi", "karma", "ahimsa", "viveka"}.issubset(demo_ids))


if __name__ == "__main__":
    unittest.main()

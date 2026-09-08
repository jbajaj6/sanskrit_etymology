"""Guards on the cross-references between terms.

A wrong link is worse than a missing one: it asserts a relationship between two
Sanskrit words that a reader will take on trust. These tests check that every
link can be traced back to something actually declared in the data.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sanskrit_etymology.demo import build_demo_terms
from sanskrit_etymology.relations import EXCLUDED_PAIRS, MAX_GROUP
from sanskrit_etymology.repository import load_repository


class RelationsTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.terms = build_demo_terms(load_repository())
        cls.by_id = {term.id: term for term in cls.terms}

    def _declares(self, term_id: str, kind: str, morpheme: str) -> bool:
        term = self.by_id[term_id]
        field, key = {
            "root": ("roots", "root"),
            "prefix": ("prefixes", "prefix"),
            "suffix": ("suffixes", "suffix"),
        }[kind]
        return any(
            str(component.get(key, "")).strip() == morpheme
            for component in getattr(term, field) or []
        )

    def test_every_morpheme_link_is_declared_by_both_terms(self) -> None:
        """The stated basis must be true of both ends, or the link is a fiction."""
        for term in self.terms:
            for group in term.related_morphemes:
                self.assertTrue(
                    self._declares(term.id, group["kind"], group["morpheme"]),
                    f"{term.id} does not declare {group['kind']} {group['morpheme']}",
                )
                for other in group["terms"]:
                    self.assertTrue(
                        self._declares(other["id"], group["kind"], group["morpheme"]),
                        f"{other['id']} does not declare {group['kind']} {group['morpheme']}",
                    )

    def test_morpheme_links_are_mutual(self) -> None:
        for term in self.terms:
            for group in term.related_morphemes:
                for other in group["terms"]:
                    back = self.by_id[other["id"]].related_morphemes
                    self.assertTrue(
                        any(
                            g["morpheme"] == group["morpheme"]
                            and any(x["id"] == term.id for x in g["terms"])
                            for g in back
                        ),
                        f"{term.id} links {other['id']} on {group['morpheme']} "
                        "but not the reverse",
                    )

    def test_no_term_links_to_itself(self) -> None:
        for term in self.terms:
            linked = [ref["id"] for group in term.related_morphemes for ref in group["terms"]]
            linked += [ref["id"] for ref in term.related_mentions]
            self.assertNotIn(term.id, linked, f"{term.id} links to itself")

    def test_links_point_at_real_terms(self) -> None:
        ids = set(self.by_id)
        for term in self.terms:
            refs = [ref for group in term.related_morphemes for ref in group["terms"]]
            refs += list(term.related_mentions)
            for ref in refs:
                self.assertIn(ref["id"], ids, f"{term.id} links to unknown {ref['id']}")
                self.assertEqual(ref["transliteration"], self.by_id[ref["id"]].transliteration)

    def test_generic_morphemes_do_not_become_families(self) -> None:
        """The bare "-a" suffix covers a quarter of the corpus and means nothing."""
        for term in self.terms:
            for group in term.related_morphemes:
                self.assertLessEqual(
                    len(group["terms"]) + 1,
                    MAX_GROUP,
                    f"{group['morpheme']} links too many terms to be informative",
                )

    def test_known_families_are_connected(self) -> None:
        """The pairs a reader would expect, including the one that prompted this."""
        def linked(a: str, b: str) -> bool:
            term = self.by_id[a]
            in_morph = any(
                ref["id"] == b for group in term.related_morphemes for ref in group["terms"]
            )
            return in_morph or any(ref["id"] == b for ref in term.related_mentions)

        self.assertTrue(linked("nididhyasana", "dhyana"), "nididhyasana should reach dhyana")
        self.assertTrue(linked("dhyana", "nididhyasana"))
        self.assertTrue(linked("vidya", "avidya"))
        self.assertTrue(linked("acarya", "guru"))
        self.assertTrue(linked("samyama", "yama"))

    def test_links_are_never_justified_by_name_containment(self) -> None:
        """The trap this module exists to avoid.

        Substring matching would read "nididhyasana" as containing "asana" and
        assert a derivation. Sharing the -ana suffix is a real link and is
        allowed; claiming a shared root or stem is not. A term that declares no
        morphemes at all must therefore pick up no structural link, however much
        its name appears inside another's.
        """
        for isolated in ("loka", "neti_neti", "atha"):
            term = self.by_id[isolated]
            self.assertEqual(
                term.related_morphemes,
                [],
                f"{isolated} declares no morphemes and must have no structural link",
            )

        # aloka's name contains loka; that must not become a link.
        aloka = [
            ref["id"] for group in self.by_id["aloka"].related_morphemes for ref in group["terms"]
        ]
        self.assertNotIn("loka", aloka)

        # Any link between these pairs must rest on an affix they share, never a root.
        for source, target in [
            ("nididhyasana", "asana"),
            ("pranava", "prana"),
            ("vasana", "asana"),
        ]:
            for group in self.by_id[source].related_morphemes:
                if any(ref["id"] == target for ref in group["terms"]):
                    self.assertNotEqual(
                        group["kind"],
                        "root",
                        f"{source} and {target} do not share a root",
                    )

    def test_homonyms_are_excluded(self) -> None:
        for source, target in EXCLUDED_PAIRS:
            self.assertFalse(
                any(ref["id"] == target for ref in self.by_id[source].related_mentions),
                f"{source} should not link the homonym {target}",
            )


if __name__ == "__main__":
    unittest.main()

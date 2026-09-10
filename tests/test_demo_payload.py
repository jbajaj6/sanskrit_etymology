"""Guards on what the published explorer actually shows the reader.

The explorer is the public face of the project, so these tests care less about
internal plumbing than about two promises the page makes: every term is
browsable and linkable, and no term claims more sourcing than it has.
"""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from sanskrit_etymology.demo import build_demo_terms, sort_demo_terms
from sanskrit_etymology.repository import load_repository, normalized_slug
from sanskrit_etymology.validation import (
    ALLOWED_THEMATIC_BUCKETS,
    validate_repository,
)


class DemoPayloadTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = load_repository()
        cls.terms = build_demo_terms(cls.repo)
        cls.by_id = {term.id: term for term in cls.terms}

    def test_every_term_is_filterable(self) -> None:
        """The theme filter bar is useless if terms fall outside every bucket."""
        unsorted_ids = [term.id for term in self.terms if not term.thematic_bucket]
        self.assertEqual(unsorted_ids, [], "terms with no thematic bucket")

        for term in self.terms:
            self.assertIn(term.thematic_bucket, ALLOWED_THEMATIC_BUCKETS, term.id)

    def test_every_term_has_a_stable_link_target(self) -> None:
        """Term ids become URL fragments, so they must be unique and url-safe."""
        ids = [term.id for term in self.terms]
        self.assertEqual(len(ids), len(set(ids)), "duplicate term ids")

        for term_id in ids:
            self.assertEqual(
                term_id,
                term_id.strip(),
                f"'{term_id}' has surrounding whitespace",
            )
            self.assertRegex(term_id, r"^[a-z0-9_]+$", f"'{term_id}' is not url-safe")

    def test_verified_terms_carry_their_evidence(self) -> None:
        """A 'source-verified' badge must be backed by a quoted passage."""
        verified = [term for term in self.terms if term.verification == "source-verified"]
        self.assertTrue(verified, "no source-verified terms in the bundle")

        for term in verified:
            self.assertTrue(term.source_context, f"{term.id} verified but has no source")
            self.assertTrue(term.citation_trail, f"{term.id} verified but has no citations")

    def test_unverified_terms_make_no_source_claim(self) -> None:
        """The inverse: an unverified term must not display a quoted passage."""
        for term in self.terms:
            if term.verification == "source-verified":
                continue
            self.assertEqual(term.verification, "unverified", term.id)
            self.assertIsNone(term.source_context, f"{term.id} shows a source it cannot back")
            self.assertEqual(term.citation_trail, [], term.id)

    def test_verification_tracks_the_canonical_analyses(self) -> None:
        analysis_ids = {analysis.id for analysis in self.repo.analyses}
        for term in self.terms:
            expected = "source-verified" if term.id in analysis_ids else "unverified"
            self.assertEqual(term.verification, expected, term.id)

    def test_meaning_search_has_text_to_match_against(self) -> None:
        """Searching by English meaning only works if a gloss is present."""
        for term in self.terms:
            self.assertTrue(term.professor_gloss, f"{term.id} has no professor gloss")
            self.assertTrue(term.literal_gloss, f"{term.id} has no literal gloss")

    def test_every_term_declares_its_source_text(self) -> None:
        """The source filter and the card label both read this field."""
        for term in self.terms:
            self.assertIn(term.source_text, {"yoga_sutras", "upanisads"}, term.id)

    def test_upanisadic_terms_cite_an_upanisad(self) -> None:
        """A term filed under the Upanisads must not carry a Yoga Sutra citation."""
        sigla = ("BṛU", "ChU", "KaU", "MāU", "AiU", "ĪśU", "ŚvU", "PraU", "MuU", "KaivU", "GK")
        upanisadic = [t for t in self.terms if t.source_text == "upanisads"]
        self.assertTrue(upanisadic, "no Upanisadic terms in the bundle")
        for term in upanisadic:
            self.assertFalse(term.chapter.startswith("YS"), term.id)
            self.assertTrue(
                term.chapter.startswith(sigla),
                f"{term.id} chapter '{term.chapter}' names no Upanisad",
            )

    def test_verified_upanisadic_terms_quote_their_source(self) -> None:
        """Guards the claim that these passages were checked, not recalled."""
        for term in self.terms:
            if term.source_text != "upanisads" or term.verification != "source-verified":
                continue
            self.assertTrue(term.source_context, term.id)
            self.assertTrue(
                any("GRETIL" in entry for entry in term.citation_trail),
                f"{term.id} claims verification without naming the corpus",
            )

    def test_every_quoted_passage_carries_a_translation(self) -> None:
        """The card sets Sanskrit and English differently, so both must be present.

        nirodha once stored YS 1.2 with no translation, and the renderer set the
        bare Sanskrit as if it were a full passage.
        """
        cite = re.compile(
            r"(?:YS|B[ṛr]U|ChU|KaivU|KaU|M[āa]U|AiU|[ĪI][śs]U|[ŚS]vU|PraU|MuU|GK)\s*[\d][\d.,\s–-]*(?=:)"
        )
        for term in self.terms:
            if not term.source_context:
                continue
            starts = [m.start() for m in cite.finditer(term.source_context)]
            self.assertTrue(starts, f"{term.id} source_context names no citation")
            bounds = starts + [len(term.source_context)]
            for index in range(len(starts)):
                chunk = term.source_context[bounds[index] : bounds[index + 1]]
                self.assertRegex(
                    chunk,
                    r'\(\s*"',
                    f"{term.id}: passage {chunk[:40]!r} has no quoted translation",
                )

    def test_yoga_sutra_terms_appear_in_the_sutra_they_quote(self) -> None:
        """A quoted passage must actually contain the term it is evidence for.

        Sandhi means the term is usually embedded in a compound and altered at
        the join, so the comparison is on a normalised stem.
        """
        # asamprajnata is the documented exception: the word is Vyasa's, not
        # Patanjali's, and its entry says so in the passage itself.
        exceptions = {"asamprajnata"}

        def normalise(text: str) -> str:
            text = text.lower().replace("-", "").replace(" ", "")
            for a, b in (("ṃ", "m"), ("ṅ", "m"), ("n", "m"), ("ā", "a"), ("ī", "i"),
                         ("ū", "u"), ("ḥ", "")):
                # Visarga drops everywhere, not just finally: YS 4.29 reads
                # "dharmameghaḥ samādhiḥ" as two words.
                text = text.replace(a, b)
            return text

        def stems(translit: str) -> set[str]:
            base = normalise(translit)
            found = {base}
            if len(base) > 4:
                found |= {base[:-1], base[:-2]}
            if base[:1] in {"a"}:
                found |= {base[1:], "ai" + base[1:]}
            if base[:1] == "e":
                found.add("ai" + base[1:])
            return {s for s in found if len(s) > 3}

        for term in self.terms:
            if term.source_text != "yoga_sutras" or term.verification != "source-verified":
                continue
            if term.id in exceptions:
                self.assertIn(
                    "does not literally appear",
                    term.source_context,
                    f"{term.id} is listed as an exception but does not explain why",
                )
                continue
            sanskrit = normalise(term.source_context.split(":", 1)[1].split('("')[0])
            self.assertTrue(
                any(stem in sanskrit for stem in stems(term.transliteration)),
                f"{term.id} is not present in the sutra quoted for it",
            )

    def test_chinese_mappings_name_where_they_were_found(self) -> None:
        """A mapping asserts a cross-linguistic claim, so it must cite a text."""
        taisho = re.compile(r"T\d{2}n\d{4}")
        for term in self.terms:
            for candidate in term.chinese_counterparts or []:
                source = candidate.get("source")
                self.assertTrue(source, f"{term.id}: {candidate['characters']} cites nothing")
                self.assertRegex(
                    source,
                    taisho,
                    f"{term.id}: {candidate['characters']} names no Taishō text",
                )

    def test_only_verified_terms_carry_chinese_mappings(self) -> None:
        """A term we have not checked against its own text should not also be
        making claims about how it was rendered in another language."""
        for term in self.terms:
            if term.chinese_counterparts:
                self.assertEqual(
                    term.verification,
                    "source-verified",
                    f"{term.id} is unverified but carries a Chinese mapping",
                )

    def test_morpheme_identifiers_are_bare(self) -> None:
        """A qualifier belongs in the meaning, not in the morpheme itself.

        Several entries once declared a suffix as "-ya (taddhita)". The card
        rendered it, but the cross-referencer keys on the exact morpheme, so
        those terms silently linked to nothing.
        """
        for term in self.terms:
            for field, key in (("roots", "root"), ("prefixes", "prefix"), ("suffixes", "suffix")):
                for component in getattr(term, field) or []:
                    value = component[key]
                    self.assertNotRegex(
                        value,
                        r"[ ()/]",
                        f"{term.id}: {key} {value!r} carries a qualifier or two morphemes",
                    )

    def test_segmentation_markers_are_declared(self) -> None:
        """A piece marked as a root or suffix needs a row explaining it."""
        for term in self.terms:
            body = re.sub(r"\([^)]*\)", "", term.segmentation or "")
            for piece in re.split(r"[|+\u2192]", body):
                piece = piece.strip()
                if piece.startswith("\u221a"):
                    self.assertTrue(
                        any(r["root"] == piece for r in term.roots or []),
                        f"{term.id}: segmentation names {piece}, which is not declared",
                    )
                elif piece.startswith("-"):
                    self.assertTrue(
                        any(s["suffix"] == piece for s in term.suffixes or []),
                        f"{term.id}: segmentation names {piece}, which is not declared",
                    )

    def test_sort_places_analysed_terms_first(self) -> None:
        ordered = sort_demo_terms(self.terms)
        first_extended = next(
            index
            for index, term in enumerate(ordered)
            if term.priority_bucket == "extended"
        )
        buckets_before = {term.priority_bucket for term in ordered[:first_extended]}
        self.assertNotIn("extended", buckets_before)


class SeedCatalogTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.repo = load_repository()

    def test_catalog_covers_the_whole_explorer(self) -> None:
        """The seed catalog is meant to be canonical, not a stale subset."""
        seed_ids = {term.id for term in self.repo.seed_terms}
        demo_ids = {term.id for term in build_demo_terms(self.repo)}
        self.assertEqual(demo_ids - seed_ids, set(), "explorer terms missing from catalog")

    def test_slugs_match_their_transliteration(self) -> None:
        for term in self.repo.seed_terms:
            self.assertEqual(
                term.normalized_slug,
                normalized_slug(term.transliteration),
                term.id,
            )

    def test_unverified_coverage_is_reported_as_a_warning(self) -> None:
        """Validation should surface the sourcing gap rather than stay silent."""
        issues = validate_repository(self.repo)
        warnings = [issue for issue in issues if issue.severity == "warning"]
        self.assertTrue(
            any("source-verified" in issue.message for issue in warnings),
            "no warning reports how many terms lack sourcing",
        )

    def test_validation_reports_no_errors(self) -> None:
        errors = [
            issue for issue in validate_repository(self.repo) if issue.severity == "error"
        ]
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

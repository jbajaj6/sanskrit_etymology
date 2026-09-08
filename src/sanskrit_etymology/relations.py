"""Cross-references between terms, derived from evidence already in the data.

The primary basis is word structure: two terms are related when they are built
from the same morpheme. That is a fact about the analysis, visible in the
breakdown the reader is already looking at, so each link can be traced.

A secondary basis is prose: one entry's authored text names another term. That
is an editorial judgement rather than a structural fact, but it is a judgement
a person actually made while writing, and it catches pairs no shared morpheme
would - guru and acarya, for instance.

Deliberately not used: substring containment between term names. It reads
"nididhyasana" as containing "asana" and "pranava" as containing "prana", both
of which are etymologically false. A link asserting a false derivation is worse
than no link at all.
"""

from __future__ import annotations

import re
from collections import defaultdict
from typing import Any

# A morpheme shared by more than this many terms is a grammatical default
# rather than a family worth following. The generic action-noun suffix "-a"
# covers a quarter of the corpus and says nothing; "-ana" covers the action
# nouns of practice (dhyana, dharana, sravana, nididhyasana) and says a lot.
MAX_GROUP = 20

# A term named in more than this share of the corpus carries little
# information. In practice this suppresses only "yoga".
HUB_SHARE = 0.25
MAX_MENTIONS = 6

# Homonyms: the prose contains the string but does not mean the term.
EXCLUDED_PAIRS = {
    # mrtyu's note discusses Yama the god of death, not yama the restraint.
    ("mrtyu", "yama"),
}

_DEVANAGARI = r"ऀ-ॿ"

MORPHEME_FIELDS = (
    ("root", "roots", "root"),
    ("prefix", "prefixes", "prefix"),
    ("suffix", "suffixes", "suffix"),
)


def _ref(term: Any) -> dict[str, str]:
    return {
        "id": term.id,
        "transliteration": term.transliteration,
        "devanagari": term.devanagari,
    }


def _prose(term: Any) -> str:
    return " ".join(
        part or ""
        for part in (
            term.literal_gloss,
            term.philosophical_gloss,
            term.doctrinal_significance,
            term.ambiguity_notes,
        )
    )


def _patterns(term: Any) -> list[re.Pattern[str]]:
    forms = {
        term.transliteration,
        term.transliteration.replace("-", ""),
        term.transliteration.replace("-", " "),
        term.devanagari,
    }
    return [
        re.compile(
            rf"(?<![\w{_DEVANAGARI}\-])" + re.escape(form) + rf"(?![\w{_DEVANAGARI}\-])",
            re.IGNORECASE,
        )
        for form in forms
        if len(form) > 2
    ]


def build_morpheme_index(terms: list[Any]) -> dict[tuple[str, str], list[str]]:
    """Map (kind, morpheme) to the ids of every term declaring it."""
    index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for term in terms:
        for kind, attr, key in MORPHEME_FIELDS:
            for component in getattr(term, attr, None) or []:
                name = str(component.get(key, "")).strip()
                if name:
                    index[(kind, name)].append(term.id)
    return index


def build_relations(terms: list[Any]) -> dict[str, dict[str, Any]]:
    """Return {term_id: {"morphemes": [...], "mentions": [...]}}."""
    by_id = {term.id: term for term in terms}
    index = build_morpheme_index(terms)

    # -- shared morphemes -------------------------------------------------
    shared: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for (kind, name), ids in index.items():
        unique = sorted(set(ids))
        if len(unique) < 2 or len(unique) > MAX_GROUP:
            continue
        for source in unique:
            siblings = [_ref(by_id[other]) for other in unique if other != source]
            shared[source].append(
                {"kind": kind, "morpheme": name, "terms": siblings}
            )

    for entries in shared.values():
        # Roots first: the tightest and most meaningful family.
        order = {"root": 0, "prefix": 1, "suffix": 2}
        entries.sort(key=lambda e: (order[e["kind"]], len(e["terms"]), e["morpheme"]))

    # -- names appearing in authored prose --------------------------------
    patterns = {term.id: _patterns(term) for term in terms}
    prose = {term.id: _prose(term) for term in terms}

    mentions: dict[str, set[str]] = defaultdict(set)
    for target in terms:
        pats = patterns[target.id]
        for source in terms:
            if source.id == target.id:
                continue
            if (source.id, target.id) in EXCLUDED_PAIRS:
                continue
            if any(pattern.search(prose[source.id]) for pattern in pats):
                mentions[source.id].add(target.id)

    incoming: dict[str, int] = defaultdict(int)
    for targets in mentions.values():
        for target in targets:
            incoming[target] += 1
    hub_cutoff = max(2, int(len(terms) * HUB_SHARE))
    hubs = {tid for tid, count in incoming.items() if count > hub_cutoff}

    relations: dict[str, dict[str, Any]] = {}
    for term in terms:
        structural = shared.get(term.id, [])
        already = {ref["id"] for entry in structural for ref in entry["terms"]}
        named = sorted(
            tid
            for tid in mentions.get(term.id, set())
            if tid not in already and tid not in hubs
        )
        relations[term.id] = {
            "morphemes": structural,
            "mentions": [_ref(by_id[tid]) for tid in named[:MAX_MENTIONS]],
        }
    return relations

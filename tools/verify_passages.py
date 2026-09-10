#!/usr/bin/env python3
"""Check every quoted passage against the source text it cites.

The explorer's central claim is that each source-verified term quotes a real
passage. This checks that claim the only way it can be checked: by comparing the
quoted Sanskrit, character for character, against the mūla text in a local
corpus.

It needs the GRETIL corpus on disk and so cannot run in CI; run it locally
whenever passages are added or edited:

    python3 tools/verify_passages.py

Comparison ignores whitespace, punctuation, and the anusvāra written either as
m or as ṃ. Nothing else is folded, so a genuine letter difference is reported.
An ellipsis in a quote marks a deliberate excerpt: each fragment must occur, in
order.

EMENDATIONS lists every place the quoted text departs from the corpus file
because that file has a clear input error. Each is also disclosed on the term's
own card. Anything not listed here must match verbatim.
"""

from __future__ import annotations

import html
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GRETIL = Path.home() / ".buddha/GRETIL/1_sanskr"
UPA_DIR = GRETIL / "1_veda/4_upa"
YS_FILE = GRETIL / "6_sastra/3_phil/yoga/patyog_u.htm"

UPA_FILES = {
    "BṛU": ("brup___u.htm", "BrhUp_"), "ChU": ("chup___u.htm", "ChUp_"),
    "KaU": ("kathop_u.htm", "KaU_"), "MāU": ("mandup_u.htm", "MandUp_"),
    "AiU": ("aitup__u.htm", "AitUp_"), "ĪśU": ("isup___u.htm", "IsUp_"),
    "ŚvU": ("svetu_pu.htm", "SvetUp_"), "PraU": ("prasup_u.htm", "PrUp_"),
}

EMENDATIONS = {
    ("susupti",  "MāU", "5"):      ("evāndamayo", "evānandamayo"),
    ("dahara",   "ChU", "8.1.1"):  ("antarākāsaḥ", "antarākāśaḥ"),
    ("avyakta",  "KaU", "3.11"):   ("puruśān", "puruṣān"),
    ("taijasa",  "MāU", "4"):      ("svaprasthāno", "svapnasthāno"),
    ("upanisad", "BṛU", "2.4.10"): ("vyākhyānani", "vyākhyānāni"),
}

REF = re.compile(r"[|/]{2}\s*([A-Za-z_]+[\d,.\-]+)\s*[|/]{2}")
CITE = re.compile(r"(YS|BṛU|ChU|KaU|MāU|AiU|ĪśU|ŚvU|PraU|MuU)\s*(\d+(?:[.,]\d+)*)\s*:\s*")


def _plain(path: Path) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", path.read_text(encoding="utf-8", errors="replace")))
    tail = text.rsplit("gretil.htm", 1)
    return tail[1] if len(tail) == 2 else text


def _units(path: Path) -> dict[str, str]:
    text = _plain(path)
    out, prev = {}, 0
    for m in REF.finditer(text):
        body = " ".join(text[prev:m.start()].split())
        if body:
            out[m.group(1).strip()] = body
        prev = m.end()
    return out


def load_corpus() -> dict[str, dict[str, str]]:
    corpus: dict[str, dict[str, str]] = {}
    if YS_FILE.exists():
        raw = _units(YS_FILE)
        corpus["YS"] = {k.replace("YS_", ""): v for k, v in raw.items()}
    for sigla, (fname, _) in UPA_FILES.items():
        path = UPA_DIR / fname
        corpus[sigla] = _units(path) if path.exists() else {}
    return corpus


def lookup(corpus, sigla, ref):
    table = corpus.get(sigla) or {}
    if sigla == "YS":
        return table.get(ref)
    prefix = UPA_FILES[sigla][1]
    parts = ref.split(".")
    candidates = [prefix + ref]
    if len(parts) == 3:
        candidates.append(f"{prefix}{parts[0]},{parts[1]}.{parts[2]}")
    if len(parts) == 2:
        candidates.append(f"{prefix}{parts[0]},{parts[1]}")
    for c in candidates:
        if c in table:
            return table[c]
    return None


def norm(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\s|/(),;:'\"’‘`\-–—\[\]]+", "", text)
    return text.replace("ṃ", "m").replace("ṁ", "m").lower()


def main() -> int:
    if not UPA_DIR.exists():
        print(f"GRETIL corpus not found at {GRETIL}; nothing to check against.")
        return 2

    corpus = load_corpus()
    analyses = yaml.safe_load(
        (ROOT / "data/analyses/term_analyses.yaml").read_text(encoding="utf-8")
    )["analyses"]

    tally, failures = Counter(), []
    for term in analyses:
        ctx = term.get("source_context")
        if not ctx:
            continue
        marks = list(CITE.finditer(ctx))
        if not marks:
            tally["no citation"] += 1
            failures.append((term["id"], "?", "no citation parsed", ""))
            continue
        for i, m in enumerate(marks):
            sigla, ref = m.group(1), m.group(2).replace(",", ".")
            stop = marks[i + 1].start() if i + 1 < len(marks) else len(ctx)
            quoted = ctx[m.end():stop].split('("')[0]
            source = lookup(corpus, sigla, ref)
            fix = EMENDATIONS.get((term["id"], sigla, ref))
            if source is not None and fix:
                source = source.replace(*fix)
            if source is None:
                tally["reference not found"] += 1
                failures.append((term["id"], f"{sigla} {ref}", "reference not found", ""))
                continue
            fragments = [f for f in re.split(r"\.\.\.|…", quoted) if norm(f)]
            haystack, pos, bad = norm(source), 0, None
            for frag in fragments:
                idx = haystack.find(norm(frag), pos)
                if idx == -1:
                    bad = frag.strip()[:80]
                    break
                pos = idx + len(norm(frag))
            if bad is None:
                tally["verified"] += 1
            else:
                tally["MISMATCH"] += 1
                failures.append((term["id"], f"{sigla} {ref}", "does not match source", bad))

    for tid, ref, why, extra in failures:
        print(f"  {why:22s} {tid:22s} {ref:12s} {extra}")
    print(f"\n{dict(tally)}")
    if EMENDATIONS:
        print(f"({len(EMENDATIONS)} disclosed emendations of errors in the corpus files)")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

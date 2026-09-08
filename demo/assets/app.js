(function () {
  "use strict";

  const terms = Array.isArray(window.TERMS_DATA) ? window.TERMS_DATA : [];
  const searchEl = document.getElementById("search");
  const suggestionsEl = document.getElementById("suggestions");
  const browseEl = document.getElementById("browse");
  const resultEl = document.getElementById("result");
  const termGridEl = document.getElementById("termGrid");
  const filterBarEl = document.getElementById("filterBar");
  const browseCountEl = document.getElementById("browseCount");

  const THEMES = [
    { id: "all", label: "All terms" },
    { id: "meditation_core", label: "Meditation" },
    { id: "mind_psychology", label: "Mind" },
    { id: "affliction_obstacle", label: "Afflictions" },
    { id: "practice_discipline", label: "Practice" },
    { id: "insight_knowledge", label: "Knowledge" },
    { id: "liberation_metaphysics", label: "Liberation" },
    { id: "advanced_compound", label: "Compounds" },
  ];

  const KIND_LABEL = { prefix: "Prefix", root: "Root", suffix: "Suffix", stem: "Stem" };

  // Citation sigla used to split a stored passage into its quoted units.
  const CITE_RE =
    /(?:YS|B[ṛr]U|ChU|KaU|M[āa]U|AiU|[ĪI][śs]U|[ŚS]vU|PraU|MuU|T\.\d+)\s*[\d][\d.,\s–-]*(?=:)/g;

  const THEME_LABELS = Object.fromEntries(
    THEMES.filter((theme) => theme.id !== "all").map((theme) => [theme.id, theme.label])
  );
  const THEME_ORDER = THEMES.map((theme) => theme.id).filter((id) => id !== "all");

  const SOURCES = [
    { id: "all", label: "All sources" },
    { id: "yoga_sutras", label: "Yoga Sutras" },
    { id: "upanisads", label: "Upaniṣads" },
  ];
  const SOURCE_LABELS = {
    yoga_sutras: "Yoga Sutras",
    upanisads: "Upaniṣads",
  };

  let activeIndex = -1;
  let activeTheme = "all";
  let activeSource = "all";
  let verifiedOnly = false;

  if (!terms.length) {
    resultEl.style.display = "block";
    resultEl.innerHTML =
      '<div class="empty-state">Demo data not loaded. Run <code>sanskrit-etymology build-demo</code>.</div>';
    return;
  }

  renderFilters();
  renderGrid();
  routeFromHash();

  window.addEventListener("hashchange", routeFromHash);

  searchEl.addEventListener("input", () => {
    const query = searchEl.value.trim().toLowerCase();
    activeIndex = -1;
    if (!query) {
      hideSuggestions();
      return;
    }
    showSuggestions(searchTerms(query));
  });

  searchEl.addEventListener("keydown", (event) => {
    const items = suggestionsEl.querySelectorAll(".suggestion-item");
    if (event.key === "ArrowDown" && items.length) {
      event.preventDefault();
      activeIndex = Math.min(activeIndex + 1, items.length - 1);
      updateActive(items);
      return;
    }

    if (event.key === "ArrowUp" && items.length) {
      event.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      updateActive(items);
      return;
    }

    if (event.key === "Escape") {
      hideSuggestions();
      return;
    }

    if (event.key === "Enter") {
      event.preventDefault();
      if (activeIndex >= 0 && items[activeIndex]) {
        openTerm(items[activeIndex].dataset.id);
        return;
      }
      if (items.length > 0) {
        openTerm(items[0].dataset.id);
      }
    }
  });

  document.addEventListener("click", (event) => {
    const suggestion = event.target.closest(".suggestion-item");
    if (suggestion) {
      openTerm(suggestion.dataset.id);
      return;
    }

    const row = event.target.closest(".row-link, .term-link");
    if (row) {
      openTerm(row.dataset.id);
      return;
    }

    const filter = event.target.closest(".filter-btn");
    if (filter) {
      activeTheme = filter.dataset.theme;
      renderFilters();
      renderGrid();
      return;
    }

    const source = event.target.closest(".source-btn");
    if (source) {
      activeSource = source.dataset.source;
      renderFilters();
      renderGrid();
      return;
    }

    const toggle = event.target.closest(".verified-toggle");
    if (toggle) {
      verifiedOnly = !verifiedOnly;
      renderFilters();
      renderGrid();
      return;
    }

    if (event.target.closest(".back-btn")) {
      event.preventDefault();
      goBack();
      return;
    }

    if (
      !event.target.closest(".search-container") &&
      !event.target.closest(".suggestions")
    ) {
      hideSuggestions();
    }
  });

  /* ---------- routing ---------- */

  function routeFromHash() {
    const slug = decodeURIComponent(window.location.hash.replace(/^#/, "")).trim();
    if (!slug) {
      showBrowse();
      return;
    }
    const term = findTerm(slug);
    if (!term) {
      showBrowse();
      return;
    }
    showCard(term);
  }

  function openTerm(termId) {
    const term = findTerm(termId);
    if (!term) {
      return;
    }
    // Let the hashchange handler do the rendering so that back/forward,
    // direct links, and clicks all take the same path.
    if (decodeURIComponent(window.location.hash.replace(/^#/, "")) === term.id) {
      showCard(term);
      return;
    }
    window.location.hash = encodeURIComponent(term.id);
  }

  function goBack() {
    if (window.location.hash) {
      window.history.back();
      return;
    }
    showBrowse();
  }

  function findTerm(slug) {
    const needle = String(slug).toLowerCase();
    return (
      terms.find((term) => term.id.toLowerCase() === needle) ||
      terms.find((term) => (term.search_aliases || []).includes(needle))
    );
  }

  /* ---------- views ---------- */

  function showBrowse() {
    hideSuggestions();
    resultEl.style.display = "none";
    resultEl.innerHTML = "";
    browseEl.style.display = "block";
  }

  function showCard(term) {
    hideSuggestions();
    searchEl.value = "";
    browseEl.style.display = "none";
    resultEl.style.display = "block";
    resultEl.innerHTML = renderCard(term);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ---------- search ---------- */

  function searchTerms(query) {
    const scored = [];
    terms.forEach((term) => {
      const aliases = term.search_aliases || [];
      const translit = (term.transliteration || "").toLowerCase();
      let rank = null;

      if (aliases.some((alias) => alias === query)) {
        rank = 0;
      } else if (aliases.some((alias) => alias.startsWith(query))) {
        rank = 1;
      } else if (translit.includes(query) || (term.devanagari || "").includes(query)) {
        rank = 2;
      } else if (query.length >= 3 && glossText(term).includes(query)) {
        // Meaning search: someone who knows "absorption" but not "samadhi".
        rank = 3;
      }

      if (rank !== null) {
        scored.push({ term, rank });
      }
    });

    scored.sort(
      (a, b) => a.rank - b.rank || a.term.transliteration.localeCompare(b.term.transliteration)
    );
    return scored;
  }

  function glossText(term) {
    return [
      term.literal_gloss,
      term.professor_gloss,
      term.philosophical_gloss,
      term.doctrinal_significance,
    ]
      .filter(Boolean)
      .join(" ")
      .toLowerCase();
  }

  function showSuggestions(matches) {
    if (!matches.length) {
      suggestionsEl.innerHTML = '<div class="no-results">No matching terms</div>';
      suggestionsEl.style.display = "block";
      return;
    }

    suggestionsEl.innerHTML = matches
      .slice(0, 8)
      .map(
        ({ term, rank }) => `
          <div class="suggestion-item" data-id="${esc(term.id)}">
            <span class="suggestion-deva">${esc(term.devanagari)}</span>
            <span class="suggestion-iast">${esc(term.transliteration)}</span>
            <span class="suggestion-gloss">${esc(truncate(term.literal_gloss, 40))}</span>
            ${rank === 3 ? '<span class="suggestion-why">meaning</span>' : ""}
          </div>
        `
      )
      .join("");
    suggestionsEl.style.display = "block";
  }

  function hideSuggestions() {
    suggestionsEl.style.display = "none";
  }

  function updateActive(items) {
    [...items].forEach((item, index) => {
      item.classList.toggle("active", index === activeIndex);
    });
  }

  /* ---------- browse grid ---------- */

  function renderFilters() {
    const counts = {};
    terms
      .filter((term) => inActiveSource(term))
      .forEach((term) => {
        const key = term.thematic_bucket || "unsorted";
        counts[key] = (counts[key] || 0) + 1;
      });

    const buttons = THEMES.filter(
      (theme) => theme.id === "all" || counts[theme.id]
    )
      .map((theme) => {
        const count =
          theme.id === "all"
            ? terms.filter((term) => inActiveSource(term)).length
            : counts[theme.id];
        const active = theme.id === activeTheme ? " active" : "";
        return `<button class="filter-btn${active}" data-theme="${theme.id}">
          ${esc(theme.label)} <span class="filter-count">${count}</span>
        </button>`;
      })
      .join("");

    const sourceCounts = {};
    terms.forEach((term) => {
      const key = term.source_text || "yoga_sutras";
      sourceCounts[key] = (sourceCounts[key] || 0) + 1;
    });
    const sourceButtons = SOURCES.filter(
      (source) => source.id === "all" || sourceCounts[source.id]
    )
      .map((source) => {
        const count = source.id === "all" ? terms.length : sourceCounts[source.id];
        const active = source.id === activeSource ? " active" : "";
        return `<button class="source-btn${active}" data-source="${source.id}">
          ${esc(source.label)} <span class="filter-count">${count}</span>
        </button>`;
      })
      .join("");

    const verifiedCount = terms.filter(isVerified).length;
    const toggle = `<button class="verified-toggle${verifiedOnly ? " active" : ""}"
      aria-pressed="${verifiedOnly}">
      Show only source-verified terms <span class="filter-count">${verifiedCount}</span>
    </button>`;

    filterBarEl.innerHTML = `
      <div class="filter-group">
        <span class="filter-legend" id="lg-source">Source</span>
        <div class="segmented" role="group" aria-labelledby="lg-source">${sourceButtons}</div>
      </div>
      <div class="filter-group">
        <span class="filter-legend" id="lg-theme">Theme</span>
        <div class="filter-set" role="group" aria-labelledby="lg-theme">${buttons}</div>
      </div>
      <div class="filter-group">
        <span class="filter-legend">Sourcing</span>
        ${toggle}
      </div>`;
  }

  function inActiveSource(term) {
    return activeSource === "all" || (term.source_text || "yoga_sutras") === activeSource;
  }

  function visibleTerms() {
    return terms.filter((term) => {
      if (!inActiveSource(term)) {
        return false;
      }
      if (activeTheme !== "all" && term.thematic_bucket !== activeTheme) {
        return false;
      }
      if (verifiedOnly && !isVerified(term)) {
        return false;
      }
      return true;
    });
  }

  function renderGrid() {
    const shown = visibleTerms();
    browseCountEl.textContent = shown.length
      ? `${shown.length} ${shown.length === 1 ? "term" : "terms"}`
      : "";

    if (!shown.length) {
      termGridEl.innerHTML =
        '<p class="browse-empty">No terms match these filters. Clear one to widen the search.</p>';
      return;
    }

    // Reading a corpus is easier under headings than as one undivided field.
    const grouped = new Map();
    shown.forEach((term) => {
      const key = term.thematic_bucket || "advanced_compound";
      if (!grouped.has(key)) {
        grouped.set(key, []);
      }
      grouped.get(key).push(term);
    });

    const order = activeTheme === "all" ? THEME_ORDER : [activeTheme];
    termGridEl.innerHTML = order
      .filter((theme) => grouped.has(theme))
      .map((theme) => {
        const entries = grouped
          .get(theme)
          .slice()
          .sort((a, b) => a.transliteration.localeCompare(b.transliteration));
        return `
          <section class="term-group">
            <h2 class="group-heading">
              <span class="group-name">${esc(THEME_LABELS[theme] || theme)}</span>
              <span class="group-count">${entries.length}</span>
            </h2>
            <ul class="term-list">${entries.map(termRow).join("")}</ul>
          </section>
        `;
      })
      .join("");
  }

  function termRow(term) {
    const verified = isVerified(term)
      ? '<span class="row-verified" title="Source-verified"></span>'
      : "";
    return `
      <li class="term-row">
        <a class="row-link" href="#${encodeURIComponent(term.id)}" data-id="${esc(term.id)}">
          <span class="row-deva">${esc(term.devanagari)}</span>
          <span class="row-iast">${esc(term.transliteration)}</span>
          <span class="row-gloss">${esc(term.professor_gloss || term.literal_gloss)}</span>
          ${verified}
        </a>
      </li>
    `;
  }

  function isVerified(term) {
    return term.verification === "source-verified";
  }

  /* ---------- term card ---------- */

  function renderCard(term) {
    const morphology = buildMorphologyRows(term);
    const segmentation = buildSegmentation(term);

    const structure =
      segmentation || morphology
        ? `
          <section class="card-section">
            <h2 class="section-label">Word structure</h2>
            ${segmentation}
            ${morphology}
          </section>
        `
        : "";

    return `
      <a class="back-btn" href="#">Back to all terms</a>
      <article class="result-card">
        <header class="card-header">
          <p class="card-corpus">${esc(SOURCE_LABELS[term.source_text] || SOURCE_LABELS.yoga_sutras)}</p>
          <h1 class="card-deva">${esc(term.devanagari)}</h1>
          <p class="card-iast">${esc(term.transliteration)}</p>
          <p class="card-gloss-short">${esc(term.literal_gloss)}</p>
          <p class="card-badges">${renderVerificationBadge(term)}${renderConfidence(term)}</p>
        </header>

        ${buildSourceSection(term)}

        <div class="card-body">
          ${structure}
          ${section("Philosophical meaning", esc(term.philosophical_gloss), "prose")}
          ${section("Doctrinal significance", esc(term.doctrinal_significance), "prose")}
          ${
            term.compound_type
              ? section("Compound type", esc(term.compound_type))
              : ""
          }
          ${buildRelatedSection(term)}
          ${buildChineseSection(term)}
          ${
            term.ambiguity_notes
              ? section("Scholarly notes", esc(term.ambiguity_notes), "prose")
              : ""
          }
          ${buildCitationSection(term)}
        </div>
      </article>
    `;
  }

  function section(label, content, extraClass) {
    return `
      <section class="card-section">
        <h2 class="section-label">${label}</h2>
        <div class="section-content ${extraClass || ""}">${content}</div>
      </section>
    `;
  }

  function renderConfidence(term) {
    return `<span class="tag tag-confidence">${esc(term.confidence)} confidence in the analysis</span>`;
  }

  function renderVerificationBadge(term) {
    return isVerified(term)
      ? '<span class="tag tag-verified">Source-verified</span>'
      : '<span class="tag tag-unverified">Not yet source-verified</span>';
  }

  function buildSourceSection(term) {
    const cite = `<cite class="source-cite">${esc(term.chapter)}</cite>`;

    if (!term.source_context) {
      return `
        <section class="source-panel source-panel-empty">
          <h2 class="section-label">Where it appears</h2>
          ${cite}
          <p class="source-missing">
            No passage has been recorded for this term yet. The references above come
            from the working catalogue and have not been checked against the text.
          </p>
        </section>
      `;
    }

    return `
      <section class="source-panel">
        <h2 class="section-label">Where it appears</h2>
        ${cite}
        <blockquote class="source-quote">${formatPassage(term.source_context)}</blockquote>
      </section>
    `;
  }

  // Passages are authored as "<citation>: <sanskrit> (\"<translation>\")", sometimes
  // several in a row, sometimes with a trailing remark. Anchor on the citation
  // sigla rather than on punctuation: an earlier version split on ") " and broke
  // on entries where the passages are joined by ". " instead.

  function formatPassage(raw) {
    const text = String(raw).trim();
    const starts = [];
    let match;
    CITE_RE.lastIndex = 0;
    while ((match = CITE_RE.exec(text)) !== null) {
      starts.push({ index: match.index, label: match[0].trim() });
    }

    if (!starts.length) {
      return `<p class="passage"><span class="passage-sanskrit">${esc(text)}</span></p>`;
    }

    const blocks = [];
    const preamble = text.slice(0, starts[0].index).trim();
    if (preamble) {
      blocks.push(`<p class="passage-aside">${esc(preamble)}</p>`);
    }

    starts.forEach((cite, i) => {
      const stop = i + 1 < starts.length ? starts[i + 1].index : text.length;
      let body = text.slice(cite.index + cite.label.length, stop).trim();
      body = body.replace(/^:\s*/, "").replace(/[.;]\s*$/, "");

      const quoted = body.match(/^([\s\S]*?)\s*\(\s*"([\s\S]*?)"\s*\)\s*([\s\S]*)$/);
      const sanskrit = quoted ? quoted[1].trim() : body;
      const english = quoted ? quoted[2].trim() : "";
      const tail = quoted ? quoted[3].replace(/^[.;,\s]+/, "").trim() : "";

      blocks.push(`
        <div class="passage">
          <span class="passage-ref">${esc(cite.label)}</span>
          ${sanskrit ? `<span class="passage-sanskrit">${esc(sanskrit)}</span>` : ""}
          ${english ? `<span class="passage-english">${esc(english)}</span>` : ""}
          ${tail ? `<span class="passage-tail">${esc(tail)}</span>` : ""}
        </div>
      `);
    });

    return blocks.join("");
  }

  function buildCitationSection(term) {
    const trail = term.citation_trail || [];
    if (!trail.length) {
      return "";
    }
    return `
      <section class="card-section">
        <h2 class="section-label">Citation trail</h2>
        <ul class="citation-list">${trail.map((e) => `<li>${esc(e)}</li>`).join("")}</ul>
      </section>
    `;
  }

  function buildChineseSection(term) {
    const candidates = term.chinese_counterparts || [];
    if (!candidates.length) {
      return "";
    }
    const cards = candidates
      .map((candidate) => {
        const mappingType = (candidate.mapping_type || "").replace(/_/g, " ");
        return `
          <div class="chinese-item">
            <span class="chinese-chars">${esc(candidate.characters)}</span>
            <span class="chinese-pinyin">${esc(candidate.pinyin)}</span>
            <span class="chinese-type">${esc(mappingType)}</span>
          </div>
        `;
      })
      .join("");
    return `
      <section class="card-section">
        <h2 class="section-label">Chinese Buddhist equivalents</h2>
        <div class="chinese-list">${cards}</div>
      </section>
    `;
  }

  /* ---------- morphology ----------

     The segmentation string is authored, not generated, and carries its own
     markers: a leading √ marks a root, a leading hyphen marks a suffix. Earlier
     this code guessed instead, matching each piece against the declared
     prefix/root/suffix lists by substring in both directions. A one-letter
     prefix such as "a-" is a substring of almost every Sanskrit morpheme, so
     that guess mis-coloured 38 of 120 terms. Trust the markers; fall back to an
     exact match against the declared parts; leave anything else unmarked.        */

  function parseSegmentation(term) {
    const raw = (term.segmentation || "").trim();
    if (!raw) {
      return null;
    }

    // A trailing parenthetical is an editorial remark, not a morpheme.
    let note = "";
    let body = raw;
    const noteMatch = body.match(/\s*\(([^()]*)\)\s*$/);
    if (noteMatch) {
      note = noteMatch[1].trim();
      body = body.slice(0, noteMatch.index).trim();
    }

    // "→" introduces the inflected form the analysis resolves to.
    let derived = "";
    const arrowAt = body.indexOf("→");
    if (arrowAt !== -1) {
      derived = body.slice(arrowAt + 1).trim();
      body = body.slice(0, arrowAt).trim();
    }

    // "|" separates the members of a compound analysed word by word.
    const groups = body
      .split("|")
      .map((group) => group.trim())
      .filter(Boolean)
      .map((group) =>
        group
          .split(/\s*\+\s*/)
          .map((piece) => piece.trim())
          .filter(Boolean)
          .map((piece) => {
            // A parenthetical can also sit on an individual morpheme, as in
            // "ni + √dhyai (desiderative, reduplicated) + -ana".
            const inline = piece.match(/^(.*?)\s*\(([^()]*)\)\s*$/);
            const text = inline ? inline[1].trim() : piece;
            return {
              text,
              gloss: inline ? inline[2].trim() : "",
              kind: classifyPiece(text, term),
            };
          })
      );

    if (!groups.length) {
      return null;
    }
    return { groups, note, derived };
  }

  function classifyPiece(piece, term) {
    if (piece.startsWith("√")) {
      return "root";
    }
    if (piece.startsWith("-")) {
      return "suffix";
    }

    const bare = piece.replace(/^[√-]|-$/g, "");
    const declared = (list, key, strip) =>
      (list || []).some((item) => item[key].replace(strip, "") === bare);

    if (declared(term.prefixes, "prefix", /-$/)) {
      return "prefix";
    }
    if (declared(term.roots, "root", /^√/)) {
      return "root";
    }
    if (declared(term.suffixes, "suffix", /^-/)) {
      return "suffix";
    }
    // A stem, a particle, or a compound member with no affix marking.
    return "stem";
  }

  function buildSegmentation(term) {
    const parsed = parseSegmentation(term);
    if (!parsed) {
      return "";
    }

    const groups = parsed.groups
      .map((pieces) =>
        `<span class="seg-group">` +
        pieces
          .map(
            (piece, index) =>
              `<span class="seg-piece seg-${piece.kind}"${
                piece.gloss ? ` title="${esc(piece.gloss)}"` : ""
              }>${esc(piece.text)}${
                piece.gloss ? `<span class="seg-piece-note">${esc(piece.gloss)}</span>` : ""
              }</span>` +
              (index < pieces.length - 1 ? '<span class="seg-join">+</span>' : "")
          )
          .join("") +
        `</span>`
      )
      .join('<span class="seg-boundary">·</span>');

    const derived = parsed.derived
      ? `<span class="seg-derived"><span class="seg-arrow">→</span>${esc(parsed.derived)}</span>`
      : "";
    const note = parsed.note ? `<p class="seg-note">${esc(parsed.note)}</p>` : "";

    return `<div class="seg-line">${groups}${derived}</div>${note}`;
  }

  function buildMorphologyRows(term) {
    const rows = [];
    (term.prefixes || []).forEach((prefix) => {
      rows.push({ kind: "prefix", key: prefix.prefix, value: prefix.prefix, meaning: prefix.meaning });
    });
    (term.roots || []).forEach((root) => {
      rows.push({
        kind: "root",
        key: root.root,
        value: `${root.root}${root.devanagari ? ` ${root.devanagari}` : ""}`,
        meaning: root.meaning,
      });
    });
    (term.suffixes || []).forEach((suffix) => {
      rows.push({
        kind: "suffix",
        key: suffix.suffix,
        value: suffix.suffix,
        meaning: suffix.grammatical_function
          ? `${suffix.meaning} — ${suffix.grammatical_function}`
          : suffix.meaning,
      });
    });

    if (!rows.length) {
      return "";
    }

    const shared = new Map(
      (term.related_morphemes || []).map((entry) => [`${entry.kind}:${entry.morpheme}`, entry.terms])
    );

    return `
      <dl class="morph-list">
        ${rows
          .map((row) => {
            const siblings = shared.get(`${row.kind}:${row.key}`) || [];
            return `
              <dt class="morph-term">
                <span class="morph-kind">${KIND_LABEL[row.kind]}</span>
                <span class="morph-value">${esc(row.value)}</span>
              </dt>
              <dd class="morph-meaning">
                ${esc(row.meaning)}
                ${buildSiblingLinks(row, siblings)}
              </dd>
            `;
          })
          .join("")}
      </dl>
    `;
  }

  // The connection a reader most wants is "what else is built from this piece",
  // so it belongs on the piece itself rather than in a footnote at the bottom.
  function buildSiblingLinks(row, siblings) {
    if (!siblings.length) {
      return "";
    }
    const links = siblings
      .map(
        (other) =>
          `<a class="term-link" href="#${encodeURIComponent(other.id)}" data-id="${esc(other.id)}">
             <span class="term-link-deva">${esc(other.devanagari)}</span>${esc(other.transliteration)}
           </a>`
      )
      .join("");
    return `
      <div class="morph-links">
        <span class="morph-links-label">Also built on ${esc(row.key)}</span>
        <div class="term-link-row">${links}</div>
      </div>
    `;
  }

  function buildRelatedSection(term) {
    const mentions = term.related_mentions || [];
    if (!mentions.length) {
      return "";
    }
    const links = mentions
      .map(
        (other) =>
          `<a class="term-link" href="#${encodeURIComponent(other.id)}" data-id="${esc(other.id)}">
             <span class="term-link-deva">${esc(other.devanagari)}</span>${esc(other.transliteration)}
           </a>`
      )
      .join("");
    return `
      <section class="card-section">
        <h2 class="section-label">Discussed in this entry</h2>
        <div class="term-link-row">${links}</div>
      </section>
    `;
  }

  /* ---------- helpers ---------- */

  function esc(value) {
    return String(value === null || value === undefined ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function truncate(text, maxLength) {
    if (!text) {
      return "";
    }
    return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
  }
})();

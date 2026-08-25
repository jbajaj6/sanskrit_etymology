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

  let activeIndex = -1;
  let activeTheme = "all";
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

    const chip = event.target.closest(".term-chip");
    if (chip) {
      openTerm(chip.dataset.id);
      return;
    }

    const filter = event.target.closest(".filter-btn");
    if (filter) {
      activeTheme = filter.dataset.theme;
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
    terms.forEach((term) => {
      const key = term.thematic_bucket || "unsorted";
      counts[key] = (counts[key] || 0) + 1;
    });

    const buttons = THEMES.filter(
      (theme) => theme.id === "all" || counts[theme.id]
    )
      .map((theme) => {
        const count = theme.id === "all" ? terms.length : counts[theme.id];
        const active = theme.id === activeTheme ? " active" : "";
        return `<button class="filter-btn${active}" data-theme="${theme.id}">
          ${esc(theme.label)} <span class="filter-count">${count}</span>
        </button>`;
      })
      .join("");

    const verifiedCount = terms.filter(isVerified).length;
    const toggle = `<button class="verified-toggle${verifiedOnly ? " active" : ""}"
      aria-pressed="${verifiedOnly}">
      Source-verified only <span class="filter-count">${verifiedCount}</span>
    </button>`;

    filterBarEl.innerHTML = `<div class="filter-row">${buttons}</div>
      <div class="filter-row filter-row-secondary">${toggle}</div>`;
  }

  function visibleTerms() {
    return terms.filter((term) => {
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
      ? `${shown.length} of ${terms.length} terms`
      : "No terms match this filter";

    termGridEl.innerHTML = shown
      .map(
        (term) => `
          <a class="term-chip${isVerified(term) ? " chip-verified" : ""}"
             href="#${encodeURIComponent(term.id)}"
             data-id="${esc(term.id)}">
            <span class="chip-deva">${esc(term.devanagari)}</span>
            ${esc(term.transliteration)}
          </a>
        `
      )
      .join("");
  }

  function isVerified(term) {
    return term.verification === "source-verified";
  }

  /* ---------- term card ---------- */

  function renderCard(term) {
    const confidenceClass =
      term.confidence === "high"
        ? "conf-high"
        : term.confidence === "medium"
        ? "conf-medium"
        : "conf-low";

    return `
      <button class="back-btn">&larr; Back to term list</button>
      <div class="result-card">
        <div class="card-header">
          <div class="card-badges">
            ${renderVerificationBadge(term)}
            <span class="card-confidence ${confidenceClass}">${esc(
      term.confidence
    )} confidence</span>
          </div>
          <div class="card-deva">${esc(term.devanagari)}</div>
          <div class="card-iast">${esc(term.transliteration)}</div>
          <div class="card-gloss-short">${esc(term.literal_gloss)}</div>
        </div>

        <div class="segmentation-strip">${buildSegmentation(term)}</div>

        <div class="card-body">
          <div class="card-section">
            <div class="section-label">Morphological Components</div>
            <div class="morph-grid">${buildMorphologyCards(term)}</div>
          </div>

          ${
            term.compound_type
              ? section("Compound Type", esc(term.compound_type))
              : ""
          }

          ${buildSourceSection(term)}

          ${section("Philosophical Meaning", esc(term.philosophical_gloss), "serif")}
          ${section("Doctrinal Significance", esc(term.doctrinal_significance), "serif")}

          ${buildChineseSection(term)}
          ${
            term.ambiguity_notes
              ? section("Scholarly Notes", esc(term.ambiguity_notes), "serif")
              : ""
          }
          ${buildCitationSection(term)}
        </div>
      </div>
    `;
  }

  function section(label, content, extraClass) {
    return `
      <div class="card-section">
        <div class="section-label">${label}</div>
        <div class="section-content ${extraClass || ""}">${content}</div>
      </div>
    `;
  }

  function renderVerificationBadge(term) {
    if (isVerified(term)) {
      return '<span class="card-verified verified-yes">source-verified</span>';
    }
    return '<span class="card-verified verified-no">not yet source-verified</span>';
  }

  function buildSourceSection(term) {
    const chapter = `<span class="chapter-ref">${esc(term.chapter)}</span>`;

    if (!term.source_context) {
      return `
        <div class="card-section">
          <div class="section-label">Where It Appears</div>
          <div class="section-content">${chapter}</div>
          <div class="source-missing">
            This term has not yet been checked against the text. The passage
            references above come from the working bundle, and no quoted sutra
            has been recorded for it.
          </div>
        </div>
      `;
    }

    return `
      <div class="card-section">
        <div class="section-label">Where It Appears</div>
        <div class="section-content">${chapter}</div>
        <blockquote class="source-quote serif">${esc(term.source_context)}</blockquote>
      </div>
    `;
  }

  function buildCitationSection(term) {
    const trail = term.citation_trail || [];
    if (!trail.length) {
      return "";
    }
    const items = trail.map((entry) => `<li>${esc(entry)}</li>`).join("");
    return `
      <div class="card-section">
        <div class="section-label">Citation Trail</div>
        <ul class="citation-list">${items}</ul>
      </div>
    `;
  }

  function buildMorphologyCards(term) {
    const cards = [];
    (term.prefixes || []).forEach((prefix) => {
      cards.push({ type: "Prefix", value: prefix.prefix, meaning: prefix.meaning });
    });
    (term.roots || []).forEach((root) => {
      cards.push({
        type: "Root",
        value: `${root.root}${root.devanagari ? ` ${root.devanagari}` : ""}`,
        meaning: root.meaning,
      });
    });
    (term.suffixes || []).forEach((suffix) => {
      cards.push({
        type: "Suffix",
        value: suffix.suffix,
        meaning: suffix.grammatical_function
          ? `${suffix.meaning} — ${suffix.grammatical_function}`
          : suffix.meaning,
      });
    });

    if (!cards.length) {
      return `
        <div class="morph-item">
          <div class="morph-type">Status</div>
          <div class="morph-value">Pending</div>
          <div class="morph-meaning">This term does not yet have a canonical morphological breakdown.</div>
        </div>
      `;
    }

    return cards
      .map(
        (card) => `
          <div class="morph-item">
            <div class="morph-type">${esc(card.type)}</div>
            <div class="morph-value">${esc(card.value)}</div>
            <div class="morph-meaning">${esc(card.meaning)}</div>
          </div>
        `
      )
      .join("");
  }

  function buildChineseSection(term) {
    const candidates = term.chinese_counterparts || [];
    if (!candidates.length) {
      return "";
    }

    const cards = candidates
      .map((candidate) => {
        const mappingType = candidate.mapping_type || "";
        return `
          <div class="chinese-card">
            <div class="chinese-chars">${esc(candidate.characters)}</div>
            <div class="chinese-pinyin">${esc(candidate.pinyin)}</div>
            <span class="chinese-type type-${esc(mappingType.replace(/\s/g, "_"))}">
              ${esc(mappingType.replace(/_/g, " "))}
            </span>
          </div>
        `;
      })
      .join("");

    return `
      <div class="card-section">
        <div class="section-label">Chinese Buddhist Equivalents</div>
        <div class="chinese-cards">${cards}</div>
      </div>
    `;
  }

  function buildSegmentation(term) {
    if (!term.segmentation) {
      return "";
    }

    const parts = term.segmentation.split(/\s*\+\s*/);
    const prefixes = (term.prefixes || []).map((prefix) => prefix.prefix.replace("-", ""));
    const roots = (term.roots || []).map((root) => root.root.replace("√", ""));
    const suffixes = (term.suffixes || []).map((suffix) => suffix.suffix.replace("-", ""));

    return parts
      .map((part, index) => {
        const cleaned = part.replace(/[√-]/g, "");
        let cssClass = "seg-root";
        if (prefixes.some((prefix) => cleaned.includes(prefix) || prefix.includes(cleaned))) {
          cssClass = "seg-prefix";
        } else if (suffixes.some((suffix) => cleaned.includes(suffix) || suffix.includes(cleaned))) {
          cssClass = "seg-suffix";
        } else if (roots.some((root) => cleaned.includes(root) || root.includes(cleaned))) {
          cssClass = "seg-root";
        }

        const plus = index < parts.length - 1 ? '<span class="seg-plus">+</span>' : "";
        return `<span class="seg-piece"><span class="seg-label ${cssClass}">${esc(
          part
        )}</span>${plus}</span>`;
      })
      .join("");
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

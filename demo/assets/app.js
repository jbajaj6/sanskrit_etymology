(function () {
  "use strict";

  const terms = Array.isArray(window.TERMS_DATA) ? window.TERMS_DATA : [];
  const searchEl = document.getElementById("search");
  const suggestionsEl = document.getElementById("suggestions");
  const browseEl = document.getElementById("browse");
  const resultEl = document.getElementById("result");
  const termGridEl = document.getElementById("termGrid");

  let activeIndex = -1;

  if (!terms.length) {
    resultEl.style.display = "block";
    resultEl.innerHTML = '<div class="empty-state">Demo data not loaded. Run <code>sanskrit-etymology build-demo</code>.</div>';
    return;
  }

  renderGrid();

  searchEl.addEventListener("input", () => {
    const query = searchEl.value.trim().toLowerCase();
    activeIndex = -1;
    if (!query) {
      hideSuggestions();
      return;
    }

    const matches = terms.filter((term) =>
      (term.search_aliases || []).some((alias) => alias.startsWith(query)) ||
      (term.devanagari || "").includes(query) ||
      (term.transliteration || "").toLowerCase().includes(query)
    );
    showSuggestions(matches);
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

    if (event.key === "Enter") {
      event.preventDefault();
      if (activeIndex >= 0 && items[activeIndex]) {
        selectTerm(items[activeIndex].dataset.id);
        return;
      }
      if (items.length > 0) {
        selectTerm(items[0].dataset.id);
      }
    }
  });

  document.addEventListener("click", (event) => {
    const suggestion = event.target.closest(".suggestion-item");
    if (suggestion) {
      selectTerm(suggestion.dataset.id);
      return;
    }

    const chip = event.target.closest(".term-chip");
    if (chip) {
      selectTerm(chip.dataset.id);
      return;
    }

    const backButton = event.target.closest(".back-btn");
    if (backButton) {
      goBack();
      return;
    }

    if (!event.target.closest(".search-container") && !event.target.closest(".suggestions")) {
      hideSuggestions();
    }
  });

  function renderGrid() {
    termGridEl.innerHTML = terms
      .map(
        (term) => `
          <div class="term-chip" data-id="${term.id}">
            <span class="chip-deva">${term.devanagari}</span>
            ${term.transliteration}
          </div>
        `
      )
      .join("");
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
        (term) => `
          <div class="suggestion-item" data-id="${term.id}">
            <span class="suggestion-deva">${term.devanagari}</span>
            <span class="suggestion-iast">${term.transliteration}</span>
            <span class="suggestion-gloss">${truncate(term.literal_gloss, 40)}</span>
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

  function selectTerm(termId) {
    const term = terms.find((candidate) => candidate.id === termId);
    if (!term) {
      return;
    }

    hideSuggestions();
    searchEl.value = "";
    browseEl.style.display = "none";
    resultEl.style.display = "block";
    resultEl.innerHTML = renderCard(term);
    resultEl.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function goBack() {
    resultEl.style.display = "none";
    resultEl.innerHTML = "";
    browseEl.style.display = "block";
    searchEl.focus();
  }

  function renderCard(term) {
    const segmentation = buildSegmentation(term);
    const morphologyCards = buildMorphologyCards(term);
    const chineseSection = buildChineseSection(term);
    const compoundSection = term.compound_type
      ? `
        <div class="card-section">
          <div class="section-label">Compound Type</div>
          <div class="section-content">${term.compound_type}</div>
        </div>
      `
      : "";
    const ambiguitySection = term.ambiguity_notes
      ? `
        <div class="card-section">
          <div class="section-label">Scholarly Notes</div>
          <div class="section-content serif">${term.ambiguity_notes}</div>
        </div>
      `
      : "";
    const confidenceClass =
      term.confidence === "high" ? "conf-high" : term.confidence === "medium" ? "conf-medium" : "conf-low";

    return `
      <button class="back-btn">← Back to term list</button>
      <div class="result-card">
        <div class="card-header">
          <span class="card-confidence ${confidenceClass}">${term.confidence} confidence</span>
          <div class="card-deva">${term.devanagari || ""}</div>
          <div class="card-iast">${term.transliteration || ""}</div>
          <div class="card-gloss-short">${term.literal_gloss || ""}</div>
        </div>

        <div class="segmentation-strip">${segmentation}</div>

        <div class="card-body">
          <div class="card-section">
            <div class="section-label">Morphological Components</div>
            <div class="morph-grid">${morphologyCards}</div>
          </div>

          ${compoundSection}

          <div class="card-section">
            <div class="section-label">Yoga Sutras Reference</div>
            <div class="section-content"><span class="chapter-ref">${term.chapter}</span></div>
          </div>

          <div class="card-section">
            <div class="section-label">Philosophical Meaning</div>
            <div class="section-content serif">${term.philosophical_gloss}</div>
          </div>

          <div class="card-section">
            <div class="section-label">Doctrinal Significance</div>
            <div class="section-content serif">${term.doctrinal_significance}</div>
          </div>

          ${chineseSection}
          ${ambiguitySection}
        </div>
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
            <div class="morph-type">${card.type}</div>
            <div class="morph-value">${card.value}</div>
            <div class="morph-meaning">${card.meaning}</div>
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
            <div class="chinese-chars">${candidate.characters}</div>
            <div class="chinese-pinyin">${candidate.pinyin}</div>
            <span class="chinese-type type-${mappingType.replace(/\s/g, "_")}">
              ${mappingType.replace(/_/g, " ")}
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
        return `<span class="seg-piece"><span class="seg-label ${cssClass}">${part}</span>${plus}</span>`;
      })
      .join("");
  }

  function truncate(text, maxLength) {
    if (!text) {
      return "";
    }
    return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
  }
})();

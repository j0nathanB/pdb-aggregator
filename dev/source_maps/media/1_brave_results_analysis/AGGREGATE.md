# Aggregate Analysis: EN vs Local Brave News Search

**Generated:** 2026-03-20
**Countries analyzed:** 28

---

## Global Summary

| Metric | Value |
|--------|-------|
| Total EN results | 3623 |
| Total Local results | 2355 |
| Overall URL overlap | 49.7% |
| EN-only URLs | 1638 |
| Local-only URLs | 370 |
| Shared URLs | 1985 |

---

## Country Classification

### Largely Identical (0 countries)

EN and Local return >85% the same URLs. **EN search alone is sufficient.**

*(none)*

### EN Yields Better Results (0 countries)

EN search returns 30%+ more results. **EN is the primary search; local adds marginal value.**

*(none)*

### Local Yields Better Results (0 countries)

Local search returns 30%+ more results. **Both searches recommended for maximum coverage.**

*(none)*

### Mixed / Close (17 countries)

Neither approach is clearly dominant (<30% difference). **Running both provides marginal additional coverage.**

| Country | EN results | Local results | Overlap |
|---------|-----------|--------------|---------|
| Australia | 108 | 108 | 76% |
| Brazil | 157 | 157 | 61% |
| Canada | 166 | 169 | 71% |
| Chile | 173 | 173 | 84% |
| Finland | 128 | 130 | 77% |
| France | 150 | 150 | 70% |
| Germany | 139 | 142 | 67% |
| Italy | 140 | 140 | 64% |
| Japan | 116 | 117 | 65% |
| Mexico | 170 | 169 | 70% |
| Poland | 126 | 132 | 74% |
| South Korea | 112 | 110 | 80% |
| Spain | 154 | 152 | 80% |
| Sweden | 130 | 130 | 79% |
| Taiwan | 116 | 104 | 73% |
| Turkey | 140 | 140 | 82% |
| United Kingdom | 132 | 132 | 68% |

### Local Search Broken (11 countries)

Brave API rejected `ui_lang` parameter — locale not supported. **EN search is the only option.**

| Country | Local params | EN results | Issue |
|---------|-------------|-----------|-------|
| Czech Republic | ui_lang=cs-CZ | 137 | `ui_lang` not in Brave's supported set |
| Estonia | ui_lang=et-EE | 88 | `ui_lang` not in Brave's supported set |
| India | ui_lang=hi-IN | 178 | `ui_lang` not in Brave's supported set |
| Indonesia | ui_lang=id-ID | 130 | `ui_lang` not in Brave's supported set |
| Latvia | ui_lang=lv-LV | 78 | `ui_lang` not in Brave's supported set |
| Lithuania | ui_lang=lt-LT | 65 | `ui_lang` not in Brave's supported set |
| Norway | ui_lang=nb-NO | 164 | `ui_lang` not in Brave's supported set |
| Romania | ui_lang=ro-RO | 110 | `ui_lang` not in Brave's supported set |
| Saudi Arabia | ui_lang=ar-SA | 86 | `ui_lang` not in Brave's supported set |
| Uae | ui_lang=ar-AE | 102 | `ui_lang` not in Brave's supported set |
| Ukraine | ui_lang=uk-UA | 128 | `ui_lang` not in Brave's supported set |

---

## Recommendations

### Why EN and Local often return the same results

- The `site:` operator in the query anchors results to a specific domain, which is the dominant filter
- Brave's news index appears to return the same articles regardless of `search_lang` for most domains
- The `search_lang` and `country` parameters primarily affect ranking and snippet language, not the underlying index
- For English-language domains (e.g., `reuters.com`, `theguardian.com`), language settings have no effect

### When local search adds value

- Countries with primarily non-English media and where Brave has good local-language indexing
- Sources that publish in multiple languages — local search may surface the native-language edition
- Countries where the local search found unique URLs not in the EN results

### Pipeline recommendation

1. **Default to EN search** — it provides the broadest coverage and works for all countries
2. **Add local search only for countries where it demonstrably adds unique content** (see 'Local Yields Better' category above)
3. **Skip local search for countries with broken locale support** — use EN only
4. **For countries with identical results** — running both is redundant; use EN only to halve API costs

---

## Full Country Comparison Table

| Country | Leader | EN | Local | Overlap | EN-only | Local-only | Category |
|---------|--------|-----|-------|---------|---------|------------|----------|
| Australia | Anthony Albanese | 108 | 108 | 76% | 15 | 15 | mixed |
| Brazil | Lula | 157 | 157 | 61% | 38 | 38 | mixed |
| Canada | Mark Carney | 166 | 169 | 71% | 27 | 30 | mixed |
| Chile | Gabriel Boric | 173 | 173 | 84% | 15 | 15 | mixed |
| Czech Republic | Petr Fiala | 137 | 0 | 0% | 137 | 0 | broken |
| Estonia | Kristen Michal | 88 | 0 | 0% | 88 | 0 | broken |
| Finland | Petteri Orpo | 128 | 130 | 77% | 16 | 18 | mixed |
| France | Emmanuel Macron | 150 | 150 | 70% | 26 | 26 | mixed |
| Germany | Friedrich Merz | 139 | 142 | 67% | 26 | 29 | mixed |
| India | Narendra Modi | 178 | 0 | 0% | 178 | 0 | broken |
| Indonesia | Prabowo Subianto | 130 | 0 | 0% | 130 | 0 | broken |
| Italy | Giorgia Meloni | 140 | 140 | 64% | 31 | 31 | mixed |
| Japan | Shigeru Ishiba | 116 | 117 | 65% | 24 | 25 | mixed |
| Latvia | Evika Silina | 78 | 0 | 0% | 78 | 0 | broken |
| Lithuania | Gintautas Paluckas | 65 | 0 | 0% | 65 | 0 | broken |
| Mexico | Claudia Sheinbaum | 170 | 169 | 70% | 30 | 29 | mixed |
| Norway | Jonas Gahr Store | 164 | 0 | 0% | 164 | 0 | broken |
| Poland | Donald Tusk | 126 | 132 | 74% | 16 | 22 | mixed |
| Romania | Nicusor Dan | 110 | 0 | 0% | 110 | 0 | broken |
| Saudi Arabia | Mohammed bin Salman | 86 | 0 | 0% | 86 | 0 | broken |
| South Korea | Lee Jae-myung | 112 | 110 | 80% | 13 | 11 | mixed |
| Spain | Pedro Sanchez | 154 | 152 | 80% | 18 | 16 | mixed |
| Sweden | Ulf Kristersson | 130 | 130 | 79% | 15 | 15 | mixed |
| Taiwan | Lai Ching-te | 116 | 104 | 73% | 23 | 11 | mixed |
| Turkey | Recep Tayyip Erdogan | 140 | 140 | 82% | 14 | 14 | mixed |
| Uae | Mohammed bin Zayed | 102 | 0 | 0% | 102 | 0 | broken |
| Ukraine | Volodymyr Zelenskyy | 128 | 0 | 0% | 128 | 0 | broken |
| United Kingdom | Keir Starmer | 132 | 132 | 68% | 25 | 25 | mixed |
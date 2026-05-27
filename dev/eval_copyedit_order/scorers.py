"""
Mechanical scorers for the copyedit/style-edit order evaluation.

Each scorer takes a prose string (or a parsed dict of prose fields) and
returns a list of hit records — location, snippet, and a kind tag. Counts
are derived by len(hits). Scorers are deliberately conservative about what
they flag; the eval reports deltas vs a baseline, not absolute counts (see
eval plan note on stale-titles precision).
"""

import re
from dataclasses import dataclass
from typing import Iterable


# Acronyms considered "common knowledge" per the copyeditor prompt's
# familiar-abbreviation list, plus common wire-copy shorthand the prompt
# clearly expects.
FAMILIAR_ACRONYMS: set[str] = {
    "AIDS", "BBC", "CIA", "EU", "FBI", "GDP", "HIV", "IMF", "NASA", "NATO",
    "NGO", "OECD", "UNESCO", "DNA", "AWACS",
    "UN", "US", "USA", "UK", "UAE", "EEA", "EEZ",
    "G7", "G20", "ECB", "WTO", "ICBM", "PM", "CEO", "CFO", "COO",
    "AI", "IT", "TV", "OK",
    # Country-codes that recur as adjectives/nouns and aren't really acronyms
    # (rare in prose but harmless)
}

# An acronym is 2–5 consecutive uppercase letters, optionally trailing 's'.
_ACRONYM_RE = re.compile(r"\b([A-Z]{2,5})(s)?\b")

# An "intro" looks like: `Foo Bar Baz (ACR)` — one or more title-cased or
# all-caps words immediately followed by `(XYZ)`. Matches the convention the
# copyeditor prompt enforces.
_PAREN_INTRO_RE = re.compile(
    r"((?:[A-Z][A-Za-zÀ-ÿ'’\-]+\s+){1,6})\(([A-Z]{2,5})\)"
)


@dataclass(frozen=True)
class Hit:
    kind: str
    offset: int
    snippet: str
    extra: dict

    def to_dict(self) -> dict:
        return {"kind": self.kind, "offset": self.offset, "snippet": self.snippet, **self.extra}


# ---------------------------------------------------------------------------
# Text extraction helpers
# ---------------------------------------------------------------------------

PROSE_FIELDS_ORDER = ("narrative_body", "regional_lead", "edited_essay",
                      "card_summary", "headline")


def extract_prose(parsed: dict | str) -> str:
    """Flatten a parsed-output dict into a single prose string for scoring.

    Joins known prose fields in a stable order separated by double newlines.
    Unknown string values are appended at the end so nothing is silently
    dropped.
    """
    if isinstance(parsed, str):
        return parsed
    if not isinstance(parsed, dict):
        return ""

    parts: list[str] = []
    seen: set[str] = set()
    for key in PROSE_FIELDS_ORDER:
        val = parsed.get(key)
        if isinstance(val, str) and val.strip():
            parts.append(val)
            seen.add(key)
    for key, val in parsed.items():
        if key in seen:
            continue
        if isinstance(val, str) and val.strip():
            parts.append(val)
        elif isinstance(val, list):
            # handle e.g. other_stories, items, gap_paragraphs
            for item in val:
                if isinstance(item, str) and item.strip():
                    parts.append(item)
                elif isinstance(item, dict):
                    for vv in item.values():
                        if isinstance(vv, str) and vv.strip():
                            parts.append(vv)
    return "\n\n".join(parts)


def _snippet(text: str, start: int, end: int, pad: int = 40) -> str:
    lo = max(0, start - pad)
    hi = min(len(text), end + pad)
    s = text[lo:hi]
    return s.replace("\n", " ").strip()


# ---------------------------------------------------------------------------
# Scorer 1: bare acronyms (not in familiar list and never introduced)
# ---------------------------------------------------------------------------

def _introduced_acronyms(text: str) -> set[str]:
    return {m.group(2) for m in _PAREN_INTRO_RE.finditer(text)}


def score_bare_acronyms(text: str) -> list[Hit]:
    introduced = _introduced_acronyms(text) | FAMILIAR_ACRONYMS
    hits: list[Hit] = []
    for m in _ACRONYM_RE.finditer(text):
        acr = m.group(1)
        if acr in introduced:
            continue
        # Skip the capture when it's the intro itself — guard against
        # `(ACR)` being flagged as bare when the preceding phrase wasn't
        # in title case.
        before = text[max(0, m.start() - 2):m.start()]
        if before.endswith("("):
            continue
        hits.append(Hit(
            kind="bare_acronym",
            offset=m.start(),
            snippet=_snippet(text, m.start(), m.end()),
            extra={"acronym": acr},
        ))
    return hits


# ---------------------------------------------------------------------------
# Scorer 2: acronym chain breaks (bare mention precedes its paren intro)
# ---------------------------------------------------------------------------

def score_acronym_chain_breaks(text: str) -> list[Hit]:
    intros: dict[str, int] = {}
    for m in _PAREN_INTRO_RE.finditer(text):
        intros.setdefault(m.group(2), m.start())
    hits: list[Hit] = []
    for m in _ACRONYM_RE.finditer(text):
        acr = m.group(1)
        if acr in FAMILIAR_ACRONYMS:
            continue
        intro_pos = intros.get(acr)
        if intro_pos is None:
            continue  # no intro at all — bare_acronyms scorer owns this case
        if m.start() < intro_pos:
            hits.append(Hit(
                kind="acronym_chain_break",
                offset=m.start(),
                snippet=_snippet(text, m.start(), m.end()),
                extra={"acronym": acr, "intro_offset": intro_pos},
            ))
    return hits


# ---------------------------------------------------------------------------
# Scorer 3: stale titles vs leader reference
#
# Low precision — see eval plan. Reports deltas vs baseline, not absolute
# counts. The filter below skips obvious false positives from constructions
# like "Mexico's president Sheinbaum" and "Minister for X met with …".
# ---------------------------------------------------------------------------

TITLE_NOUNS = [
    "prime minister", "foreign minister", "finance minister", "defense minister",
    "defence minister", "interior minister", "economy minister", "trade minister",
    "energy minister", "justice minister", "health minister", "environment minister",
    "president", "chancellor", "premier", "taoiseach", "secretary",
    "chairman", "chairwoman", "chair", "speaker", "envoy",
    "general", "admiral", "colonel", "commander", "ambassador", "governor",
]
# Longer names first so "foreign minister" matches before "minister"
TITLE_NOUNS = sorted(TITLE_NOUNS, key=len, reverse=True)
_TITLE_RE = re.compile(r"\b(" + "|".join(re.escape(t) for t in TITLE_NOUNS) + r")\b",
                        re.IGNORECASE)

_POSSESSIVE_FILTER = re.compile(r"[’']s\s+$|\bof\b\s+$|\bfor\b\s+$")


_APPOSITIVE_TITLE_RE = re.compile(
    r"^\s*,?\s*(?:the\s+|a\s+)?(" + "|".join(re.escape(t) for t in TITLE_NOUNS) + r")\b",
    re.IGNORECASE,
)


def score_stale_titles(text: str, leader_refs: dict[str, str]) -> list[Hit]:
    """leader_refs: {full_name: current_role_string}. Flag when a title noun
    immediately preceding a mention of `name` is not part of the current role.

    Guards against common false positives:
    - If the name is immediately followed by `, the <title>` (appositive),
      use that as ground truth and skip preceding-title matching entirely.
    - Skip "Mexico's president Sheinbaum" style bindings (possessive filter).
    - Skip when the preceding title is separated by more than ~4 words.
    """
    hits: list[Hit] = []
    for name, current_role in leader_refs.items():
        if not name or not current_role:
            continue
        current_role_lower = _normalize_role(current_role)
        name_re = re.compile(r"\b" + re.escape(name) + r"\b")
        for m in name_re.finditer(text):
            # Appositive after the name wins — e.g. "Petr Pavel, the president"
            after = text[m.end():m.end() + 80]
            ap = _APPOSITIVE_TITLE_RE.match(after)
            if ap is not None:
                ap_title = _normalize_role(ap.group(1))
                if ap_title in current_role_lower:
                    continue  # matches current role
                # Appositive that doesn't match current role = real stale title
                hits.append(Hit(
                    kind="stale_title",
                    offset=m.start(),
                    snippet=_snippet(text, m.start(), m.end(), pad=60),
                    extra={"name": name, "flagged_title": ap_title,
                           "current_role": current_role,
                           "source": "appositive"},
                ))
                continue

            before = text[max(0, m.start() - 60):m.start()]
            title_match = None
            for tm in _TITLE_RE.finditer(before):
                title_match = tm  # keep last (nearest preceding)
            if title_match is None:
                continue
            title_text = _normalize_role(title_match.group(1))
            if title_text in current_role_lower:
                continue
            between = before[title_match.end():]
            if _POSSESSIVE_FILTER.search(between):
                continue
            # Require the title to be tightly bound — <=4 words between title and name
            if len(between.split()) > 4:
                continue
            hits.append(Hit(
                kind="stale_title",
                offset=m.start(),
                snippet=_snippet(text, m.start(), m.end(), pad=60),
                extra={"name": name, "flagged_title": title_text,
                       "current_role": current_role,
                       "source": "preceding"},
            ))
    return hits


# ---------------------------------------------------------------------------
# Scorer 4: foreign-quote leakage
# ---------------------------------------------------------------------------

_QUOTE_SPAN_RE = re.compile(
    r'"([^"\n]{3,400})"|"([^"\n]{3,400})"|«([^»\n]{3,400})»|“([^”\n]{3,400})”'
)

_FOREIGN_CHAR_RE = re.compile(r"[áéíóúñüöäßçõàèìòùâêîôûÁÉÍÓÚÑÜÖÄÇÕÀÈÌÒÙÂÊÎÔÛ]")

# Lowercase-token spotter — used to tell whether a non-ASCII letter sits
# inside a lowercase word (likely non-English running prose) vs. a
# capitalized token (likely a transliterated proper noun like "Orbán").
_LOWERCASE_TOKEN_WITH_DIACRITIC_RE = re.compile(
    r"\b[a-z]*[áéíóúñüöäßçõàèìòùâêîôûÁÉÍÓÚÑÜÖÄÇÕÀÈÌÒÙÂÊÎÔÛ][a-záéíóúñüöäßçõàèìòùâêîôû]+\b"
)

# Small set of high-signal non-English function words. Intentionally narrow
# and excluding words that collide with common English (e.g. "die", "una",
# "sur"). We only flag words that are extremely unlikely to appear in an
# English quote.
_FOREIGN_WORD_RE = re.compile(
    r"\b(que|nicht|sondern|n[aã]o|del(?:la|lo|le)?|qu'|c'est|"
    r"sulla|dello|dei|delle|avec)\b",
    re.IGNORECASE,
)


def score_foreign_quote_leakage(text: str) -> list[Hit]:
    hits: list[Hit] = []
    for m in _QUOTE_SPAN_RE.finditer(text):
        span = next((g for g in m.groups() if g), "")
        reason = None
        # Diacritic in a lowercase token = strong non-English signal.
        # A diacritic only in capitalized tokens (Orbán, Médecins) is fine.
        if _LOWERCASE_TOKEN_WITH_DIACRITIC_RE.search(span):
            reason = "non_english_char"
        elif _FOREIGN_WORD_RE.search(span):
            reason = "non_english_word"
        if reason is None:
            continue
        hits.append(Hit(
            kind="foreign_quote_leakage",
            offset=m.start(),
            snippet=_snippet(text, m.start(), m.end(), pad=20),
            extra={"reason": reason, "span": span[:120]},
        ))
    return hits


# ---------------------------------------------------------------------------
# Convenience — run all scorers and report counts
# ---------------------------------------------------------------------------

def score_all(text: str, leader_refs: dict[str, str] | None = None) -> dict:
    return {
        "bare_acronyms": [h.to_dict() for h in score_bare_acronyms(text)],
        "acronym_chain_breaks": [h.to_dict() for h in score_acronym_chain_breaks(text)],
        "stale_titles": [h.to_dict() for h in score_stale_titles(text, leader_refs or {})],
        "foreign_quote_leakage": [h.to_dict() for h in score_foreign_quote_leakage(text)],
    }


def counts(result: dict) -> dict[str, int]:
    return {k: len(v) for k, v in result.items()}


# ---------------------------------------------------------------------------
# Leader reference loader (mirrors structured_copyeditor._build_leader_reference)
# ---------------------------------------------------------------------------

_INDIVIDUAL_ROLE_RE = re.compile(
    r"\b(" + "|".join(re.escape(t) for t in TITLE_NOUNS) + r")\b", re.IGNORECASE,
)


def _role_is_individual(role: str) -> bool:
    """True when the role string names an individual's title.

    Country configs mix individuals (name="Angela Merkel", role="Chancellor")
    with institutions (name="KMT", role="Main opposition (Kuomintang)"). Only
    the former should seed stale-title checks — institutional "roles" are
    party descriptions and trigger false positives.
    """
    return bool(_INDIVIDUAL_ROLE_RE.search(role))


_SPELLING_VARIANTS = {
    "defence": "defense",
    "labour": "labor",
    "programme": "program",
    "organisation": "organization",
}


def _normalize_role(role: str) -> str:
    r = role.lower()
    for uk, us in _SPELLING_VARIANTS.items():
        r = r.replace(uk, us)
    return r


def load_leader_refs(codes: Iterable[str]) -> dict[str, str]:
    """Load {name: role} for all actors across the given country codes.

    Mirrors production's _build_leader_reference with two filters:
    - Only actors whose role looks like an individual title (not a party
      description) are returned.
    - UK/US spelling variants are normalised so "Defense Minister" in the
      config matches "defence minister" in prose.
    """
    from monitor.config import load_country_config
    refs: dict[str, str] = {}
    for code in codes:
        try:
            cfg = load_country_config(code)
        except FileNotFoundError:
            continue
        for a in cfg.actors:
            if a.name and a.role and _role_is_individual(a.role):
                refs[a.name] = a.role
    return refs

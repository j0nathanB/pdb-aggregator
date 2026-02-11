"""
Snippet embedding and pre-filtering using sentence-transformers.
"""
import logging
import re
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)

# Unified multilingual model - all leaders use the same model for cross-lingual comparability
# E5 models use instruction prefixes: "query: " for queries, "passage: " for documents
DEFAULT_MODEL = "intfloat/multilingual-e5-small"

# Models that require instruction prefixes for optimal performance
E5_MODELS = {"intfloat/multilingual-e5-small", "intfloat/multilingual-e5-base", "intfloat/multilingual-e5-large"}

OPINION_MARKERS = [
    "opinion:", "opinion |", "editorial:", "analysis:",
    "column:", "commentary:", "perspective:",
]


@dataclass
class EmbeddedSnippet:
    """A search result with its embedding."""
    title: str
    snippet: str
    url: str
    source_name: str
    source_type: str  # "wire" or "domestic"
    date: str
    embedding: np.ndarray


def _parse_name_parts(leader_name: str) -> list[str]:
    """
    Parse a leader name into searchable parts, keeping compound surnames together.

    Examples:
        "Lula da Silva" -> ["lula", "da silva"]
        "Ursula von der Leyen" -> ["ursula", "von der leyen"]
        "Mark Carney" -> ["mark", "carney"]
    """
    # Particles that indicate compound surnames (Portuguese, German, Dutch, etc.)
    COMPOUND_PARTICLES = {"da", "de", "do", "dos", "das", "von", "van", "der", "la", "le", "del", "di"}

    words = leader_name.lower().split()
    parts = []
    i = 0

    while i < len(words):
        word = words[i]

        # Check if this starts a compound surname (particle + following words)
        if word in COMPOUND_PARTICLES and i + 1 < len(words):
            # Collect all consecutive particles and the final surname
            compound = [word]
            j = i + 1
            while j < len(words):
                if words[j] in COMPOUND_PARTICLES:
                    compound.append(words[j])
                    j += 1
                else:
                    compound.append(words[j])
                    break
            parts.append(" ".join(compound))
            i = j + 1
        else:
            parts.append(word)
            i += 1

    return parts


def _build_name_pattern(name_part: str) -> re.Pattern:
    """
    Build a regex pattern that matches a name part with grammatical variations.

    Handles:
    - Slavic declensions (Tusk -> Tuska, Tuskiem, Tusku, Tuskowi)
    - Ukrainian/Russian variations (Zelenskyy -> Zelenskya, Zelenskyego)
    - Transliteration variants (Zelenskyy/Zelensky/Zelenskiy)

    Args:
        name_part: A single name part (e.g., "tusk", "zelenskyy")

    Returns:
        Compiled regex pattern
    """
    # For very short names (<=4 chars), require near-exact match to avoid false positives
    if len(name_part) <= 4:
        # Allow only 1-2 char suffix for short names
        return re.compile(rf"\b{re.escape(name_part)}[a-ząćęłńóśźżа-яіїєґ]{{0,2}}\b", re.IGNORECASE)

    # For names ending in consonant + y/i variations (Slavic names)
    # e.g., Zelenskyy, Zelensky, Zelenskiy -> stem is "zelensk"
    if name_part.endswith(("yy", "ky", "iy", "yi", "ii")):
        stem = re.sub(r"[yi]+$", "", name_part)
        if len(stem) >= 4:
            # Match stem + various endings (y, yy, iy, yi, ya, yego, etc.)
            return re.compile(rf"\b{re.escape(stem)}[yiї]{{0,3}}[a-ząćęłńóśźżа-яіїєґ]{{0,4}}\b", re.IGNORECASE)

    # For names ending in vowels, the stem is usually name minus the vowel
    if name_part.endswith(("a", "e", "i", "o", "u", "y")):
        stem = name_part[:-1]
        if len(stem) >= 4:
            # Match stem + up to 4 chars (covers most declensions)
            return re.compile(rf"\b{re.escape(stem)}[a-ząćęłńóśźżа-яіїєґ]{{0,5}}\b", re.IGNORECASE)

    # Default: match name + optional suffix for grammatical endings
    # Covers Polish: Tusk -> Tuska, Tuskiem, Tusku, Tuskowi
    return re.compile(rf"\b{re.escape(name_part)}[a-ząćęłńóśźżа-яіїєґ]{{0,5}}\b", re.IGNORECASE)


def filter_relevant(snippets: list[dict], leader_name: str) -> list[dict]:
    """
    Filter snippets to those mentioning the leader by name.

    Handles grammatical variations common in Slavic and other languages:
    - Polish declensions (Tusk -> Tuska, Tuskiem)
    - Ukrainian variations (Zelenskyy -> Zelenskya)
    - Transliteration variants

    Args:
        snippets: Raw search result dicts
        leader_name: Full name (e.g. "Mark Carney")

    Returns:
        Snippets that mention the leader's surname (required) or full name
    """
    name_parts = _parse_name_parts(leader_name)
    # Build regex patterns for each name part
    patterns = [_build_name_pattern(part) for part in name_parts]

    # The surname is the last name part (e.g., "carney" for "Mark Carney",
    # "da silva" for "Lula da Silva"). Surname match is required to avoid
    # false positives from common first names like "Mark" matching "Mark Kelly".
    surname_pattern = patterns[-1] if patterns else None

    relevant = []

    for s in snippets:
        text = f"{s['title']} {s.get('snippet', '')}".lower()
        # Require surname match (avoids "Mark Kelly" matching "Mark Carney")
        if surname_pattern and surname_pattern.search(text):
            relevant.append(s)

    removed = len(snippets) - len(relevant)
    if removed:
        logger.info(f"Relevance filter: kept {len(relevant)}, removed {removed}")

    return relevant


def separate_opinions(snippets: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Separate opinion/commentary from hard news.

    Args:
        snippets: Search result dicts

    Returns:
        Tuple of (news, opinions)
    """
    # Subjective phrases that indicate opinion/commentary
    OPINION_PHRASES = [
        "sadly,", "unfortunately,", "should be", "must be", "needs to",
        "here's why", "here is why", "what we know", "what you need to know",
        "my take", "i think", "i believe", "in my view",
    ]

    news, opinions = [], []

    for s in snippets:
        title = s["title"]
        title_lower = title.lower()

        is_opinion = False

        # Check section markers
        for marker in OPINION_MARKERS:
            if marker in title_lower:
                is_opinion = True
                break

        # Check byline pattern: "Firstname Lastname: headline"
        if not is_opinion and ": " in title:
            before_colon = title.split(":")[0].strip()
            words = before_colon.split()
            if 2 <= len(words) <= 3 and all(w[0].isupper() for w in words if w):
                is_opinion = True

        # Check for opinion phrases (subjective language)
        if not is_opinion:
            for phrase in OPINION_PHRASES:
                if phrase in title_lower:
                    is_opinion = True
                    break

        (opinions if is_opinion else news).append(s)

    if opinions:
        logger.info(f"Opinion filter: {len(news)} news, {len(opinions)} opinion/commentary")

    return news, opinions


def _strip_leader_name(text: str, leader_name: str) -> str:
    """Remove leader name variants from text before embedding.

    Builds regex variants from the full name:
      "Volodymyr Zelenskyy" -> matches Zelenskyy, Zelensky, Zelenskiy,
      Volodymyr Zelenskyy, etc.
    """
    parts = leader_name.strip().split()
    # Build patterns for full name and each individual part (2+ chars)
    variants = [re.escape(leader_name)]
    for part in parts:
        if len(part) >= 2:
            # Handle common transliteration variants (ky/kiy/kyy endings)
            variants.append(re.escape(part).rstrip("y") + r"y{0,2}(?:iy)?")
    pattern = re.compile(r"\b(?:" + "|".join(variants) + r")\b", re.IGNORECASE)
    stripped = pattern.sub("", text)
    # Collapse extra whitespace left behind
    return re.sub(r"  +", " ", stripped).strip()


class SnippetEmbedder:
    """Embeds search result snippets for clustering."""

    _model_cache: dict[str, SentenceTransformer] = {}

    def __init__(self, model_name: str = DEFAULT_MODEL):
        self.model_name = model_name
        self.uses_e5_prefix = model_name in E5_MODELS
        if model_name not in SnippetEmbedder._model_cache:
            logger.info(f"Loading embedding model: {model_name}")
            SnippetEmbedder._model_cache[model_name] = SentenceTransformer(model_name)
        self.model = SnippetEmbedder._model_cache[model_name]

    def embed_snippets(
        self,
        snippets: list[dict],
        leader_name: str | None = None,
    ) -> list[EmbeddedSnippet]:
        """
        Embed a batch of search result snippets.

        Args:
            snippets: List of dicts with title, snippet, url, source_name, source_type, date
            leader_name: If provided, strip leader name variants from text before
                embedding so the model focuses on topical content rather than the
                shared subject.

        Returns:
            List of EmbeddedSnippet with embeddings
        """
        texts = [f"{s['title']} {s.get('snippet', '')}" for s in snippets]

        if leader_name:
            texts = [_strip_leader_name(t, leader_name) for t in texts]

        # E5 models perform better with instruction prefixes
        # Using "passage: " for documents being indexed/compared
        if self.uses_e5_prefix:
            texts = [f"passage: {t}" for t in texts]

        embeddings = self.model.encode(texts, normalize_embeddings=True)

        return [
            EmbeddedSnippet(
                title=s["title"],
                snippet=s.get("snippet", ""),
                url=s["url"],
                source_name=s["source_name"],
                source_type=s.get("source_type", "domestic"),
                date=s.get("date", ""),
                embedding=emb,
            )
            for s, emb in zip(snippets, embeddings)
        ]

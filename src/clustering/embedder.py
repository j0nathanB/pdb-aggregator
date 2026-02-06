"""
Snippet embedding and pre-filtering using sentence-transformers.
"""
import logging
import re
from sentence_transformers import SentenceTransformer
from dataclasses import dataclass
import numpy as np

logger = logging.getLogger(__name__)

# Model choice: bge-small-en-v1.5 is fast and good on short text
DEFAULT_MODEL = "BAAI/bge-small-en-v1.5"

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


def filter_relevant(snippets: list[dict], leader_name: str) -> list[dict]:
    """
    Filter snippets to those mentioning the leader by name.

    Args:
        snippets: Raw search result dicts
        leader_name: Full name (e.g. "Mark Carney")

    Returns:
        Snippets that mention any part of the leader's name
    """
    name_parts = leader_name.lower().split()
    relevant = []

    for s in snippets:
        text = f"{s['title']} {s.get('snippet', '')}".lower()
        if any(part in text for part in name_parts):
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

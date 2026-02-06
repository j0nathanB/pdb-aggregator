"""
Diffbot NLP API integration for entity extraction and summarization.
"""
import logging
import httpx
from typing import Optional

from .core import DIFFBOT_TOKEN, TIMEOUT, HEADERS

logger = logging.getLogger(__name__)


async def extract_nlp(text: str, lang: str = "auto") -> Optional[dict]:
    """
    Extract entities and summary from text using Diffbot NLP API.

    Per the Diffbot NL API docs, the request body must be an array of
    document objects and the response is also an array.

    Args:
        text: Article text to analyze
        lang: Language code ("en", "es", "fr", "de", "zh", "ru", "ja",
              "nl", "pl", "no", "da", "sv", "it") or "auto" for
              auto-detection.

    Returns:
        Dict with entities, summary, sentiment, etc.
    """
    if not DIFFBOT_TOKEN:
        return None

    if not text or not text.strip():
        return None

    async with httpx.AsyncClient(timeout=TIMEOUT, headers=HEADERS) as client:
        try:
            response = await client.post(
                "https://nl.diffbot.com/v1/",
                params={
                    "token": DIFFBOT_TOKEN,
                    "fields": "entities,sentiment,facts,records,categories,sentences,language,summary",
                },
                json=[{
                    "content": text,
                    "lang": lang,
                    "format": "plain text",
                    "customSummary": {"maxNumberOfSentences": 10},
                    "documentType": "news article",
                }],
            )
            response.raise_for_status()
            result = response.json()
            # Response is also an array — take first element
            return result[0] if isinstance(result, list) and result else result

        except Exception as e:
            logger.error(f"Diffbot NLP error: {e}")
            return None


def extract_high_salience_entities(nlp_result: dict, threshold: float = 0.8) -> list[dict]:
    """
    Extract high-salience entities from Diffbot NLP result.

    Args:
        nlp_result: Raw Diffbot NLP response
        threshold: Minimum salience score (0-1)

    Returns:
        List of entity dicts with name, type, uri, salience
    """
    entities = []

    for entity in nlp_result.get("entities", []):
        salience = entity.get("salience", 0)
        if salience >= threshold:
            entities.append({
                "name": entity.get("name", ""),
                "type": entity["allTypes"][0].get("name", "unknown") if entity.get("allTypes") else "unknown",
                "uri": entity.get("diffbotUri", ""),
                "salience": salience,
            })

    return entities


def get_summary(nlp_result: dict) -> str:
    """Extract summary from Diffbot NLP result."""
    return nlp_result.get("summary", "")

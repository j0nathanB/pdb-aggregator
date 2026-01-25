"""
Translator Agent - Translates non-English articles.

Uses LLM translation with specialized prompting to preserve:
- Political nuance and connotation
- Cultural context
- Proper nouns and titles
"""

import logging
from typing import Optional

from ..config import Article
from .base import complete, with_retry, process_batch

logger = logging.getLogger(__name__)


TRANSLATION_SYSTEM = """You are a professional translator specializing in political and diplomatic content.

Your translation priorities:
1. ACCURACY: Preserve the exact meaning, especially for policy language and commitments
2. NUANCE: Maintain political connotations (e.g., "regime" vs "government", "militants" vs "freedom fighters")
3. CONTEXT: Add brief [translator notes] for culturally-specific references that need explanation
4. PROPER NOUNS: Keep names, titles, and organizations in their standard English forms

Format your output as:
[TRANSLATION]
<translated text>

[NOTES] (optional)
- Any important context about terminology or cultural references
"""


LANGUAGE_NAMES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "pl": "Polish",
    "fi": "Finnish",
    "uk": "Ukrainian",
    "zh": "Chinese",
    "ar": "Arabic",
    "ru": "Russian",
    "pt": "Portuguese",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
}


class TranslatorAgent:
    """
    Translates non-English article content to English.
    
    Optimized for political/diplomatic content with attention to
    nuance that might be lost in generic translation.
    """
    
    async def translate_batch(
        self,
        articles: list[Article],
        target_language: str = "en",
    ) -> list[Article]:
        """
        Translate all non-English articles in a batch.
        
        Articles already in the target language are passed through unchanged.
        
        Args:
            articles: List of articles to translate
            target_language: Target language code (default: English)
            
        Returns:
            Articles with translated_content populated where needed
        """
        # Filter to only articles needing translation
        needs_translation = [
            a for a in articles 
            if a.original_language != target_language and a.content
        ]
        
        if not needs_translation:
            logger.info("No articles need translation")
            return articles
        
        logger.info(f"Translating {len(needs_translation)} articles")
        
        # Translate in parallel with rate limiting
        async def translate_one(article: Article) -> Article:
            translated = await self.translate_article(article, target_language)
            return translated
        
        translated_articles = await process_batch(
            items=needs_translation,
            processor=translate_one,
            max_concurrent=3,
            desc="Translation",
        )
        
        # Build lookup of translated articles
        translated_lookup = {a.id: a for a in translated_articles if a}
        
        # Merge translations back into original list
        result = []
        for article in articles:
            if article.id in translated_lookup:
                result.append(translated_lookup[article.id])
            else:
                result.append(article)
        
        return result
    
    @with_retry(max_attempts=2)
    async def translate_article(
        self,
        article: Article,
        target_language: str = "en",
    ) -> Article:
        """
        Translate a single article.
        
        Args:
            article: Article to translate
            target_language: Target language code
            
        Returns:
            Article with translated_content populated
        """
        if article.original_language == target_language:
            return article
        
        if not article.content:
            return article
        
        source_lang = LANGUAGE_NAMES.get(
            article.original_language, 
            article.original_language
        )
        
        prompt = f"""Translate the following {source_lang} news article to English.

TITLE: {article.title}

CONTENT:
{article.content}

Remember to preserve political nuance and add translator notes for culturally-specific references.
"""
        
        response = await complete(
            prompt=prompt,
            system=TRANSLATION_SYSTEM,
            temperature=0.1,  # Low temperature for accuracy
        )
        
        # Parse translation and notes
        translation, notes = self._parse_translation(response)
        
        # Update article with translation
        article.translated_content = translation
        
        # Also translate title if present in response
        if article.title and article.original_language != "en":
            title_translation = await self._translate_title(article.title, source_lang)
            if title_translation:
                # Store original title and use translation
                article.title = f"{title_translation} [{article.title}]"
        
        return article
    
    async def _translate_title(self, title: str, source_lang: str) -> Optional[str]:
        """Translate just the article title."""
        prompt = f"""Translate this {source_lang} headline to English. 
Output ONLY the translated headline, nothing else.

{title}
"""
        
        try:
            response = await complete(
                prompt=prompt,
                temperature=0.1,
                max_tokens=200,
            )
            return response.strip()
        except Exception as e:
            logger.warning(f"Title translation failed: {e}")
            return None
    
    def _parse_translation(self, response: str) -> tuple[str, Optional[str]]:
        """
        Parse translation response into text and notes.
        
        Returns:
            Tuple of (translated_text, translator_notes)
        """
        translation = ""
        notes = None
        
        if "[TRANSLATION]" in response:
            parts = response.split("[TRANSLATION]")
            if len(parts) > 1:
                remaining = parts[1]
                
                if "[NOTES]" in remaining:
                    trans_part, notes_part = remaining.split("[NOTES]", 1)
                    translation = trans_part.strip()
                    notes = notes_part.strip()
                else:
                    translation = remaining.strip()
        else:
            # No markers, assume entire response is translation
            translation = response.strip()
        
        return translation, notes
    
    async def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str = "en",
        context: Optional[str] = None,
    ) -> str:
        """
        Translate arbitrary text (utility method).
        
        Args:
            text: Text to translate
            source_language: Source language code
            target_language: Target language code
            context: Optional context about the content
            
        Returns:
            Translated text
        """
        if source_language == target_language:
            return text
        
        source_name = LANGUAGE_NAMES.get(source_language, source_language)
        
        prompt = f"""Translate the following {source_name} text to English.
{f"Context: {context}" if context else ""}

TEXT:
{text}

Output ONLY the translation.
"""
        
        response = await complete(
            prompt=prompt,
            temperature=0.1,
        )
        
        return response.strip()

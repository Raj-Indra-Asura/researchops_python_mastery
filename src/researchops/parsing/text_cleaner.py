"""Text cleaning and normalisation utilities.

Used before keyword indexing and ML preprocessing to produce
clean, consistent text from raw PDF extractions.

Week 7 TODO:
- Add stop-word removal.
- Add stemming/lemmatisation option.
- Handle ligatures (ﬁ → fi, etc.) from PDF extraction artefacts.
"""

from __future__ import annotations

import re
import unicodedata


def clean_text(raw: str) -> str:
    """Return a cleaned version of raw extracted text.

    Operations performed (in order):
    1. Unicode NFKC normalisation (collapses ligatures, etc.).
    2. Remove control characters (except newline/tab).
    3. Collapse runs of whitespace to single spaces.
    4. Strip leading/trailing whitespace.
    """
    # 1. Normalise unicode
    text = unicodedata.normalize("NFKC", raw)

    # 2. Remove control characters (keep \n and \t)
    text = re.sub(r"[^\S\n\t]+", " ", text)
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)

    # 3. Collapse multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # 4. Strip
    return text.strip()


def normalise_for_search(text: str) -> str:
    """Aggressive normalisation for keyword indexing.

    Returns lowercase text with punctuation stripped, suitable for
    building an inverted index or simple keyword match.
    """
    text = clean_text(text)
    text = text.lower()
    # Keep only alphanumeric and whitespace
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    # Collapse whitespace
    return " ".join(text.split())

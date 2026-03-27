from __future__ import annotations

from collections import Counter
from math import sqrt


def embed_text(text: str) -> Counter[str]:
    tokens = [token.strip(".,:;!?").lower() for token in text.split() if token.strip()]
    return Counter(tokens)


def cosine_similarity(left: Counter[str], right: Counter[str]) -> float:
    if not left or not right:
        return 0.0
    overlap = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in overlap)
    left_norm = sqrt(sum(value * value for value in left.values()))
    right_norm = sqrt(sum(value * value for value in right.values()))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)

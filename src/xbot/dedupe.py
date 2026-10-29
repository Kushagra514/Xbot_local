import re


def _words(text):
    return {w for w in re.split(r"[^a-z0-9]+", text.lower()) if w}


def similarity(a, b):
    wa, wb = _words(a), _words(b)
    union = wa | wb
    if not union:
        return 0.0
    return len(wa & wb) / len(union)


def is_duplicate(text, past, threshold=0.6):
    return any(similarity(text, p) >= threshold for p in past)

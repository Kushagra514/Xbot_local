from urllib.parse import quote


def compose_url(text):
    if not text.strip():
        raise ValueError("empty text")
    if len(text) > 280:
        raise ValueError("text too long")
    return "https://x.com/intent/post?text=" + quote(text, safe="")

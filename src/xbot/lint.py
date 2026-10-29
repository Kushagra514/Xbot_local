BANNED = ("game-changer", "game changer", "unlock", "delve", "🚀", "thread 🧵")


def lint_post(text):
    if not text.strip():
        return ["empty"]
    problems = []
    if len(text) > 280:
        problems.append("too_long")
    if any(k in text for k in ("http://", "https://", "www.")):
        problems.append("has_link")
    lower = text.lower()
    if any(b in lower for b in BANNED):
        problems.append("banned_phrase")
    if sum(1 for w in text.split() if w.startswith("#")) > 2:
        problems.append("too_many_hashtags")
    return problems

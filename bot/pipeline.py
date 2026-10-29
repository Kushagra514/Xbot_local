"""Closed-loop draft pipeline for the Mode A X bot.

    python3 bot/pipeline.py              # draft one post from the first learning
    python3 bot/pipeline.py --all        # draft a post from every learning
    python3 bot/pipeline.py --rate <id> <rating>  # log human feedback (1-5)

Flow (per learning):
  knowledge -> draft (local Qwen) -> lint (rules) -> dedupe (past posts)
  -> critic (rubric score) -> [one bounded revision if needed]
  -> queue in SQLite (status=drafted) -> compose link (human taps Post)

Stdlib only. The agent never calls the X API; it only drafts and prints a link.
"""
import argparse
import os
import sqlite3
import sys
import time
from pathlib import Path

# Allow running both as `python3 bot/pipeline.py` and `python3 -m bot.pipeline`.
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
for p in (str(ROOT), str(SRC)):
    if p not in sys.path:
        sys.path.insert(0, p)

from bot.knowledge_reader import read_knowledge
from bot.draft_post import draft_post
from bot.critique_post import critique_post
from xbot import db, lint, dedupe, compose

DEFAULT_MIN_SCORE = 4.0
MAX_REV = 1  # one bounded revision per learning


def init_state(db_path="state/twitter_bot.db"):
    conn = db.init_db(db_path)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS feedback ("
        "id INTEGER PRIMARY KEY, post_id INTEGER, pillar TEXT, topic TEXT, "
        "rating INTEGER, notes TEXT, created_at TEXT NOT NULL)"
    )
    conn.commit()
    return conn


def _revise(draft, issues, voice, rules, learning, pillars):
    """Ask the model to rewrite the draft fixing the listed issues. One call."""
    import json, urllib.request
    OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
    MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:4b-q4_K_M")
    NUM_CTX = int(os.environ.get("NUM_CTX", "8192"))
    system = (
        "You are an editor. Rewrite the X post below so it fixes these issues: "
        + "; ".join(issues)
        + ". Keep it <=280 chars, no links, no banned phrases, max 2 hashtags. "
        "Follow voice.md and rules.md. Output ONLY the post text."
    )
    user = (
        f"# LEARNING: {learning.title}\n{learning.body}\n\n"
        f"# CURRENT DRAFT:\n{draft}\n\n# ISSUES TO FIX:\n" + "\n".join(f"- {i}" for i in issues)
        + "\n\n# VOICE:\n" + voice + "\n# RULES:\n" + rules
    )
    body = __import__("json").dumps({
        "model": MODEL, "stream": False,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "options": {"temperature": 0.3, "num_ctx": NUM_CTX},
    }).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        text = __import__("json").load(resp)["message"]["content"]
    return text.strip().strip('"').strip()


def _clean(text):
    return text.strip().strip('"').strip()


def run_pipeline(knowledge_dir="knowledge", db_path="state/twitter_bot.db",
                 voice="instructions/voice.md", rules="instructions/rules.md",
                 rubric="instructions/rubric.md", pillars="instructions/content_pillars.md",
                 min_score=DEFAULT_MIN_SCORE, all_=False):
    voice = (ROOT / voice).read_text()
    rules = (ROOT / rules).read_text()
    rubric = (ROOT / rubric).read_text()
    pillars = (ROOT / pillars).read_text()

    learnings = read_knowledge(knowledge_dir)
    if not learnings:
        print("No learnings found in knowledge/. Add markdown files there first.")
        return []
    if not all_:
        learnings = learnings[:1]

    conn = init_state(db_path)
    past = db.past_texts(conn)
    results = []

    for learning in learnings:
        print(f"\n=== {learning.title} (pillar: {learning.pillar}) ===")
        draft = _clean(draft_post(learning, voice, rules, pillars))
        issues = lint.lint_post(draft)
        rev = 0
        while issues and rev < MAX_REV:
            rev += 1
            draft = _clean(_revise(draft, issues, voice, rules, learning, pillars))
            issues = lint.lint_post(draft)

        if dedupe.is_duplicate(draft, past) and rev < MAX_REV:
            draft = _clean(_revise(draft, ["duplicate of a past post"], voice, rules, learning, pillars))
            rev += 1

        score, feedback = critique_post(draft, rubric)
        if score < min_score and rev < MAX_REV:
            draft = _clean(_revise(draft, [f"critic score {score:.1f}: {feedback}"], voice, rules, learning, pillars))
            rev += 1
            score, feedback = critique_post(draft, rubric)

        problems = lint.lint_post(draft)
        if problems:
            print(f"SKIP: still violates {problems}")
            continue

        pid = db.add_post(conn, draft, learning.pillar, status="drafted")
        url = compose.compose_url(draft)
        results.append(dict(id=pid, pillar=learning.pillar, topic=learning.title,
                            text=draft, score=score, url=url))
        print(f"QUEUED id={pid} score={score:.1f} attempts={rev + 1}")
        print(f"  {draft}")
        print(f"  POST LINK: {url}")

    conn.close()
    return results


def rate_post(post_id, rating, notes="", db_path="state/twitter_bot.db"):
    """Log human feedback for a posted draft (free, manual metrics)."""
    conn = sqlite3.connect(db_path)
    row = conn.execute("SELECT pillar, text FROM posts WHERE id = ?", (post_id,)).fetchone()
    if row is None:
        conn.close()
        raise KeyError(post_id)
    pillar, text = row
    conn.execute(
        "INSERT INTO feedback (post_id, pillar, topic, rating, notes, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (post_id, pillar, text[:60], int(rating), notes,
         __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat()),
    )
    conn.commit()
    conn.close()
    print(f"Rated post {post_id} ({pillar}) = {rating}/5")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--all", action="store_true", help="draft from every learning, not just the first")
    ap.add_argument("--rate", type=int, metavar="POST_ID", help="log a human rating for a post id")
    ap.add_argument("--rating", type=int, default=5, help="rating value with --rate (1-5)")
    ap.add_argument("--notes", default="", help="notes with --rate")
    ap.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE,
                    help="minimum critic score to queue (default 4.0)")
    a = ap.parse_args()

    if a.rate is not None:
        rate_post(a.rate, a.rating, a.notes)
        return
    run_pipeline(all_=a.all, min_score=a.min_score)


if __name__ == "__main__":
    main()

"""Score a draft post against the rubric using the local Qwen model.

Returns an average score (1-5) and short feedback. Used by the closed loop to decide
whether a draft is good enough to queue or needs a revision.
"""
import json
import os
import urllib.request

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:4b-q4_K_M")
NUM_CTX = int(os.environ.get("NUM_CTX", "8192"))


def _chat(system, user, temperature=0.2):
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "stream": False,
        "options": {"temperature": temperature, "num_ctx": NUM_CTX},
    }).encode()
    req = urllib.request.Request(
        f"{OLLAMA}/api/chat", body, {"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=900) as resp:
        text = json.load(resp)["message"]["content"]
    return text.strip()


def critique_post(draft, rubric):
    """Return (average_score: float, feedback: str)."""
    system = (
        "You are a strict editor. Score the draft post 1-5 on each rubric criterion, "
        "then output the average. Reply with exactly two lines:\n"
        "SCORE: <number between 1 and 5>\nFEEDBACK: <one sentence>\n"
        "No other text."
    )
    user = f"# RUBRIC:\n{rubric}\n\n# DRAFT:\n{draft}\n"
    text = _chat(system, user)
    score = 3.0
    feedback = text
    for line in text.split("\n"):
        if line.startswith("SCORE:"):
            try:
                score = float(line.split(":", 1)[1].strip())
            except ValueError:
                score = 3.0
    return score, feedback

"""Draft an X post from a learning using the local Qwen model via Ollama.

Mode A: draft only. This module never touches the X API and never opens a browser.
It only returns text for the human to review and post via the compose link.
"""
import json
import os
import urllib.request

OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:4b-q4_K_M")
NUM_CTX = int(os.environ.get("NUM_CTX", "8192"))


def _chat(system, user, temperature=0.3):
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


def draft_post(learning, voice, rules, pillars):
    """Draft one native-text X post (<=280 chars, no links) from a Learning.

    Returns the raw draft text (may need lint/critic review before queuing).
    """
    system = (
        "You are an expert X (Twitter) ghostwriter for an AI/ML practitioner. "
        "Draft ONE native text post (no links, 280 characters max) from the learning. "
        "Follow voice.md, rules.md and content_pillars.md exactly. "
        "Output ONLY the post text - no quotes, no labels, no markdown fences, no hashtags unless they add value."
    )
    user = (
        f"# LEARNING (title: {learning.title}, pillar: {learning.pillar})\n"
        f"{learning.body}\n\n"
        f"# VOICE:\n{voice}\n\n# RULES:\n{rules}\n\n# CONTENT PILLARS:\n{pillars}\n\n"
        "Write the post now:"
    )
    return _chat(system, user)

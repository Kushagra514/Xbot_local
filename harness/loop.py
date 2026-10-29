#!/usr/bin/env python3
"""Closed-loop coordinator for the xbot fleet. Stdlib only.

    python3 harness/loop.py --level 3 --all --fresh
    python3 harness/loop.py --level 4 --task T2

Harness levels (cumulative) — see experiments/PROTOCOL.md:
  0  bare prompt: task title only
  1  + instructions: AGENTS.md, role, spec, read-only tests
  2  + gate: verify.sh decides; failing output is reverted
  3  + feedback: gate output is fed back, up to MAX_TRIES attempts
  4  + state & critic: lessons.md injected; critic reviews passing code; scribe records lessons
Ground truth (did verify.sh pass?) is measured at EVERY level and logged to state/runs.csv.
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOARD = ROOT / "board" / "TASKS.md"
RUNS = ROOT / "state" / "runs.csv"
LESSONS = ROOT / "state" / "lessons.md"
OLLAMA = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "qwen3.5:4b-q4_K_M")
NUM_CTX = int(os.environ.get("NUM_CTX", "8192"))
MAX_TRIES = 3
TASK_RE = re.compile(r"^- \[( |x)\] (T\d+) \| (.+?) \| (\S+) \| (\S+) \| (\S+)\s*$")
FILE_RE = re.compile(r"###\s*FILE:\s*(\S+)\s*\n```[a-zA-Z]*\n(.*?)```", re.DOTALL)


def load_tasks():
    tasks = []
    for line in BOARD.read_text().splitlines():
        m = TASK_RE.match(line)
        if m:
            done, tid, title, test, out, spec = m.groups()
            tasks.append(dict(done=done == "x", id=tid, title=title, test=test, out=out, spec=spec))
    return tasks


def read(rel):
    return (ROOT / rel).read_text()


# ---------- model access ----------
def chat(messages, role, task, mock):
    if mock:
        return mock_reply(Path(mock), role, task)
    body = json.dumps({
        "model": MODEL, "messages": messages, "stream": False,
        "options": {"temperature": 0.2, "num_ctx": NUM_CTX},
    }).encode()
    req = urllib.request.Request(f"{OLLAMA}/api/chat", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        text = json.load(resp)["message"]["content"]
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


def mock_reply(mockdir, role, task):
    """Offline self-test: builder returns a prepared file, critic approves, scribe returns a canned lesson."""
    if role == "builder":
        src = mockdir / task["out"]
        if not src.exists():
            return "I could not do it."
        return f"### FILE: {task['out']}\n```python\n{src.read_text()}```"
    if role == "critic":
        return "Looks fine.\nVERDICT: PASS"
    return "Read the acceptance tests first and match every exception type exactly."


# ---------- prompt assembly ----------
FORMAT = "Reply with the complete file in exactly this format and nothing else:\n### FILE: {out}\n```python\n<code>\n```"


def builder_messages(level, task, feedback):
    fmt = FORMAT.format(out=task["out"])
    if level == 0:
        system = "You write Python."
        user = f"Task: {task['title']}\nOutput file: {task['out']}\n\n{fmt}"
    else:
        system = read("AGENTS.md") + "\n\n" + read("roles/builder.md")
        if level >= 4 and LESSONS.exists() and LESSONS.read_text().strip():
            system += "\n\n# Lessons from earlier runs\n" + LESSONS.read_text()
        user = (f"# Task {task['id']}: {task['title']}\n\n{read(task['spec'])}\n\n"
                f"# Acceptance tests (read-only)\n```python\n{read(task['test'])}```\n\n{fmt}")
    if feedback:
        user += f"\n\n# Your previous attempt was rejected. Details:\n{feedback}\n\nFix the root cause and resend the COMPLETE file."
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


# ---------- tools ----------
def apply_files(reply, allowed):
    """Write only the one allowed output file. Returns True if written."""
    for path, code in FILE_RE.findall(reply):
        if path.strip() == allowed:
            target = ROOT / allowed
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(code)
            return True
    return False


def gate(test):
    p = subprocess.run(["bash", str(ROOT / "scripts" / "verify.sh"), test],
                       capture_output=True, text=True, cwd=ROOT)
    return p.returncode == 0, (p.stdout + p.stderr)[-2500:]


def critic_review(task, mock):
    code = read(task["out"])
    system = read("AGENTS.md") + "\n\n" + read("roles/critic.md")
    user = f"# Spec\n{read(task['spec'])}\n\n# Code under review ({task['out']})\n```python\n{code}```"
    reply = chat([{"role": "system", "content": system}, {"role": "user", "content": user}], "critic", task, mock)
    lines = [l for l in reply.strip().splitlines() if l.strip()]
    verdict = lines[-1].strip() if lines else ""
    return verdict == "VERDICT: PASS", reply


def scribe_note(task, last_output, mock):
    system = read("roles/scribe.md")
    user = f"Task failed: {task['title']}\n\nLast gate output:\n{last_output}"
    lesson = chat([{"role": "system", "content": system}, {"role": "user", "content": user}], "scribe", task, mock)
    lesson = " ".join(lesson.split())[:400]
    with LESSONS.open("a") as f:
        f.write(f"- {lesson}\n")


# ---------- one task ----------
def run_task(task, level, mock, fresh, tick):
    out = ROOT / task["out"]
    if fresh and out.exists():
        out.unlink()
    original = out.read_text() if out.exists() else None
    tries = MAX_TRIES if level >= 3 else 1
    feedback, passed, attempts, critic_rejects, output = None, False, 0, 0, ""
    started = time.time()

    for attempt in range(1, tries + 1):
        attempts = attempt
        reply = chat(builder_messages(level, task, feedback), "builder", task, mock)
        if not apply_files(reply, task["out"]):
            feedback = f"No valid '### FILE: {task['out']}' block found in your reply."
            output = feedback
            continue
        ok, output = gate(task["test"])
        if ok and level >= 4:
            approved, review = critic_review(task, mock)
            if not approved:
                critic_rejects += 1
                ok, output = False, "Critic rejected the code:\n" + review
        if ok:
            passed = True
            break
        feedback = output
        if level >= 2:  # the gate blocks bad code from staying in the repo
            if original is None:
                out.unlink(missing_ok=True)
            else:
                out.write_text(original)

    if not passed and level >= 4:
        scribe_note(task, output, mock)
    if passed and tick and level >= 2:
        text = BOARD.read_text().replace(f"- [ ] {task['id']} |", f"- [x] {task['id']} |")
        BOARD.write_text(text)

    seconds = round(time.time() - started, 1)
    new = not RUNS.exists()
    with RUNS.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["ts", "model", "level", "task", "attempts", "passed", "critic_rejects", "seconds"])
        w.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), "mock" if mock else MODEL, level, task["id"],
                    attempts, int(passed), critic_rejects, seconds])
    print(f"L{level} {task['id']} {'PASS' if passed else 'FAIL'} attempts={attempts} "
          f"critic_rejects={critic_rejects} {seconds}s")
    return passed


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--level", type=int, choices=range(5), required=True)
    ap.add_argument("--task", help="task id, e.g. T2")
    ap.add_argument("--all", action="store_true", help="run every task on the board")
    ap.add_argument("--fresh", action="store_true", help="delete the output file first (use for experiments)")
    ap.add_argument("--tick", action="store_true", help="tick the board checkbox on success (level>=2)")
    ap.add_argument("--mock", metavar="DIR", help="offline self-test: take builder output from DIR/<out path>")
    a = ap.parse_args()

    tasks = load_tasks()
    if a.task:
        tasks = [t for t in tasks if t["id"] == a.task]
    elif a.all:
        pass
    else:
        tasks = [t for t in tasks if not t["done"]][:1]
    if not tasks:
        sys.exit("no matching task on the board")
    results = [run_task(t, a.level, a.mock, a.fresh, a.tick) for t in tasks]
    print(f"{sum(results)}/{len(results)} passed")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()

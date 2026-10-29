#!/usr/bin/env python3
"""Compare harness levels from state/runs.csv.  Usage: python3 harness/report.py [model]

Columns: runs = task-runs, pass% = final gate result, 1st-try% = passed on attempt 1,
att = mean attempts, c-rej = critic rejections, sec = mean seconds per task.
"""
import csv
import sys
from collections import defaultdict
from pathlib import Path

RUNS = Path(__file__).resolve().parent.parent / "state" / "runs.csv"
NAMES = {0: "bare prompt", 1: "+instructions", 2: "+gate", 3: "+feedback", 4: "+state/critic"}


def main():
    if not RUNS.exists():
        sys.exit("no runs yet. Try: python3 harness/loop.py --level 3 --all --fresh")
    only = sys.argv[1] if len(sys.argv) > 1 else None
    groups = defaultdict(list)
    for r in csv.DictReader(RUNS.open()):
        if only and r["model"] != only:
            continue
        groups[(r["model"], int(r["level"]))].append(r)
    if not groups:
        sys.exit("no rows for that model")
    head = f"{'model':<22}{'level':<20}{'runs':>5}{'pass%':>7}{'1st-try%':>10}{'att':>6}{'c-rej':>7}{'sec':>7}   per task"
    print(head + "\n" + "-" * (len(head) + 24))
    for (model, lv), rs in sorted(groups.items()):
        n = len(rs)
        ok = sum(int(r["passed"]) for r in rs)
        first = sum(1 for r in rs if int(r["passed"]) and int(r["attempts"]) == 1)
        per = defaultdict(lambda: [0, 0])
        for r in rs:
            per[r["task"]][0] += int(r["passed"])
            per[r["task"]][1] += 1
        tasks = " ".join(f"{t}:{a}/{b}" for t, (a, b) in sorted(per.items()))
        print(f"{model[:21]:<22}{('L%d %s' % (lv, NAMES[lv])):<20}{n:>5}{100 * ok / n:>6.0f}%{100 * first / n:>9.0f}%"
              f"{sum(int(r['attempts']) for r in rs) / n:>6.1f}{sum(int(r['critic_rejects']) for r in rs):>7}"
              f"{sum(float(r['seconds']) for r in rs) / n:>7.1f}   {tasks}")
    print("\nSmall samples are noisy: repeat each level >= 3 times; differences under ~2 task-runs are noise.")


if __name__ == "__main__":
    main()

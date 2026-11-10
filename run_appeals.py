#!/usr/bin/env python3
"""
Run criterion 4, the appeal path, three times.  <- UNIT 8, MILESTONE 3

    python app.py                              # in one terminal
    python run_appeals.py --label before       # in another

`run_eval.py` only posts to /submit, and an appeal needs a content_id that a
real submission handed back, so criterion 4 can't be written as a scenario.
This does it instead, per trial:

  1. submits 5 texts and keeps each content_id
  2. appeals each one with its own reasoning
  3. appeals 2 content_ids that don't exist
  4. reads logs/audit.jsonl back and checks, for every real appeal, that an
     `appeal` entry with status `under_review` and the exact reasoning is
     there, and that the original `decided` entry is unchanged; and for every
     fake one, that it got a 404 and left no appeal entry behind.

Unlike run_eval.py it does decide pass/fail, because criterion 4's checks are
all exact: a status code, a field value, a string match.

Writes `results/appeal_run_<date>_<label>.md`.
"""

import argparse
import datetime as dt
import json
import sys
import uuid

import audit
import config
import scenarios

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


DEFAULT_URL = f"http://{config.HOST}:{config.PORT}"

TEXTS = [
    scenarios.MINE_CASUAL,
    scenarios.MINE_PLAIN,
    scenarios.PUBLISHED_EQUALITY,
    scenarios.AI_SLEEP,
    scenarios.BORDERLINE_UNIT7,
]
FAKE_IDS = 2


def run_trial(requests, url, trial, timeout):
    """One trial: 5 real appeals and 2 fake ones, each checked against the log."""
    # A fresh creator per submission, so the trial tests the appeal path and
    # never my own rate limit.
    run_tag = uuid.uuid4().hex[:6]
    real = []
    for i, text in enumerate(TEXTS, 1):
        creator = f"appeal_{run_tag}_t{trial}_{i}"
        sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator},
                            timeout=timeout)
        content_id = sub.json().get("content_id")
        decided_before = [e for e in audit.entries_for(content_id)
                          if e.get("status") == "decided"] if content_id else []
        reasoning = (f"Trial {trial}, piece {i}: I wrote this myself and can show "
                     f"my drafts. ({run_tag})")
        app = requests.post(f"{url}/appeal",
                            json={"content_id": content_id, "reasoning": reasoning},
                            timeout=timeout)
        real.append({"content_id": content_id, "submit_status": sub.status_code,
                     "reasoning": reasoning, "response_status": app.status_code,
                     "response": app.json(), "decided_before": decided_before})

    fake = []
    for j in range(1, FAKE_IDS + 1):
        content_id = f"fake{run_tag}t{trial}n{j}"
        app = requests.post(f"{url}/appeal",
                            json={"content_id": content_id, "reasoning": "typo test"},
                            timeout=timeout)
        fake.append({"content_id": content_id, "response_status": app.status_code,
                     "response": app.json()})

    # Check every one against what the log actually holds now.
    for r in real:
        entries = audit.entries_for(r["content_id"])
        appeals = [e for e in entries if e.get("event") == "appeal"]
        decided_now = [e for e in entries if e.get("status") == "decided"]
        r["checks"] = {
            "returned_200": r["response_status"] == 200,
            "response_under_review": r["response"].get("status") == "under_review",
            "appeal_entry_logged": len(appeals) == 1,
            "logged_under_review": bool(appeals) and appeals[0].get("status") == "under_review",
            "reasoning_exact": bool(appeals) and appeals[0].get("reasoning") == r["reasoning"],
            "original_unchanged": len(r["decided_before"]) == 1
                                  and decided_now == r["decided_before"],
        }
        r["passed"] = all(r["checks"].values())
    for f in fake:
        appeals = [e for e in audit.entries_for(f["content_id"]) if e.get("event") == "appeal"]
        f["checks"] = {"returned_404": f["response_status"] == 404,
                       "no_appeal_logged": not appeals}
        f["passed"] = all(f["checks"].values())
    return real, fake


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--label", default="")
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--timeout", type=float, default=90.0)
    args = parser.parse_args()

    import requests
    try:
        requests.get(f"{args.url}/health", timeout=5)
    except Exception:  # noqa: BLE001
        print(f"Nothing answering at {args.url}. Start it:  python app.py", file=sys.stderr)
        sys.exit(1)

    trials = []
    for trial in range(1, args.trials + 1):
        real, fake = run_trial(requests, args.url, trial, args.timeout)
        trials.append((real, fake))
        print(f"  trial {trial}: real {sum(r['passed'] for r in real)}/{len(real)}, "
              f"fake {sum(f['passed'] for f in fake)}/{len(fake)}")

    write_report(trials, args)


def write_report(trials, args):
    config.RESULTS_DIR.mkdir(exist_ok=True)
    stamp = dt.datetime.now().strftime("%Y-%m-%d_%H%M")
    label = f"_{args.label}" if args.label else ""
    path = config.RESULTS_DIR / f"appeal_run_{stamp}{label}.md"

    runs_real = " | ".join(f"{sum(r['passed'] for r in real)}/{len(real)}" for real, _ in trials)
    runs_fake = " | ".join(f"{sum(f['passed'] for f in fake)}/{len(fake)}" for _, fake in trials)
    header = " | ".join(f"Run {i}" for i in range(1, len(trials) + 1))
    lines = [
        f"# Appeal run{f' — {args.label}' if args.label else ''}",
        "",
        "- Produced by: `run_appeals.py::main`",
        "- Service: `app.py::submit` then `app.py::appeal`; checked against `logs/audit.jsonl`",
        f"- {len(trials)} trials · {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        f"| Check | Target | {header} |",
        f"|---|---|{'|'.join(['---'] * len(trials))}|",
        f"| Real appeals: 200, under_review, logged with exact reasoning, original unchanged | 5 of 5 | {runs_real} |",
        f"| Fake ids: 404 and no appeal logged | 2 of 2 | {runs_fake} |",
        "",
        "---",
        "",
        "## What actually came back",
        "",
    ]
    for n, (real, fake) in enumerate(trials, 1):
        shown = [{k: v for k, v in r.items() if k != "decided_before"} for r in real]
        lines += [f"**Trial {n}**", "", "```json",
                  json.dumps({"real": shown, "fake": fake}, indent=2, ensure_ascii=False),
                  "```", ""]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()

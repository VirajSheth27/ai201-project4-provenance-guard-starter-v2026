#!/usr/bin/env python3
"""
The capstone run log: five criteria, three trials — capstone (unit 9).

    python run_capstone.py --label before
    python fresh_clone_check.py --label before    # criterion 5, run separately

Each trial is one call to `measure_cost.run_once()`, which starts a FRESH
`serve.py` process (so the cold request is really cold), sends 1 cold + 50 warm
+ 3 bad-input + a 7-request burst to /submit, stops the server, and reads back
the records it wrote to logs/requests.jsonl. Nothing changes between trials.

Criteria 1–4 are scored here against the targets in criteria.md
("Capstone criteria"), exactly as written there:

  1. warm P95 <= 2000 ms AND cold <= 20 s
  2. /submit logged == /submit sent == 61 (/health readiness polls excluded)
  3. highest rss_mb after any /submit <= 1200 MB AND
     sum(cpu_s of the 50 warm records) / 50 <= 3.5 AND
     stage shares total within 99–101 %
  4. blank -> 400, short -> 422, array -> 400, burst -> 5x200 then 2x429,
     no 5xx anywhere in the run, and every rejected request logged with
     outcome `rejected` (4xx) or `rate_limited` (429)

Criterion 5 is three fresh clones; `fresh_clone_check.py` writes
results/fresh_clone_<label>.json and this script folds it into the table if
it's there.

Writes results/capstone_<date>_<label>.md.
"""

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

import config
import measure_cost

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent
WARM_N = 50
EXPECTED_SUBMITS = 1 + WARM_N + 3 + 7          # 61

P95_MAX_MS = 2000
COLD_MAX_MS = 20_000
RSS_MAX_MB = 1200
CPU_MAX_S = 3.5
SHARE_RANGE = (99.0, 101.0)
EXPECTED_BAD = [("blank", 400), ("short", 422), ("array", 400)] + \
               [("flood", 200)] * 5 + [("flood", 429)] * 2
OUTCOME_FOR = {400: "rejected", 422: "rejected", 429: "rate_limited", 200: "ok"}


def score(r):
    """Score one trial against criteria 1–4. Returns {n: (passed, cell_text)}."""
    w = r["warm"]["duration_ms"]
    cold_ms = r["cold"]["duration_ms"]
    c1 = (w.get("p95") is not None and w["p95"] <= P95_MAX_MS
          and cold_ms is not None and cold_ms <= COLD_MAX_MS
          and w.get("n") == WARM_N)
    c1_txt = f"p95 {w.get('p95')} ms, cold {cold_ms / 1000:.1f} s"

    c2 = (r["submit_sent"] == EXPECTED_SUBMITS
          and r["submit_logged"] == r["submit_sent"]
          and r["submit_records_in_log"] == r["submit_sent"])
    c2_txt = f"{r['submit_logged']}/{r['submit_sent']}"

    share = r["stage_share_total"]
    cpu = r["warm_cpu"]["mean_s"]
    c3 = (r["peak_rss_mb"] is not None and r["peak_rss_mb"] <= RSS_MAX_MB
          and cpu is not None and cpu <= CPU_MAX_S and r["warm_cpu"]["n"] == WARM_N
          and share is not None and SHARE_RANGE[0] <= share <= SHARE_RANGE[1])
    c3_txt = f"{r['peak_rss_mb']} MB, {cpu} core-s, {share}%"

    bad = r["bad_path"]
    got = [(b["phase"], b["status"]) for b in bad]
    codes_ok = got == EXPECTED_BAD
    logged_ok = all(b["logged_outcome"] == OUTCOME_FOR.get(b["status"]) for b in bad)
    cases = [
        bad[0]["status"] == 400 and bad[0]["logged_outcome"] == "rejected",
        bad[1]["status"] == 422 and bad[1]["logged_outcome"] == "rejected",
        bad[2]["status"] == 400 and bad[2]["logged_outcome"] == "rejected",
        [b["status"] for b in bad[3:]] == [200] * 5 + [429] * 2
        and all(b["logged_outcome"] == OUTCOME_FOR.get(b["status"]) for b in bad[3:]),
    ] if len(bad) == 10 else [False] * 4
    c4 = codes_ok and logged_ok and not r["any_500"] and all(cases)
    c4_txt = f"{sum(cases)}/4" + ("" if not r["any_500"] else ", 5xx!")

    return {1: (c1, c1_txt), 2: (c2, c2_txt), 3: (c3, c3_txt), 4: (c4, c4_txt)}


def load_clone_results(label):
    path = config.RESULTS_DIR / f"fresh_clone_{label}.json"
    if not path.exists():
        return None, path
    return json.loads(path.read_text(encoding="utf-8")), path


def find(records, rid):
    return next((x for x in records if x.get("request_id") == rid), None)


def report(trials, scores, args, clone):
    names = {
        1: "1. Warm P95 ≤ 2 s, cold ≤ 20 s (50 warm)",
        2: "2. Every /submit request logged",
        3: "3. Memory ≤ 1200 MB, warm CPU ≤ 3.5 core-s, stage shares 99–101 %",
        4: "4. Bad input + burst: right codes, no 5xx, logged",
        5: "5. Fresh clone sets up and serves",
    }
    targets = {1: "p95 ≤ 2000 ms and cold ≤ 20 s, every run",
               2: "61/61, every run",
               3: "all three, every run",
               4: "4/4 cases, no 5xx, every run",
               5: "3 of 3 clones"}
    L = [f"# Capstone run log — {args.label}", "",
         f"Generated {dt.datetime.now():%Y-%m-%d %H:%M} by `python run_capstone.py "
         f"--label {args.label}`. Three trials, each against a freshly started "
         f"`serve.py` (waitress), nothing changed between them.", "",
         "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |",
         "|---|---|---|---|---|---|"]
    for n in (1, 2, 3, 4):
        cells = [f"{'✔' if scores[t][n][0] else '✘'} {scores[t][n][1]}" for t in range(len(trials))]
        verdict = "MET" if all(scores[t][n][0] for t in range(len(trials))) else "MISSED"
        L.append(f"| {names[n]} | {targets[n]} | " + " | ".join(cells) + f" | **{verdict}** |")
    if clone:
        cells = [f"{'✔' if c['passed'] else '✘'} {c['summary']}" for c in clone["clones"]]
        cells += ["—"] * (3 - len(cells))
        passed = sum(c["passed"] for c in clone["clones"])
        verdict = "MET" if passed == 3 and len(clone["clones"]) == 3 else "MISSED"
        L.append(f"| {names[5]} | {targets[5]} | " + " | ".join(cells[:3]) + f" | **{verdict}** ({passed}/3) |")
    else:
        L.append(f"| {names[5]} | {targets[5]} | not run | not run | not run | — |")

    L += ["", "## Per trial", ""]
    for i, r in enumerate(trials, 1):
        w = r["warm"]["duration_ms"]
        L += [f"**Run {i}** ({r['stamp']}): startup {r['startup_s']} s · cold {r['cold']['duration_ms']} ms "
              f"({r['cold']['cpu_s']} core-s) · warm p50 {w['p50']} / p95 {w['p95']} / p99 {w['p99']} / "
              f"max {w['max']} ms (n={w['n']}) · warm CPU {r['warm_cpu']['sum_s']} / {r['warm_cpu']['n']} = "
              f"{r['warm_cpu']['mean_s']} core-s · highest RSS {r['peak_rss_mb']} MB · "
              f"stage shares {r['stage_share']} = {r['stage_share_total']}% · "
              f"/submit logged {r['submit_logged']}/{r['submit_sent']}", ""]

    r = trials[0]
    recs = r["records"]
    sent = r["sent_detail"]
    warm_recs = [find(recs, s["request_id"]) for s in sent if s["phase"] == "warm"]
    slowest = max((x for x in warm_recs if x), key=lambda x: x["duration_ms"])
    cold_rec = find(recs, next(s["request_id"] for s in sent if s["phase"] == "cold"))
    L += ["## Real output (Run 1)", "",
          "Produced by `measure_cost.py::run_once` (sending) and "
          "`app.py::_telemetry_finish` → `telemetry.py::log_request` (the records).", "",
          "**Criterion 1**: the cold request and the slowest warm request:", "", "```json",
          json.dumps(cold_rec, ensure_ascii=False), json.dumps(slowest, ensure_ascii=False), "```", "",
          "**Criterion 2**: every /submit the script sent, with its status and the "
          "request_id it was matched to in `requests.jsonl`:", "", "```json"]
    L += [json.dumps(s) for s in sent]
    L += ["```", "",
          "**Criterion 3**: stage breakdown (warm, ms) and the record with the highest memory reading:", "",
          "| Stage | mean | p95 | share |", "|---|---|---|---|"]
    for k, v in r["stages_ms"].items():
        if v.get("n"):
            L.append(f"| {k} | {v['mean']} | {v['p95']} | {r['stage_share'].get(k)}% |")
    L.append(f"| total | | | {r['stage_share_total']}% |")
    peak = max((x for x in recs if x.get("route") == "/submit"), key=lambda x: x.get("rss_mb") or 0)
    L += ["", "```json", json.dumps(peak, ensure_ascii=False), "```", "",
          "**Criterion 4**: every bad-path request's log record:", "", "```json"]
    for s in sent:
        if s["phase"] in ("blank", "short", "array", "flood"):
            L.append(json.dumps(find(recs, s["request_id"]), ensure_ascii=False))
    L += ["```", ""]
    if clone:
        L += ["**Criterion 5**: from `fresh_clone_check.py` "
              f"(`results/fresh_clone_{args.label}.json`):", "", "```"]
        for c in clone["clones"]:
            L.append(f"clone {c['n']}: {c['summary']}")
            for step in c["steps"]:
                L.append(f"   {step['step']:<14} {'ok ' if step['ok'] else 'FAIL'} {step['detail']}")
        L += ["```", ""]
    L += ["## All records, every trial", ""]
    for i, t in enumerate(trials, 1):
        L += [f"<details><summary>Run {i}: {len(t['records'])} records</summary>", "", "```json"]
        L += [json.dumps(x, ensure_ascii=False) for x in t["records"]]
        L += ["```", "", "</details>", ""]
    return "\n".join(L)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--label", required=True)
    p.add_argument("--trials", type=int, default=3)
    p.add_argument("--port", type=int, default=5061)
    args = p.parse_args()

    trials, scores = [], []
    for t in range(args.trials):
        print(f"\n=== trial {t + 1}/{args.trials} ===")
        r = measure_cost.run_once(label=f"{args.label}-t{t + 1}", n=WARM_N,
                                  port=args.port + t, quiet=True)
        trials.append(r)
        s = score(r)
        scores.append(s)
        for n, (ok, txt) in s.items():
            print(f"  criterion {n}: {'MET   ' if ok else 'MISSED'} {txt}")

    clone, clone_path = load_clone_results(args.label)
    if not clone:
        print(f"\n(criterion 5: no {clone_path.name} yet; run fresh_clone_check.py --label {args.label})")

    config.RESULTS_DIR.mkdir(exist_ok=True)
    out = config.RESULTS_DIR / f"capstone_{dt.datetime.now():%Y-%m-%d_%H%M}_{args.label}.md"
    out.write_text(report(trials, scores, args, clone), encoding="utf-8")
    (config.RESULTS_DIR / f"capstone_{args.label}.json").write_text(json.dumps(
        [{k: v for k, v in r.items() if k not in ("records",)} for r in trials], indent=1),
        encoding="utf-8")
    print(f"\nwrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

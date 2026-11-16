#!/usr/bin/env python3
"""
What does one run of Provenance Guard cost? — capstone (unit 9).

    python measure_cost.py --label before

It does the whole thing itself, so the number comes from a real process and
not a warm laptop session:

  1. Starts `python serve.py` as a fresh process on its own port (5055 unless
     --port), and times how long until /health answers.        -> startup
  2. Sends ONE /submit while the model isn't loaded yet.        -> cold
  3. Sends --n more /submit (default 10), the ten "own writing" texts from
     scenarios.py, each under its own creator_id.              -> warm
  4. Sends deliberate failures: blank text (400), too-short text (422), a
     JSON array instead of an object (400), and a burst of 7 from one
     creator, which should end in 429s.                         -> bad path
  5. Stops the server, reads the records this run wrote to
     logs/requests.jsonl, and matches every request it sent to its record by
     the X-Request-ID header.

Then it writes results/cost_<date>_<label>.md: latency (mean/p50/p95/max),
CPU seconds, memory, a per-stage breakdown, every failure's status, and how
many of the requests it sent actually appear in the log.

"Cost" here is **compute**, not money: nothing in this system calls a paid
API. CPU seconds come from time.process_time() inside the server, which is
process-wide — accurate here because the requests are sent one at a time.

    --url http://127.0.0.1:5000   measure a server you already started instead
                                  (then the "cold" request is only cold if
                                  nothing has hit /submit since it started)
"""

import argparse
import datetime as dt
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

import requests

import config
import scenarios

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent


# ── helpers ───────────────────────────────────────────────────────────────────

def pct(values, p):
    """Nearest-rank percentile. Fine for a handful of samples, and honest."""
    if not values:
        return None
    s = sorted(values)
    k = max(0, min(len(s) - 1, int(round(p / 100 * len(s) + 0.5)) - 1))
    return s[k]


def summarise(values):
    if not values:
        return {"n": 0}
    return {
        "n": len(values),
        "mean": round(statistics.mean(values), 2),
        "p50": round(pct(values, 50), 2),
        "p95": round(pct(values, 95), 2),
        "max": round(max(values), 2),
        "min": round(min(values), 2),
    }


def own_writing_texts():
    for s in scenarios.SCENARIOS:
        if s.get("name") == "own writing":
            return list(s["texts"])
    raise SystemExit("scenarios.py has no 'own writing' scenario to send")


def start_server(port):
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", PYTHONUNBUFFERED="1")
    log_path = config.LOG_DIR / f"serve_{port}.out"
    out = log_path.open("w", encoding="utf-8")
    t0 = time.perf_counter()
    proc = subprocess.Popen([sys.executable, str(ROOT / "serve.py")], cwd=ROOT,
                            env=env, stdout=out, stderr=subprocess.STDOUT)
    url = f"http://127.0.0.1:{port}"
    deadline = time.time() + 120
    while time.time() < deadline:
        if proc.poll() is not None:
            raise SystemExit(f"serve.py exited early ({proc.returncode}); see {log_path}")
        try:
            if requests.get(url + "/health", timeout=2).ok:
                return proc, url, round(time.perf_counter() - t0, 2)
        except requests.RequestException:
            pass
        time.sleep(0.2)
    proc.kill()
    raise SystemExit(f"serve.py didn't answer /health within 120 s; see {log_path}")


# ── the run ───────────────────────────────────────────────────────────────────

def run_once(label="", n=10, port=5055, url=None, quiet=False):
    """
    One full measurement. Returns a dict with everything measured, including the
    raw log records, so run_capstone.py can call this three times.
    """
    stamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    say = (lambda *a: None) if quiet else print

    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    lines_before = (len(config.REQUEST_LOG.read_text(encoding="utf-8").splitlines())
                    if config.REQUEST_LOG.exists() else 0)

    proc, startup_s = None, None
    if url is None:
        say(f"starting serve.py on port {port} ...")
        proc, url, startup_s = start_server(port)
        say(f"  /health answered after {startup_s} s")

    sent = []   # (phase, expected, status, request_id, client_ms)

    def post(phase, expected, body=None, raw=None):
        t0 = time.perf_counter()
        try:
            if raw is not None:
                r = requests.post(url + "/submit", data=raw, timeout=180,
                                  headers={"Content-Type": "application/json"})
            else:
                r = requests.post(url + "/submit", json=body, timeout=180)
            status, rid = r.status_code, r.headers.get("X-Request-ID")
        except requests.RequestException as exc:
            status, rid = f"EXC {type(exc).__name__}", None
        ms = round((time.perf_counter() - t0) * 1000, 1)
        sent.append({"phase": phase, "expected": expected, "status": status,
                     "request_id": rid, "client_ms": ms})
        say(f"  {phase:<10} {str(status):<5} {ms:>9.1f} ms")
        return status

    texts = own_writing_texts()
    tag = f"cost{stamp}"

    say("cold:")
    post("cold", 200, {"text": texts[0], "creator_id": f"{tag}_cold"})

    say(f"warm x{n}:")
    for i in range(n):
        post("warm", 200, {"text": texts[i % len(texts)], "creator_id": f"{tag}_w{i+1}"})

    say("bad path:")
    post("blank", 400, {"text": "   ", "creator_id": f"{tag}_blank"})
    post("short", 422, {"text": "far too short", "creator_id": f"{tag}_short"})
    post("array", 400, raw="[1, 2, 3]")
    for i in range(7):
        post("flood", 200 if i < config.RATE_LIMIT_PER_MINUTE else 429,
             {"text": texts[1], "creator_id": f"{tag}_flood"})

    if proc is not None:
        proc.terminate()
        try:
            proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            proc.kill()

    # Read back exactly the records this run wrote.
    all_lines = config.REQUEST_LOG.read_text(encoding="utf-8").splitlines()
    records = [json.loads(l) for l in all_lines[lines_before:] if l.strip()]
    by_id = {r.get("request_id"): r for r in records}
    for s in sent:
        s["record"] = by_id.get(s["request_id"])

    def recs(phase):
        return [s["record"] for s in sent if s["phase"] == phase and s["record"]]

    cold = recs("cold")
    warm = [r for r in recs("warm") if r["http_status"] == 200]
    stage_names = ["validate", "model_signal", "style_signal", "score_label", "audit_write"]
    warm_stages = {k: summarise([r["stages_ms"][k] for r in warm
                                 if r.get("stages_ms") and k in r["stages_ms"]])
                   for k in stage_names}
    warm_total = statistics.mean([r["duration_ms"] for r in warm]) if warm else None

    result = {
        "label": label,
        "stamp": stamp,
        "url": url,
        "startup_s": startup_s,
        "cold": {
            "duration_ms": cold[0]["duration_ms"] if cold else None,
            "cpu_s": cold[0]["cpu_s"] if cold else None,
            "model_signal_ms": (cold[0].get("stages_ms") or {}).get("model_signal") if cold else None,
            "rss_mb": cold[0]["rss_mb"] if cold else None,
            "status": cold[0]["http_status"] if cold else None,
        },
        "warm": {
            "duration_ms": summarise([r["duration_ms"] for r in warm]),
            "cpu_s": summarise([r["cpu_s"] for r in warm]),
            "client_ms": summarise([s["client_ms"] for s in sent
                                    if s["phase"] == "warm" and s["status"] == 200]),
            "words": summarise([r["input"]["words"] for r in warm]),
            "ok": f"{len(warm)}/{n}",
        },
        "stages_ms": warm_stages,
        "stage_share": ({k: round(100 * v["mean"] / warm_total, 1)
                         for k, v in warm_stages.items() if v.get("n")}
                        if warm_total else {}),
        "peak_rss_mb": max((r["rss_mb"] or 0) for r in records) if records else None,
        "bad_path": [{"phase": s["phase"], "expected": s["expected"], "status": s["status"],
                      "logged_outcome": (s["record"] or {}).get("outcome")}
                     for s in sent if s["phase"] in ("blank", "short", "array", "flood")],
        "sent": len(sent),
        "logged": sum(1 for s in sent if s["record"]),
        "records": records,
        "sent_detail": [{k: v for k, v in s.items() if k != "record"} for s in sent],
    }
    return result


# ── the report ────────────────────────────────────────────────────────────────

def to_markdown(r):
    w, c = r["warm"], r["cold"]
    lines = [
        f"# Cost run {r['stamp']}" + (f" — {r['label']}" if r["label"] else ""),
        "",
        f"`python measure_cost.py --label {r['label'] or '...'}` against `{r['url']}` "
        f"(started fresh by the script: {'yes' if r['startup_s'] is not None else 'no'}).",
        "",
        "## Summary",
        "",
        "| Measure | Value |",
        "|---|---|",
        f"| Process start → /health answers | {r['startup_s']} s |",
        f"| Cold /submit (first, loads GPT-2) | {c['duration_ms']} ms, {c['cpu_s']} CPU s, "
        f"model stage {c['model_signal_ms']} ms |",
        f"| Warm /submit, server-side duration | mean {w['duration_ms'].get('mean')} ms, "
        f"p50 {w['duration_ms'].get('p50')}, p95 {w['duration_ms'].get('p95')}, "
        f"max {w['duration_ms'].get('max')} (n={w['duration_ms'].get('n')}) |",
        f"| Warm /submit, client round trip | mean {w['client_ms'].get('mean')} ms, "
        f"p95 {w['client_ms'].get('p95')} |",
        f"| **Warm CPU seconds per run** | **mean {w['cpu_s'].get('mean')} s** "
        f"(min {w['cpu_s'].get('min')}, max {w['cpu_s'].get('max')}) |",
        f"| Peak resident memory | {r['peak_rss_mb']} MB |",
        f"| Warm submissions that returned 200 | {w['ok']} |",
        f"| Requests sent / found in requests.jsonl | {r['sent']} / {r['logged']} |",
        "",
        "## Where the time goes (warm, mean ms)",
        "",
        "| Stage | mean | p95 | share of total |",
        "|---|---|---|---|",
    ]
    for k, v in r["stages_ms"].items():
        if v.get("n"):
            lines.append(f"| {k} | {v['mean']} | {v['p95']} | {r['stage_share'].get(k)}% |")
    lines += ["", "## Bad path", "", "| Request | Expected | Got | Logged outcome |",
              "|---|---|---|---|"]
    for b in r["bad_path"]:
        lines.append(f"| {b['phase']} | {b['expected']} | {b['status']} | {b['logged_outcome']} |")
    lines += ["", "## Every request sent", "", "```json"]
    lines += [json.dumps(s) for s in r["sent_detail"]]
    lines += ["```", "", "## The records this run wrote to logs/requests.jsonl", "", "```json"]
    lines += [json.dumps(x, ensure_ascii=False) for x in r["records"]]
    lines += ["```", ""]
    return "\n".join(lines)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--label", default="")
    p.add_argument("--n", type=int, default=10, help="warm submissions (default 10)")
    p.add_argument("--port", type=int, default=5055)
    p.add_argument("--url", default=None, help="use a running server instead of starting one")
    args = p.parse_args()

    r = run_once(label=args.label, n=args.n, port=args.port, url=args.url)
    config.RESULTS_DIR.mkdir(exist_ok=True)
    name = f"cost_{dt.datetime.now():%Y-%m-%d_%H%M}" + (f"_{args.label}" if args.label else "") + ".md"
    out = config.RESULTS_DIR / name
    out.write_text(to_markdown(r), encoding="utf-8")

    w = r["warm"]
    print()
    print(f"startup {r['startup_s']} s | cold {r['cold']['duration_ms']} ms | "
          f"warm mean {w['duration_ms'].get('mean')} ms p95 {w['duration_ms'].get('p95')} | "
          f"warm CPU {w['cpu_s'].get('mean')} s | peak RSS {r['peak_rss_mb']} MB | "
          f"logged {r['logged']}/{r['sent']}")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

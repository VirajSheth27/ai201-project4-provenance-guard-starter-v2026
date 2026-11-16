#!/usr/bin/env python3
"""
Provenance Guard on a production server — capstone (unit 9).

    python serve.py

One command, on any OS. `python app.py` runs Flask's development server, which
says so on startup because it isn't meant to serve anyone. `gunicorn` is the
usual answer, but it needs `fork()` and doesn't run on Windows at all. Waitress
is a pure-Python WSGI server that runs the same everywhere, so this is the
start command RUNNING.md documents.

Settings come from the environment, the same as app.py:

    HOST            127.0.0.1 (loopback). Use 0.0.0.0 to accept outside traffic
    PORT            5000
    AI201_THREADS   4 — worker threads waitress uses for requests
    AI201_WARMUP    1 — load GPT-2 and run one pass before accepting traffic
                        (0 = the "before" behaviour: the first /submit loads it)

Every request is recorded in logs/requests.jsonl (see telemetry.py). Debug mode
is never on here: waitress doesn't use Flask's debugger.
"""

import os
import time

from waitress import serve

import config
import detector
import telemetry
from app import app

# Capstone improvement (Milestone 6). Before: the first /submit after a start
# paid for loading GPT-2, 6.5–10.7 s in the "before" trials, with 98% of it in
# the model_signal stage. Now the server pays it once, BEFORE it accepts
# traffic, and no writer waits for it. The cost doesn't disappear: it moves
# into startup, and /health doesn't answer until it's done.
WARMUP_TEXT = (
    "The service loads its language model before it accepts any requests, so "
    "that the first writer to submit does not wait for the model to load."
)


def warm_up() -> None:
    """Load GPT-2 and run one forward pass, and log what it cost."""
    t0, cpu0 = time.perf_counter(), time.process_time()
    outcome, error = "warmup", None
    try:
        detector.warm_up()                  # load weights + tokenizer
        detector.model_signal(WARMUP_TEXT)  # first forward pass: torch's one-time setup
    except Exception as exc:  # noqa: BLE001 — serve anyway; /submit will answer 503
        outcome, error = "warmup_failed", f"{type(exc).__name__}: {exc}"[:300]
    record = {
        "timestamp": telemetry.now_iso(),
        "request_id": None,
        "route": "(startup)",
        "method": "WARMUP",
        "http_status": None,
        "outcome": outcome,
        "duration_ms": round((time.perf_counter() - t0) * 1000, 2),
        "cpu_s": round(time.process_time() - cpu0, 4),
        "rss_mb": telemetry.rss_mb(),
        "detector_loaded": detector._model is not None,
    }
    if error:
        record["exception"] = error
    telemetry.log_request(record)
    print(f"  warm-up:         {outcome} in {record['duration_ms'] / 1000:.1f} s "
          f"({record['cpu_s']} CPU s, {record['rss_mb']} MB)", flush=True)


def main():
    threads = int(os.getenv("AI201_THREADS", "4"))
    print(f"Provenance Guard (waitress) on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off'}"
          f"  ({config.RATE_LIMIT_PER_MINUTE}/min, {config.RATE_LIMIT_PER_DAY}/day per creator)")
    print(f"  threads:         {threads}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print(f"  request log:     {config.REQUEST_LOG}")
    if os.getenv("AI201_WARMUP", "1") == "1":
        warm_up()
    else:
        print("  warm-up:         off (AI201_WARMUP=0): the first /submit loads the model")
    print(flush=True)
    serve(app, host=config.HOST, port=config.PORT, threads=threads)


if __name__ == "__main__":
    main()

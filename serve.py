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

Every request is recorded in logs/requests.jsonl (see telemetry.py). Debug mode
is never on here: waitress doesn't use Flask's debugger.
"""

import os

from waitress import serve

import config
from app import app


def main():
    threads = int(os.getenv("AI201_THREADS", "4"))
    print(f"Provenance Guard (waitress) on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}  (loads on first /submit)")
    print(f"  rate limiting:   {'ON' if config.RATE_LIMITING_ENABLED else 'off'}"
          f"  ({config.RATE_LIMIT_PER_MINUTE}/min, {config.RATE_LIMIT_PER_DAY}/day per creator)")
    print(f"  threads:         {threads}")
    print(f"  audit log:       {config.AUDIT_LOG}")
    print(f"  request log:     {config.REQUEST_LOG}")
    print(flush=True)
    serve(app, host=config.HOST, port=config.PORT, threads=threads)


if __name__ == "__main__":
    main()

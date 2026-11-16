"""
The request log — capstone (unit 9).

`audit.jsonl` answers "what did the service decide?". This file answers a
different question: "what did the service *do*, how long did it take, and
what did it cost?" One JSON object per line, one line per request, for every
route and every outcome — a 200, a 400, a 429 and a crash all leave a record.

    logs/requests.jsonl

The two logs join on `content_id`.

**No submitted text is ever written here.** An input is recorded as a short
hash, its character count and its word count. That's enough to tell whether two
requests sent the same text, and to see whether latency tracks length, without
storing anyone's writing.

    import telemetry
    with telemetry.stage("model"):
        ...
    telemetry.log_request({...})
"""

import hashlib
import json
import threading
import time
from contextlib import contextmanager
from datetime import datetime, timezone

import config

_lock = threading.Lock()

try:  # Memory is worth knowing (it's why this can't be hosted for free), but
    import psutil  # it isn't worth crashing the service over.
    _process = psutil.Process()
except ImportError:  # pragma: no cover
    _process = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def input_fingerprint(text) -> dict | None:
    """What came in, without keeping it: a 12-char sha256 prefix, chars, words."""
    if not isinstance(text, str):
        return None
    return {
        "sha256_12": hashlib.sha256(text.encode("utf-8")).hexdigest()[:12],
        "chars": len(text),
        "words": len(text.split()),
    }


def rss_mb() -> float | None:
    """Resident memory of this process, in MB. None if psutil isn't there."""
    if _process is None:
        return None
    return round(_process.memory_info().rss / (1024 * 1024), 1)


@contextmanager
def stage(name: str, into: dict):
    """
    Time one stage of a request into `into[name]`, in milliseconds.

    The time is recorded even if the stage raises, so a stage that failed
    still shows how long it ran before it did.
    """
    start = time.perf_counter()
    try:
        yield
    finally:
        into[name] = round((time.perf_counter() - start) * 1000, 2)


def log_request(record: dict) -> dict:
    """Append one request record to `logs/requests.jsonl`."""
    config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False)
    with _lock:
        with config.REQUEST_LOG.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
    return record


def read_requests(limit: int | None = None) -> list[dict]:
    """Read the request log back, oldest first. Bad lines are skipped."""
    if not config.REQUEST_LOG.exists():
        return []
    out = []
    for line in config.REQUEST_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out[-limit:] if limit else out

#!/usr/bin/env python3
"""
Criterion 5: does a fresh checkout reproduce a working service? — capstone.

    python fresh_clone_check.py --label before          # 3 clones
    python fresh_clone_check.py --label before --keep   # leave the folders

For each clone it follows the "Setup from a clean checkout" steps in
RUNNING.md, in order, in a brand-new folder with a brand-new venv:

    git clone <this repo>            (the COMMITTED HEAD — uncommitted work isn't in it)
    py -3.13 -m venv .venv           (python3.13 off Windows)
    python --version                 must be 3.11–3.13
    pip install -r requirements.txt
    python detector.py
    python test.py                   must end "0 failed"
    python serve.py                  then GET /health -> 200
    POST /submit                     -> 200 with a `guess`, and a matching
                                        record (by X-Request-ID) in the
                                        CLONE's logs/requests.jsonl

As criterion 5 allows, the machine's pip cache and Hugging Face model cache are
shared; nothing project-specific is copied between clones. The server each
clone starts is this script's own child process and is stopped when the check
ends. Clone folders live in the system temp dir and are deleted afterwards
unless --keep (each venv is ~1 GB).

Writes results/fresh_clone_<label>.json and .md.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests

import config

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent
WINDOWS = os.name == "nt"
SAMPLE = ("I tried using that new AI writer for my history paper last night, and "
          "honestly it was weird. It kept saying things I would never say.")


def run(cmd, cwd, env, timeout):
    t0 = time.perf_counter()
    p = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    return p.returncode, (p.stdout or "") + (p.stderr or ""), round(time.perf_counter() - t0, 1)


def check_one(n, label, port, keep):
    stamp = dt.datetime.now().strftime("%H%M%S")
    folder = Path(tempfile.gettempdir()) / "pg_fresh_clones" / f"{label}_{n}_{stamp}"
    folder.parent.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if k not in ("VIRTUAL_ENV", "PYTHONHOME")}
    steps = []

    def step(name, ok, detail):
        steps.append({"step": name, "ok": bool(ok), "detail": detail})
        print(f"  [{n}] {name:<14} {'ok ' if ok else 'FAIL'} {detail}")
        return ok

    server = None
    try:
        code, out, s = run(["git", "clone", "-q", str(ROOT), str(folder)], None, env, 300)
        head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=folder,
                              capture_output=True, text=True).stdout.strip() if code == 0 else "?"
        if not step("git clone", code == 0, f"HEAD {head}, {s}s"):
            return steps
        venv_cmd = (["py", "-3.13", "-m", "venv", ".venv"] if WINDOWS
                    else ["python3.13", "-m", "venv", ".venv"])
        code, out, s = run(venv_cmd, folder, env, 300)
        if not step("venv", code == 0, f"{' '.join(venv_cmd)}, {s}s"):
            return steps
        py = str(folder / ".venv" / ("Scripts/python.exe" if WINDOWS else "bin/python"))
        code, out, s = run([py, "--version"], folder, env, 60)
        ver = out.strip()
        ok_ver = any(ver.startswith(f"Python 3.{m}.") for m in (11, 12, 13))
        if not step("python ver", ok_ver, ver):
            return steps
        code, out, s = run([py, "-m", "pip", "install", "-q", "-r", "requirements.txt"],
                           folder, env, 1800)
        if not step("pip install", code == 0, f"exit {code}, {s}s"
                    + ("" if code == 0 else " | " + out.strip().splitlines()[-1][:150])):
            return steps
        code, out, s = run([py, "detector.py"], folder, env, 900)
        sig = next((l for l in out.splitlines() if l.startswith("model_signal")), "")
        if not step("detector.py", code == 0, f"{sig.strip()} ({s}s)"):
            return steps
        code, out, s = run([py, "test.py"], folder, env, 900)
        summary = next((l for l in out.splitlines() if "passed" in l and "failed" in l), "").strip()
        if not step("test.py", code == 0 and " 0 failed" in summary, summary or f"exit {code}"):
            return steps

        senv = dict(env, PORT=str(port), HOST="127.0.0.1")
        server = subprocess.Popen([py, "serve.py"], cwd=folder, env=senv,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        url = f"http://127.0.0.1:{port}"
        status, deadline = None, time.time() + 120
        while time.time() < deadline and server.poll() is None:
            try:
                status = requests.get(url + "/health", timeout=2).status_code
                break
            except requests.RequestException:
                time.sleep(0.3)
        if not step("GET /health", status == 200, f"HTTP {status}"):
            return steps

        r = requests.post(url + "/submit", json={"text": SAMPLE, "creator_id": f"clone{n}"},
                          timeout=180)
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        rid = r.headers.get("X-Request-ID")
        log = folder / "logs" / "requests.jsonl"
        recs = [json.loads(l) for l in log.read_text(encoding="utf-8").splitlines()
                if l.strip()] if log.exists() else []
        match = next((x for x in recs if x.get("request_id") == rid), None)
        ok = r.status_code == 200 and "guess" in body and match is not None
        step("POST /submit", ok,
             f"HTTP {r.status_code}, guess={body.get('guess')}, request_id {rid} "
             f"{'found' if match else 'NOT found'} in clone's requests.jsonl")
        return steps
    except Exception as exc:  # noqa: BLE001 — a crash in a step is a failed clone, recorded
        step("error", False, f"{type(exc).__name__}: {exc}"[:200])
        return steps
    finally:
        if server is not None:
            server.terminate()
            try:
                server.wait(timeout=15)
            except subprocess.TimeoutExpired:
                server.kill()
        if not keep:
            shutil.rmtree(folder, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--label", required=True)
    p.add_argument("--clones", type=int, default=3)
    p.add_argument("--port", type=int, default=5081)
    p.add_argument("--keep", action="store_true")
    args = p.parse_args()

    clones = []
    for n in range(1, args.clones + 1):
        print(f"\n=== clone {n}/{args.clones} ===")
        t0 = time.perf_counter()
        steps = check_one(n, args.label, args.port + n, args.keep)
        passed = len(steps) == 9 and all(s["ok"] for s in steps)
        failed = next((s["step"] for s in steps if not s["ok"]), None)
        summary = (f"9/9 steps, {round(time.perf_counter() - t0)} s" if passed
                   else f"failed at {failed}")
        clones.append({"n": n, "passed": passed, "summary": summary, "steps": steps})

    config.RESULTS_DIR.mkdir(exist_ok=True)
    data = {"label": args.label, "when": dt.datetime.now().isoformat(timespec="seconds"),
            "clones": clones}
    (config.RESULTS_DIR / f"fresh_clone_{args.label}.json").write_text(
        json.dumps(data, indent=1), encoding="utf-8")
    md = [f"# Fresh-clone check — {args.label}", "", f"{data['when']}, "
          f"`python fresh_clone_check.py --label {args.label}`", "", "```"]
    for c in clones:
        md.append(f"clone {c['n']}: {'PASS' if c['passed'] else 'FAIL'}: {c['summary']}")
        md += [f"   {s['step']:<14} {'ok ' if s['ok'] else 'FAIL'} {s['detail']}" for s in c["steps"]]
    md += ["```", ""]
    (config.RESULTS_DIR / f"fresh_clone_{args.label}.md").write_text("\n".join(md), encoding="utf-8")
    print(f"\n{sum(c['passed'] for c in clones)}/{len(clones)} clones passed; "
          f"wrote results/fresh_clone_{args.label}.json")


if __name__ == "__main__":
    main()

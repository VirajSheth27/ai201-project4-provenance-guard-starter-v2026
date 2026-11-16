# Fresh-clone check — after

2026-11-15T23:13:15, `python fresh_clone_check.py --label after`

```
clone 1: PASS: 8/8 steps, 318 s
   git clone      ok  HEAD fb9aa1a, 0.2s
   venv           ok  py -3.13 -m venv .venv, 12.6s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 278.0s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (13.3s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id a3dba29dda72 found in clone's requests.jsonl
clone 2: PASS: 8/8 steps, 313 s
   git clone      ok  HEAD fb9aa1a, 0.2s
   venv           ok  py -3.13 -m venv .venv, 11.7s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 271.7s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (14.0s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id 17cf9f4619ea found in clone's requests.jsonl
clone 3: PASS: 8/8 steps, 294 s
   git clone      ok  HEAD fb9aa1a, 0.2s
   venv           ok  py -3.13 -m venv .venv, 12.3s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 252.7s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (13.6s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id 7524bead5d2d found in clone's requests.jsonl
```

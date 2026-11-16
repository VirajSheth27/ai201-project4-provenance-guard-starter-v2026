# Fresh-clone check — before

2026-11-15T22:47:45, `python fresh_clone_check.py --label before` (re-scored 2026-11-15T22:50:15)

```
clone 1: PASS: 8/8 steps
   git clone      ok  HEAD bca6742, 0.2s
   venv           ok  py -3.13 -m venv .venv, 10.5s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 260.1s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (12.9s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id 3a909e22369e found in clone's requests.jsonl
clone 2: PASS: 8/8 steps
   git clone      ok  HEAD bca6742, 0.2s
   venv           ok  py -3.13 -m venv .venv, 11.6s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 262.1s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (13.0s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id 78d2a1fda9fd found in clone's requests.jsonl
clone 3: PASS: 8/8 steps
   git clone      ok  HEAD bca6742, 0.2s
   venv           ok  py -3.13 -m venv .venv, 12.1s
   python ver     ok  Python 3.13.15
   pip install    ok  exit 0, 262.9s
   detector.py    ok  model_signal   0.8864   (higher = more likely AI) (12.7s)
   test.py        ok  9 passed, 0 failed, 0 to look at, 0 skipped
   GET /health    ok  HTTP 200
   POST /submit   ok  HTTP 200, guess=human, request_id b027632d6fd2 found in clone's requests.jsonl
```

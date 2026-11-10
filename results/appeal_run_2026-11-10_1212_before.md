# Appeal run — before

- Produced by: `run_appeals.py::main`
- Service: `app.py::submit` then `app.py::appeal`; checked against `logs/audit.jsonl`
- 3 trials · 2026-11-10 12:12

| Check | Target | Run 1 | Run 2 | Run 3 |
|---|---|---|---|---|
| Real appeals: 200, under_review, logged with exact reasoning, original unchanged | 5 of 5 | 5/5 | 5/5 | 5/5 |
| Fake ids: 404 and no appeal logged | 2 of 2 | 2/2 | 2/2 | 2/2 |

---

## What actually came back

**Trial 1**

```json
{
  "real": [
    {
      "content_id": "642627f600854f9fbfa9cb1cba4dfafb",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 1: I wrote this myself and can show my drafts. (e4aafc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "642627f600854f9fbfa9cb1cba4dfafb",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "b5bd17b3428748a0a67d71fd752ab893",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 2: I wrote this myself and can show my drafts. (e4aafc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "b5bd17b3428748a0a67d71fd752ab893",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "c12b48c0007d4704b5297f10d43cdba0",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 3: I wrote this myself and can show my drafts. (e4aafc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "c12b48c0007d4704b5297f10d43cdba0",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "2a7431b25cdb42d0aa6a69dfd81cf841",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 4: I wrote this myself and can show my drafts. (e4aafc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "2a7431b25cdb42d0aa6a69dfd81cf841",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "d2c3363cb3244a7da27270334dfb75d4",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 5: I wrote this myself and can show my drafts. (e4aafc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "d2c3363cb3244a7da27270334dfb75d4",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    }
  ],
  "fake": [
    {
      "content_id": "fakee4aafct1n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fakee4aafct1n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fakee4aafct1n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fakee4aafct1n2'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    }
  ]
}
```

**Trial 2**

```json
{
  "real": [
    {
      "content_id": "a7d8303a45894d12ac23bb8093a787a1",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 1: I wrote this myself and can show my drafts. (2e9e3c)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "a7d8303a45894d12ac23bb8093a787a1",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "208dd7e9c0a44cc4a6697cb117763324",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 2: I wrote this myself and can show my drafts. (2e9e3c)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:21+00:00",
        "content_id": "208dd7e9c0a44cc4a6697cb117763324",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "146a2d9b410a47ae8c2ed66ccafac0da",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 3: I wrote this myself and can show my drafts. (2e9e3c)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:22+00:00",
        "content_id": "146a2d9b410a47ae8c2ed66ccafac0da",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "8b21b0631b4a469598f2052dd7132112",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 4: I wrote this myself and can show my drafts. (2e9e3c)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:22+00:00",
        "content_id": "8b21b0631b4a469598f2052dd7132112",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "e58e8d058374486c9635feed930c041f",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 5: I wrote this myself and can show my drafts. (2e9e3c)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:22+00:00",
        "content_id": "e58e8d058374486c9635feed930c041f",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    }
  ],
  "fake": [
    {
      "content_id": "fake2e9e3ct2n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake2e9e3ct2n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fake2e9e3ct2n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake2e9e3ct2n2'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    }
  ]
}
```

**Trial 3**

```json
{
  "real": [
    {
      "content_id": "0a300b6eb028417dbc44c60fad4c2de7",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 1: I wrote this myself and can show my drafts. (7b2fcc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:22+00:00",
        "content_id": "0a300b6eb028417dbc44c60fad4c2de7",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "5ff0ea0cc60640d980f85330338803d3",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 2: I wrote this myself and can show my drafts. (7b2fcc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:22+00:00",
        "content_id": "5ff0ea0cc60640d980f85330338803d3",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "a3168747ffe846babd4ae6563752b2f4",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 3: I wrote this myself and can show my drafts. (7b2fcc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:23+00:00",
        "content_id": "a3168747ffe846babd4ae6563752b2f4",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "e4af65ad66b7472d9b328e51c23a9e65",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 4: I wrote this myself and can show my drafts. (7b2fcc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:23+00:00",
        "content_id": "e4af65ad66b7472d9b328e51c23a9e65",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    },
    {
      "content_id": "bb83062815214a71a0e6acf639f8b239",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 5: I wrote this myself and can show my drafts. (7b2fcc)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:12:23+00:00",
        "content_id": "bb83062815214a71a0e6acf639f8b239",
        "message": "Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.",
        "status": "under_review"
      },
      "checks": {
        "returned_200": true,
        "response_under_review": true,
        "appeal_entry_logged": true,
        "logged_under_review": true,
        "reasoning_exact": true,
        "original_unchanged": true
      },
      "passed": true
    }
  ],
  "fake": [
    {
      "content_id": "fake7b2fcct3n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake7b2fcct3n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fake7b2fcct3n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake7b2fcct3n2'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    }
  ]
}
```

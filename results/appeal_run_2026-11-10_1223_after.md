# Appeal run — after

- Produced by: `run_appeals.py::main`
- Service: `app.py::submit` then `app.py::appeal`; checked against `logs/audit.jsonl`
- 3 trials · 2026-11-10 12:23

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
      "content_id": "ec930821e47e498f99ed208c449873b4",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 1: I wrote this myself and can show my drafts. (0b8270)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:47+00:00",
        "content_id": "ec930821e47e498f99ed208c449873b4",
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
      "content_id": "70a8e6808a304c3ab4df1cbffda20141",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 2: I wrote this myself and can show my drafts. (0b8270)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:47+00:00",
        "content_id": "70a8e6808a304c3ab4df1cbffda20141",
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
      "content_id": "8a284a23296c440f84b8a6d126275f16",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 3: I wrote this myself and can show my drafts. (0b8270)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:47+00:00",
        "content_id": "8a284a23296c440f84b8a6d126275f16",
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
      "content_id": "b8df3e57e310478fa7ba778c17165c41",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 4: I wrote this myself and can show my drafts. (0b8270)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:47+00:00",
        "content_id": "b8df3e57e310478fa7ba778c17165c41",
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
      "content_id": "5a8ecd14aaa44cbba746ec2d09d48f80",
      "submit_status": 200,
      "reasoning": "Trial 1, piece 5: I wrote this myself and can show my drafts. (0b8270)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:47+00:00",
        "content_id": "5a8ecd14aaa44cbba746ec2d09d48f80",
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
      "content_id": "fake0b8270t1n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake0b8270t1n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fake0b8270t1n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake0b8270t1n2'. Check it matches the one you got back from /submit."
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
      "content_id": "5238068663844c6d8271a09042d33fc4",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 1: I wrote this myself and can show my drafts. (ffe748)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "5238068663844c6d8271a09042d33fc4",
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
      "content_id": "8de0dfdb6402471889b498f93eed23f0",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 2: I wrote this myself and can show my drafts. (ffe748)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "8de0dfdb6402471889b498f93eed23f0",
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
      "content_id": "b50a2272ca75410e945bec9a3c6ad962",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 3: I wrote this myself and can show my drafts. (ffe748)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "b50a2272ca75410e945bec9a3c6ad962",
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
      "content_id": "44d4cf4945624e73b5f9a90f8f76c579",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 4: I wrote this myself and can show my drafts. (ffe748)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "44d4cf4945624e73b5f9a90f8f76c579",
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
      "content_id": "ead0a6c9828a46f79d040b5e718614f4",
      "submit_status": 200,
      "reasoning": "Trial 2, piece 5: I wrote this myself and can show my drafts. (ffe748)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "ead0a6c9828a46f79d040b5e718614f4",
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
      "content_id": "fakeffe748t2n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fakeffe748t2n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fakeffe748t2n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fakeffe748t2n2'. Check it matches the one you got back from /submit."
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
      "content_id": "11d6be516580426b9e81a62e1aa20126",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 1: I wrote this myself and can show my drafts. (59363b)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "11d6be516580426b9e81a62e1aa20126",
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
      "content_id": "370c438215eb4b1486247cee4835ba7b",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 2: I wrote this myself and can show my drafts. (59363b)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:48+00:00",
        "content_id": "370c438215eb4b1486247cee4835ba7b",
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
      "content_id": "b447ba574e3b4fc0835acc14d64551fd",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 3: I wrote this myself and can show my drafts. (59363b)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:49+00:00",
        "content_id": "b447ba574e3b4fc0835acc14d64551fd",
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
      "content_id": "c19e41a663844797a2e7e7a3d0a6e348",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 4: I wrote this myself and can show my drafts. (59363b)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:49+00:00",
        "content_id": "c19e41a663844797a2e7e7a3d0a6e348",
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
      "content_id": "b4ede9dba4524e9b9afdae4010656a2f",
      "submit_status": 200,
      "reasoning": "Trial 3, piece 5: I wrote this myself and can show my drafts. (59363b)",
      "response_status": 200,
      "response": {
        "appealed_at": "2026-11-10T17:23:49+00:00",
        "content_id": "b4ede9dba4524e9b9afdae4010656a2f",
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
      "content_id": "fake59363bt3n1",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake59363bt3n1'. Check it matches the one you got back from /submit."
      },
      "checks": {
        "returned_404": true,
        "no_appeal_logged": true
      },
      "passed": true
    },
    {
      "content_id": "fake59363bt3n2",
      "response_status": 404,
      "response": {
        "error": "not_found",
        "message": "No submission with content_id 'fake59363bt3n2'. Check it matches the one you got back from /submit."
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

# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 12:23
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `4a99a1a952af4d90ab1efb176115783d` | unsure | 0.436 | BROKE — AI text labelled unsure |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `b9867221cf1a475bb69e56556569e2bb` | human | 0.329 | BROKE — AI text labelled human |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `0553902887b040e58e3178cf1c88aa77` | unsure | 0.460 | BROKE — AI text labelled unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `28b27431e9614d38aa554eaa3f691ef5` | unsure | 0.649 | BROKE — AI text labelled unsure |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `87183d246df547af9e3e008d3ec64d2b` | human | 0.212 | BROKE — AI text labelled human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `094c670e20184702bc0fdafbdec546bc` | human | 0.344 | BROKE — AI text labelled human |
| EV07 | evasion | signal two: padding with punctuation | 200 | `b2441c6078e54771b31b2add3adb43a3` | unsure | 0.502 | BROKE — AI text labelled unsure |
| EV08 | evasion | signal one: text below the token window | 200 | `dd0bac8d0d344811b790d937786e872c` | unsure | 0.374 | BROKE — AI text labelled unsure |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `ccdf20be434f44bdb48240edd997df31` | unsure | 0.467 | BROKE — AI text labelled unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `492a8b3f9b0445e49eceb702719a7b6e` | unsure | 0.690 | BROKE — AI text labelled unsure |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `35f0b246e79d4616b63eb9010cc06bf7` | unsure | 0.504 | HELD — unsure, not accused |
| FP02 | false_positive | human writing in a formal register | 200 | `606ce9a80625483cb9d70d6be9e53e6e` | ai | 0.758 | BROKE — real writer labelled ai |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `724f46e73fba49e9a8d05b0e6f1ca8ce` | unsure | 0.693 | HELD — unsure, not accused |
| FP04 | false_positive | a student essay written to a rubric | 200 | `2e19cbbd58d64d0195f22bd83225aa25` | unsure | 0.675 | HELD — unsure, not accused |
| FP05 | false_positive | technical documentation written by a person | 200 | `6416cde3ee914a36b0cba6d49f4ea40e` | ai | 0.799 | BROKE — real writer labelled ai |
| FP06 | false_positive | a person imitating a formal template | 200 | `9fe5f9a541ff48f097230c8fd4da7358` | unsure | 0.616 | HELD — unsure, not accused |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `9b49c747f7c0410a852300d52c88205d` | unsure | 0.584 | HELD — unsure, not accused |
| FP08 | false_positive | very short genuine human submission | 200 | `ecde4a82d2e345b9b00ce3abbb52548b` | human | 0.294 | HELD — human, not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `70c7ae6199f84e2c9488d4c7fde0a000` | human | 0.241 | BROKE — asked for human, got human |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `04a0355db8c44d56a06894b6b6240827` | human | 0.102 | BROKE — asked for human, got human |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `6170968ace9841278155619e597f8d7a` | unsure | 0.516 | HELD — asked for human, got unsure |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `da30e8cd033b45c2b016619ee8a7e141` | unsure | 0.463 | HELD — label fixed text; log entry intact |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `bd695a4c4950473d8e88f48f7fa03821` | unsure | 0.422 | HELD — label fixed text; log entry intact |
| PI06 | prompt_injection | instruction plus real human text | 200 | `851cfaacbce0415eb10e9f7aa1b4797c` | unsure | 0.480 | HELD — asked for human, got unsure |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD — 400 |
| MF02 | malformed | text is a single character | 422 | `—` | — | — | HELD — 422 |
| MF03 | malformed | text is control characters | 422 | `—` | — | — | HELD — 422 |
| MF04 | malformed | text is only punctuation | 200 | `7c469ad21a614a4098dcd2bd98a8de5c` | unsure | 0.506 | BROKE — 200 and a label for text with no words |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — | HELD — 422 |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — | HELD — 422 |
| MF07 | malformed | text is right-to-left script | 200 | `4e1cb148fe164605a43a8df9661a9fd7` | ai | 0.953 | BROKE — Arabic labelled ai |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD — 413 |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD — 400 |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD — 400 |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD — 400 |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD — 400 |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD — 400 |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD — 400 |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD — 400 |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD — 400 |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD — 400 |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD — 429 from the IP bucket; never reached the route |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD — 429 from the IP bucket; never reached the route |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD — 400 |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `174a606a34b44c73b28303f4e8705171` | human | 0.014 | HELD — 200 |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b145bcbc59de49a69d05c2128ca401fe` | human | 0.014 | HELD — 200 |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fd0051f0b7f14be18499b43182042d09` | human | 0.014 | HELD — 200 |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e4f93db2f8624b6c98c2c71bcb32eb59` | human | 0.014 | HELD — 200 |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d30751464cbc45b4b7b8c8a6c2da8e3a` | human | 0.014 | HELD — 200 |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 429 |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "4a99a1a952af4d90ab1efb176115783d",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4364,
  "model_score": 0.1635,
  "style_score": 0.7093,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "b9867221cf1a475bb69e56556569e2bb",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.329,
  "model_score": 0.5943,
  "style_score": 0.0637,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "0553902887b040e58e3178cf1c88aa77",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4603,
  "model_score": 0.6662,
  "style_score": 0.2544,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "28b27431e9614d38aa554eaa3f691ef5",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6492,
  "model_score": 0.6114,
  "style_score": 0.687,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "87183d246df547af9e3e008d3ec64d2b",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2123,
  "model_score": 0.3212,
  "style_score": 0.1035,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "094c670e20184702bc0fdafbdec546bc",
  "creator_id": "attacker_EV06",
  "guess": "human",
  "confidence": 0.3442,
  "model_score": 0.5727,
  "style_score": 0.1156,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "b2441c6078e54771b31b2add3adb43a3",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5023,
  "model_score": 0.5862,
  "style_score": 0.4183,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "dd0bac8d0d344811b790d937786e872c",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.3743,
  "model_score": 0.2452,
  "style_score": 0.5034,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "ccdf20be434f44bdb48240edd997df31",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.4665,
  "model_score": 0.7042,
  "style_score": 0.2287,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "492a8b3f9b0445e49eceb702719a7b6e",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.9792,
  "style_score": 0.6128,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "35f0b246e79d4616b63eb9010cc06bf7",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.504,
  "model_score": 0.6175,
  "style_score": 0.3904,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "606ce9a80625483cb9d70d6be9e53e6e",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7579,
  "model_score": 0.7387,
  "style_score": 0.777,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "724f46e73fba49e9a8d05b0e6f1ca8ce",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6929,
  "model_score": 0.8051,
  "style_score": 0.5807,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "2e19cbbd58d64d0195f22bd83225aa25",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6753,
  "model_score": 0.8329,
  "style_score": 0.5177,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "6416cde3ee914a36b0cba6d49f4ea40e",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.7995,
  "model_score": 0.8005,
  "style_score": 0.7986,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "9fe5f9a541ff48f097230c8fd4da7358",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6157,
  "model_score": 0.8814,
  "style_score": 0.35,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "9b49c747f7c0410a852300d52c88205d",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.5837,
  "model_score": 0.8816,
  "style_score": 0.2857,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "ecde4a82d2e345b9b00ce3abbb52548b",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.2937,
  "model_score": 0.3223,
  "style_score": 0.2651,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "70c7ae6199f84e2c9488d4c7fde0a000",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.2408,
  "model_score": 0.4625,
  "style_score": 0.019,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "04a0355db8c44d56a06894b6b6240827",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.1022,
  "model_score": 0.2044,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "6170968ace9841278155619e597f8d7a",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5163,
  "model_score": 0.5943,
  "style_score": 0.4383,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "da30e8cd033b45c2b016619ee8a7e141",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4627,
  "model_score": 0.4998,
  "style_score": 0.4255,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "bd695a4c4950473d8e88f48f7fa03821",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.4221,
  "model_score": 0.6401,
  "style_score": 0.2041,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "851cfaacbce0415eb10e9f7aa1b4797c",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.4804,
  "model_score": 0.5583,
  "style_score": 0.4025,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "7c469ad21a614a4098dcd2bd98a8de5c",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.5056,
  "model_score": 0.0112,
  "style_score": 1.0,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "4e1cb148fe164605a43a8df9661a9fd7",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.9532,
  "model_score": 0.9064,
  "style_score": 1.0,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "174a606a34b44c73b28303f4e8705171",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0143,
  "model_score": 0.0287,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "b145bcbc59de49a69d05c2128ca401fe",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0143,
  "model_score": 0.0287,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "fd0051f0b7f14be18499b43182042d09",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0143,
  "model_score": 0.0287,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "e4f93db2f8624b6c98c2c71bcb32eb59",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0143,
  "model_score": 0.0287,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "d30751464cbc45b4b7b8c8a6c2da8e3a",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.0143,
  "model_score": 0.0287,
  "style_score": 0.0,
  "label": "We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
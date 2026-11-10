# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-10 11:56
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `4f6b431aed0d4e37998dc951416d13a8` | unsure | 0.445 | BROKE — AI text labelled unsure (typos) |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `a307dcdea0564cb88d514385474b721c` | unsure | 0.436 | BROKE — AI text labelled unsure |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `8bd8b01d3e754f408a13af4a4dde26c9` | unsure | 0.506 | BROKE — AI text labelled unsure |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `cb345abddc2e44e28327e82364f28d45` | unsure | 0.661 | BROKE — AI text labelled unsure, 0.661 |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `035b80da15a5425da26fc1af28055a85` | human | 0.286 | BROKE — AI text labelled human |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `1cbf0cb1ef02479bbd101da4dc44b8bb` | unsure | 0.444 | BROKE — AI text labelled unsure |
| EV07 | evasion | signal two: padding with punctuation | 200 | `20f3379842a74c5897a15fe30ca543f3` | unsure | 0.377 | BROKE — AI text labelled unsure |
| EV08 | evasion | signal one: text below the token window | 200 | `7f9c5c9fb715461fb3c14d1b8f96b450` | unsure | 0.449 | BROKE — AI text labelled unsure (2 sentences) |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `f6d20ce919774df69f64fba004c99bcd` | unsure | 0.537 | BROKE — AI text labelled unsure |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `abcef1933cfb4de086a9b4361d77ac1b` | ai | 0.854 | HELD — labelled ai |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `20c7d46fa753499e89afd042a3bafc9f` | unsure | 0.576 | HELD — unsure, not accused |
| FP02 | false_positive | human writing in a formal register | 200 | `f800be753d5a4c759285059cb1295b7b` | ai | 0.778 | BROKE — real writer labelled ai |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `b5d0423b308448109b009e857630d81c` | ai | 0.756 | BROKE — real writer labelled ai |
| FP04 | false_positive | a student essay written to a rubric | 200 | `bfeb047d40064883a0318eaa384550bf` | ai | 0.733 | BROKE — real writer labelled ai |
| FP05 | false_positive | technical documentation written by a person | 200 | `a97baa380272430fa3fe0f1ffbdecd55` | ai | 0.801 | BROKE — real writer labelled ai |
| FP06 | false_positive | a person imitating a formal template | 200 | `7c3d982082aa4a9184bdbb8d4d6296a9` | unsure | 0.690 | HELD — unsure at 0.690, 0.01 from ai |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `57ecdee949114f1c957782a75a8b2e20` | unsure | 0.657 | HELD — unsure, not accused |
| FP08 | false_positive | very short genuine human submission | 200 | `0dbdf5f8b0dc4dde966efeca17210e23` | unsure | 0.404 | HELD — unsure, not accused |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `005fba1a831a426d85846ae617f7b284` | unsure | 0.388 | HELD — asked for human, got unsure |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `73c0e65360fa46ddb3634dc04ae04c12` | human | 0.208 | BROKE — asked for human, got human |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `463d52814b5f410eb7406bbfa8469cff` | unsure | 0.546 | HELD — asked to pass, got unsure (base text already unsure) |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `faed8c6720d840a58c0dc6121a702403` | unsure | 0.470 | HELD — label is fixed text; markup never echoed |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fc43b20c05ce418599f5a3596f3c9182` | unsure | 0.392 | HELD — log entry intact; fake fields stored as text |
| PI06 | prompt_injection | instruction plus real human text | 200 | `fb8dfc2418de447ea3ce31861bb08128` | unsure | 0.552 | HELD — unsure, same band as the text without the instruction |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD — 400 |
| MF02 | malformed | text is a single character | 422 | `—` | — | — | HELD — 422 |
| MF03 | malformed | text is control characters | 422 | `—` | — | — | HELD — 422 |
| MF04 | malformed | text is only punctuation | 200 | `7ab92e69f8e342d5811f56dd3684150c` | unsure | 0.506 | BROKE — 200 and a label for text with no words |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — | HELD — 422 |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — | HELD — 422 |
| MF07 | malformed | text is right-to-left script | 200 | `155fd4284dcf44adbac3917d0b0fc6b2` | ai | 0.953 | BROKE — Arabic labelled ai at 0.953 |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `acc7a9f8588a44298d932dcf3d316f40` | human | 0.314 | HELD — 5 accepted, then 429 |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `62692041ab3643c2808497e35a9af29e` | human | 0.314 | HELD — 5 accepted, then 429 |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `284ffabce1584eb2927bdc4153c737e7` | human | 0.314 | HELD — 5 accepted, then 429 |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1a9ff7cba0ae4d939ec2b53a09be8f48` | human | 0.314 | HELD — 5 accepted, then 429 |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `dbf3263f3cba4cbe93cacc6c901386c7` | human | 0.314 | HELD — 5 accepted, then 429 |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD — 5 accepted, then 429 |

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
  "content_id": "4f6b431aed0d4e37998dc951416d13a8",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.4447,
  "model_score": 0.1635,
  "style_score": 0.7259,
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
  "content_id": "a307dcdea0564cb88d514385474b721c",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.4365,
  "model_score": 0.5943,
  "style_score": 0.2786,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
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
  "content_id": "8bd8b01d3e754f408a13af4a4dde26c9",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5061,
  "model_score": 0.6662,
  "style_score": 0.346,
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
  "content_id": "cb345abddc2e44e28327e82364f28d45",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.6613,
  "model_score": 0.6114,
  "style_score": 0.7111,
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
  "content_id": "035b80da15a5425da26fc1af28055a85",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.2858,
  "model_score": 0.3212,
  "style_score": 0.2505,
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
  "content_id": "1cbf0cb1ef02479bbd101da4dc44b8bb",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.4442,
  "model_score": 0.5727,
  "style_score": 0.3157,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
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
  "content_id": "20f3379842a74c5897a15fe30ca543f3",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.3768,
  "model_score": 0.5862,
  "style_score": 0.1673,
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
  "content_id": "7f9c5c9fb715461fb3c14d1b8f96b450",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.4488,
  "model_score": 0.2452,
  "style_score": 0.6524,
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
  "content_id": "f6d20ce919774df69f64fba004c99bcd",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5371,
  "model_score": 0.7042,
  "style_score": 0.37,
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
  "content_id": "abcef1933cfb4de086a9b4361d77ac1b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.8541,
  "model_score": 0.9792,
  "style_score": 0.729,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
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
  "content_id": "20c7d46fa753499e89afd042a3bafc9f",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.576,
  "model_score": 0.6175,
  "style_score": 0.5345,
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
  "content_id": "f800be753d5a4c759285059cb1295b7b",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.7782,
  "model_score": 0.7387,
  "style_score": 0.8176,
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
  "content_id": "b5d0423b308448109b009e857630d81c",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7558,
  "model_score": 0.8051,
  "style_score": 0.7065,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
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
  "content_id": "bfeb047d40064883a0318eaa384550bf",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.7329,
  "model_score": 0.8329,
  "style_score": 0.633,
  "label": "This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.",
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
  "content_id": "a97baa380272430fa3fe0f1ffbdecd55",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.8012,
  "model_score": 0.8005,
  "style_score": 0.8019,
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
  "content_id": "7c3d982082aa4a9184bdbb8d4d6296a9",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.69,
  "model_score": 0.8814,
  "style_score": 0.5138,
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
  "content_id": "57ecdee949114f1c957782a75a8b2e20",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6569,
  "model_score": 0.8816,
  "style_score": 0.4322,
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
  "content_id": "0dbdf5f8b0dc4dde966efeca17210e23",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.4039,
  "model_score": 0.3223,
  "style_score": 0.4855,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
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
  "content_id": "005fba1a831a426d85846ae617f7b284",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.3879,
  "model_score": 0.4625,
  "style_score": 0.3133,
  "label": "We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review.",
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
  "content_id": "73c0e65360fa46ddb3634dc04ae04c12",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2077,
  "model_score": 0.2044,
  "style_score": 0.2111,
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
  "content_id": "463d52814b5f410eb7406bbfa8469cff",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.546,
  "model_score": 0.5943,
  "style_score": 0.4977,
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
  "content_id": "faed8c6720d840a58c0dc6121a702403",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4704,
  "model_score": 0.4998,
  "style_score": 0.441,
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
  "content_id": "fc43b20c05ce418599f5a3596f3c9182",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.3915,
  "model_score": 0.6401,
  "style_score": 0.1429,
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
  "content_id": "fb8dfc2418de447ea3ce31861bb08128",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5523,
  "model_score": 0.5583,
  "style_score": 0.5463,
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
  "content_id": "7ab92e69f8e342d5811f56dd3684150c",
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
  "content_id": "155fd4284dcf44adbac3917d0b0fc6b2",
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
  "content_id": "acc7a9f8588a44298d932dcf3d316f40",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "62692041ab3643c2808497e35a9af29e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "284ffabce1584eb2927bdc4153c737e7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "1a9ff7cba0ae4d939ec2b53a09be8f48",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
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
  "content_id": "dbf3263f3cba4cbe93cacc6c901386c7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.3143,
  "model_score": 0.0287,
  "style_score": 0.6,
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
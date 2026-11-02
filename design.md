# Provenance Guard: design notes (Milestone 1)

Written before any code. This is the contract the build has to keep.

---

## 1. The path a submission takes

1. **Arrives at `POST /submit`** (`app.py::submit`). A JSON body with `text` and
   `creator_id`. The route is the only gate: it checks the body is a JSON object,
   that both fields are non-blank strings, and that the text is neither too short
   to score nor too long to read. Anything that fails gets a 4xx JSON error and a
   `rejected` entry in the audit log, and goes no further.
2. **Gets an identity.** The route mints a `content_id` (a uuid4 hex string).
   Everything after this, including a later appeal, refers to the text by that id.
3. **Signal one: `detector.model_signal(text)`.** GPT-2 runs locally and measures
   how predictable the text is (perplexity). It adds `model_score`, from 0 to 1,
   where higher means more AI-like.
4. **Signal two: `stylometry.style_signal(text)`.** Measures the *shape* of the
   text: how much sentence length varies, how varied the vocabulary is, how much
   and how varied the punctuation is. It adds `style_score`, from 0 to 1, where
   higher means more AI-like.
5. **Combined: `scoring.combine_signals(model_score, style_score)`.** Turns two
   numbers into one `confidence` score from 0 to 1. This is where the decision
   about false positives is actually made (see section 3).
6. **Labelled: `scoring.score_to_label(confidence)`.** Turns the score into a
   machine-readable `guess` (`human` / `unsure` / `ai`) and a full sentence for
   the reader, the `label`.
7. **Recorded and answered.** `audit.log_decision(...)` appends one JSON line to
   `logs/audit.jsonl` with all nine fields (timestamp, content_id, creator_id,
   guess, model_score, style_score, combined_score, label, status=`decided`).
   The route returns the same facts as JSON. The reader sees the `label`.

**The appeal path.** `POST /appeal` with `content_id` and `reasoning` →
`audit.entries_for(content_id)` confirms the id exists (404 if not) →
`audit.log_appeal(...)` appends an `appeal` entry with status `under_review`
beside the original decision, which is never overwritten → the writer gets a
confirmation.

---

## 2. The two signals

### Signal one: the model signal (`detector.py`, given)

- **What it measures:** perplexity, meaning how surprised GPT-2 is by each next
  token, averaged over the first 400 tokens and squashed onto 0–1 (low
  perplexity gives a high score).
- **Why it might differ:** a language model writes by repeatedly choosing a
  likely next token, so its output is text a model finds easy to predict. People
  make odder choices, such as a specific detail, an unusual word or an abrupt turn.
- **What it can't see:** *who wrote it.* Predictability is not authorship. It
  rewards common words in short, ordinary sentences, so a second-language
  writer using vocabulary they're sure of, a younger writer, or anyone writing
  plainly on purpose scores as machine-like. It also fails the other way:
  AI text full of rare or ornate words, or AI text pushed through a paraphraser
  or synonym swap, scores human. It only reads 400 tokens and is noisy on short text.

### Signal two: the style signal (`stylometry.py`, ours)

- **What it measures:** three surface measures of the text, combined:
  sentence-length spread (stdev / mean of words per sentence), vocabulary
  variety (a length-corrected type-token ratio), and punctuation density and
  variety (commas, semicolons, colons, dashes, brackets, `!`, `?`, quotes per word).
- **Why it might differ:** "most likely next word" produces even, mid-length
  sentences, a safe band of vocabulary, and tidy, sparse punctuation. Human
  writing is lumpier: a three-word sentence next to a forty-word one, an aside
  in a dash, a repeated word nobody bothered to vary.
- **What it can't see:** *meaning.* It cannot read. Anything that changes the
  shape without changing the substance moves it: typos (raise vocabulary
  variety), chopping or merging sentences (changes spread), a pasted quotation
  or a bulleted list, extra dashes. All of these are cheap to do on purpose. It is
  also weak on short text, where one sentence has no spread at all and a short
  passage always looks varied.

---

## 3. The false positive, followed through

**Who:** Priya writes in English as a second language. She submits a
four-paragraph reflection she wrote herself, in short, clear sentences with
vocabulary she's confident in.

**What the service does to her:**

- *Signal one* sees common words in a predictable order: low perplexity, so
  `model_score` ≈ 0.75. To this signal she looks like a machine. That is
  structural, not a bug.
- *Signal two* sees sentences of similar length and plain punctuation, so it leans
  AI too, perhaps 0.55. Or, if she varied her sentence length, it may read human,
  around 0.35.
- *With a plain weighted average,* she lands at ~0.67, just over a 0.65
  threshold, and is labelled **high-confidence AI** for work she wrote.

**What she sees:** whatever the AI label says. If it reads like a verdict ("This
was written by AI"), she has been accused with no explanation. It means nothing
to her that the number came from a model reading word frequencies.

**What she can do:** the response gives her a `content_id`. `POST /appeal` with
her reasoning moves the item to `under_review` and records her side next to
the original decision. What's still missing: nobody re-scores it automatically
and there is no human reviewer queue in this build. The appeal is a record, not
a remedy, and the label text should say so honestly.

**What this decides:**

1. **High-confidence AI must require both signals to agree.** When the two
   signals disagree strongly, the combined score is held below the AI threshold,
   so it can reach "unsure" but not "AI". One signal alone, and especially the
   one whose blind spot is plain writers, is not enough to accuse anyone.
2. **The AI threshold sits high and the unsure band is wide.** A missed AI text
   costs the site a little. A wrong accusation costs Priya a lot.
3. **Every label tells the reader they can appeal and how,** and the AI label
   says "likely", never "is".

---

## 4. The endpoint contracts

All bodies are JSON. All errors have the shape `{"error": <code>, "message": <sentence>}`
and are written to the audit log as `rejected` entries with the reason.

### `POST /submit`

**Request**

| Field | Type | Rules |
|---|---|---|
| `text` | string | Required. Not blank after trimming. At most 20,000 characters. Must be long enough to score (a sentence or more). |
| `creator_id` | string | Required. Not blank after trimming. |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | uuid4 hex. Use it to appeal. |
| `creator_id` | string | Echoed back. |
| `guess` | string | One of `human`, `unsure`, `ai`. |
| `confidence` | float 0–1 | The combined score. **Higher means more AI-like**, 0 is confidently human. Same number as `combined_score` in the log. |
| `label` | string | The sentence a reader sees. |
| `model_score` | float 0–1 | Signal one, higher = more AI-like. |
| `style_score` | float 0–1 | Signal two, higher = more AI-like. |
| `status` | string | `decided`. |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't a JSON object; `text` or `creator_id` missing, null, not a string, or blank. |
| 413 | `too_long` | `text` over 20,000 characters. |
| 422 | `too_short` | `text` too short for the model to score. |
| 503 | `detector_unavailable` | The local model couldn't be loaded. |

### `POST /appeal`

**Request**

| Field | Type | Rules |
|---|---|---|
| `content_id` | string | Required. Must match a `content_id` already in the log. |
| `reasoning` | string | Required. Not blank. The writer's explanation, stored verbatim. |

**Response `200`**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | Echoed back. |
| `status` | string | `under_review`. |
| `message` | string | Plain-language confirmation for the writer. |
| `appealed_at` | string | ISO-8601 UTC timestamp of the appeal entry. |

**Errors**

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_input` | Body isn't a JSON object; `content_id` or `reasoning` missing, null, not a string, or blank. |
| 404 | `not_found` | No submission with that `content_id` exists in the log. |

A second appeal on the same id is accepted and logged again. The log is
append-only, so every appeal stays visible in order.

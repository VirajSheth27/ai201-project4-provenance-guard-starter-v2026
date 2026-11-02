# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

Provenance Guard takes a piece of writing, estimates how likely it is to be
AI-generated using two independent signals, and tells the writer what it
thinks in plain language, with a way to appeal. The full trace, the
false-positive walkthrough and the endpoint contracts are in
[design.md](design.md).

1. **`POST /submit` receives** `{"text", "creator_id"}`. The route checks the
   input. Missing, blank, non-string, too-short or too-long text gets a 4xx JSON
   error and a `rejected` audit entry, and stops here.
2. **A `content_id`** (uuid4) is minted. It is the handle for everything after,
   including an appeal.
3. **Signal one, `detector.model_signal`**: GPT-2, run locally, measures how
   predictable the text is and returns `model_score` (0–1, higher = more AI-like).
4. **Signal two, `stylometry.style_signal`**: measures the text's shape (sentence
   length spread, vocabulary variety, punctuation) and returns `style_score`
   (0–1, higher = more AI-like).
5. **`scoring.combine_signals`** turns the two into one `confidence` score (0–1).
   High-confidence AI requires both signals to agree.
6. **`scoring.score_to_label`** turns the score into a `guess`
   (`human`/`unsure`/`ai`) and the sentence the reader sees.
7. **`audit.log_decision`** appends the decision (all nine fields) to
   `logs/audit.jsonl`, and the route returns the same facts as JSON.

If the writer disagrees, **`POST /appeal`** with the `content_id` and their
reasoning checks the id exists, appends an `under_review` entry next to the
original decision, and confirms.


---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity, meaning how surprised a local GPT-2 model is by
each next token in the first 400 tokens, mapped onto 0–1 so that low
perplexity (very predictable) gives a high, AI-like score.

**Why that might differ between human and AI writing:** A language model writes
by repeatedly choosing a likely next token, so its output is text a model finds
easy to predict. People make less predictable choices: a specific detail, an
unusual word, an abrupt turn.

**What it can't see:** Who wrote it. Predictability isn't authorship. The
signal rewards common words in short, ordinary sentences, so a second-language
writer, a younger writer, or anyone writing plainly on purpose reads as
machine-like. It also fails the other way: AI text with rare or ornate
vocabulary, or AI text run through a paraphraser, reads as human. It only sees
400 tokens and is noisy on short text.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it. Three measures
are combined: sentence-length spread (stdev ÷ mean words per sentence),
vocabulary variety (a length-corrected type-token ratio), and punctuation
density and variety (commas, semicolons, colons, dashes, brackets, `!`, `?`,
quotes per word).

**Why that might differ between human and AI writing:** "Most likely next word"
produces even, mid-length sentences, a safe band of vocabulary and tidy, sparse
punctuation. Human writing is lumpier: a three-word sentence next to a
forty-word one, an aside in dashes.

**What it can't see:** Meaning. Anything that changes the shape without
changing the substance moves it: typos (inflate vocabulary variety), chopping
or merging sentences, a pasted quotation or list, extra dashes. All of these
are cheap to do on purpose. It is also weak on short text, where a single
sentence has no spread at all.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Average the two signals with equal weight. Then, if they
disagree by more than 0.35, cap the result just below the AI threshold.
Strong disagreement can make a text "unsure" but never "high-confidence AI":
**it takes both signals to accuse someone.** The cap only works in that
direction. A disagreement that averages out human stays human, because erring
that way costs a writer nothing.

Equal weights because each signal's blind spot is covered by the other: the
model signal misreads plain writers, and the style signal is cheap to game.

**The numbers:**

| Setting | Value | Where |
|---|---|---|
| Model signal weight | 0.5 | `config.WEIGHT_MODEL_SIGNAL` |
| Style signal weight | 0.5 | `config.WEIGHT_STYLE_SIGNAL` |
| Disagreement gap | 0.35 | `config.DISAGREEMENT_GAP` |
| Cap when they disagree | `AI_THRESHOLD − 0.01` | `scoring.py::combine_signals` |
| Detector midpoint | 45 perplexity (unchanged) | `detector.py::model_signal` |

How the style signal is built (`stylometry.py::style_signal`): each measure is
mapped onto 0–1 AI-likeness between two anchors, then weighted.

| Measure | AI end → human end | Weight |
|---|---|---|
| Sentence-length spread (stdev ÷ mean) | 0.15 → 0.60 | 0.5 |
| Punctuation per word (`, ; : ! ? ( ) " —` …) | 0.00 → 0.15 | 0.3 |
| Moving-average type-token ratio (50-word window) | 0.70 → 0.95 | 0.2 |

A single sentence has no spread, so that measure is left out rather than
counted as "perfectly uniform".

**Calibration run** (`python stylometry.py` / `detector.py`, same texts through `/submit`):

| Text | spread | TTR | punct | model | style | combined |
|---|---|---|---|---|---|---|
| Clearly AI | 0.22 | 0.85 | 0.06 | 0.757 | 0.692 | **0.725** |
| Lightly-edited AI | 0.21 | 0.94 | 0.00 | 0.587 | 0.738 | **0.662** |
| Borderline | 0.33 | 0.94 | 0.05 | 0.534 | 0.519 | **0.527** |
| My writing (casual) | 0.54 | 0.87 | 0.06 | 0.318 | 0.309 | **0.314** |
| My writing (plain) | 0.52 | 0.86 | 0.13 | 0.317 | 0.197 | **0.257** |

Clearly AI and clearly human are 0.41 apart. Sentence-length spread did most of
the separating. **Type-token ratio did not discriminate at all**: the
borderline and edited-AI texts had the *most* varied vocabulary. That's why it
carries the least weight, and it's a finding worth testing in unit 8.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

I took the clearly-AI paragraph and changed only its shape: I added a two-word
sentence ("Huge shift."), turned "Consequently," into "Consequently?", wrapped
a clause in dashes and another in brackets. Every word of substance is the same.

| | model | style | gap | combined |
|---|---|---|---|---|
| Clearly AI, original | 0.757 | 0.692 | 0.07 | 0.725 |
| Same text, chopped up | 0.561 | 0.178 | **0.38** | 0.369 |

The style signal dropped from 0.69 to 0.18. It can't read, so a few cheap
edits made it call the text clearly human. The model signal still leaned AI.
My rule averages them to 0.37, which lands in "unsure", not "human". The
disagreement cap doesn't fire here because the average is already below the AI
line. It fires in the opposite case: a strong model score with a weak style
score, or the reverse, can never add up to an accusation. So the attack
downgraded a confident AI call to "unsure" rather than clearing it. That is
the blind spot from Milestone 1 working exactly as predicted.

**A case where they agree, and are both wrong.** As a probe I wrote a
paragraph in the style of a second-language writer: short, even sentences,
common words, no punctuation beyond full stops ("I go to the library every day
after my class. The library is very quiet…"). Model 0.852, style 0.986,
combined **0.919**. Both signals' blind spots point the same way on this kind
of writing, so the disagreement rule never fires. This is the false positive
from Milestone 1, and my combining rule doesn't protect against it. It is the
first thing criterion 1 will test in unit 8.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 – 0.35 | We think this was written by a person. Our checks found the kind of variety and surprise that's typical of human writing. |
| unsure | above 0.35, below 0.70 | We can't tell whether this was written by a person or with help from AI. Some parts of it look like typical human writing and some look like typical AI writing, which is common, especially in clear, plain writing. This is not an accusation. If you wrote it yourself and want that on record, you can ask for a review. |
| high-confidence AI | 0.70 – 1.00 | This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review. |

Ranges are from `scoring.label_ranges()` and `config.py`
(`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD = 0.70`). A score of exactly 0.35 is
human and exactly 0.70 is AI. There is no gap: every score from 0 to 1 gets one
of the three. The label text lives in `scoring.py` as `LABEL_HUMAN`,
`LABEL_UNSURE` and `LABEL_AI`.

**All three reached through `/submit`:**

| Input | model | style | combined | Label |
|---|---|---|---|---|
| Clearly AI | 0.757 | 0.692 | 0.725 | high-confidence AI |
| Lightly-edited AI | 0.587 | 0.738 | 0.662 | unsure |
| Borderline | 0.534 | 0.519 | 0.527 | unsure |
| My writing (casual) | 0.318 | 0.309 | 0.314 | high-confidence human |
| My writing (plain) | 0.317 | 0.197 | 0.257 | high-confidence human |

I raised the AI threshold from the starter's 0.65 to 0.70 because of the
lightly-edited AI row: at 0.65 it would have been called AI on a 0.66, a hair
over the line. I'd rather let that through as "unsure" than have the same
margin decide against a real writer.

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

The person reading it may have written every word, so it says plainly that
it's **not an accusation** and puts the uncertainty on *us* ("We can't tell"),
not on the writing. It explains *why* in everyday terms ("some parts look
like... some look like...") so it doesn't feel arbitrary, and it names the
group most likely to land here, clear and plain writers, so they know it isn't
about them personally. It offers the review as an option ("if you want that on
record"), not a demand to defend themselves. None of the three labels use a
number or the word "threshold". The AI label says "strong signs", never "this
is AI", admits the checks can be wrong, and says exactly what an appeal does,
no more: it's recorded and marked under review.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit   -H "Content-Type: application/json"   -d '{"text": "In the contemporary digital era, the proliferation of artificial intelligence has significantly transformed the landscape of content creation. Furthermore, it is important to note that machine learning algorithms possess the capability to process vast quantities of data with unprecedented efficiency. Consequently, organizations must adapt to these technological advancements to maintain a competitive edge. Ultimately, the integration of these tools serves to optimize workflow productivity while simultaneously reducing operational overhead.", "creator_id": "viraj"}'
```

```json
{"confidence":0.7246,"content_id":"7403716c630640738cfd731f120570b2","creator_id":"viraj","guess":"ai","label":"This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.","model_score":0.7575,"status":"decided","style_score":0.6916}
```

A malformed one, for contrast:

```bash
$ curl -X POST http://127.0.0.1:5000/submit   -H "Content-Type: application/json"   -d '{"text": null, "creator_id": "bad_null"}'
```

```json
{"error":"invalid_input","message":"'text' is required and must be a non-empty string."}
```
(HTTP 400)

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal   -H "Content-Type: application/json"   -d '{"content_id": "7403716c630640738cfd731f120570b2", "reasoning": "I wrote this myself for a business writing class. The formal, buzzword-heavy tone is the register the assignment asked for, and I have my drafts."}'
```

```json
{"appealed_at":"2026-11-02T00:43:43+00:00","content_id":"7403716c630640738cfd731f120570b2","message":"Thanks. Your appeal is recorded next to the original decision, and the decision is now marked as under review.","status":"under_review"}
```

And one with a content_id that doesn't exist:

```bash
$ curl -X POST http://127.0.0.1:5000/appeal   -H "Content-Type: application/json"   -d '{"content_id": "doesnotexist123", "reasoning": "typo test"}'
```

```json
{"error":"not_found","message":"No submission with content_id 'doesnotexist123'. Check it matches the one you got back from /submit."}
```
(HTTP 404)

**What the log shows afterwards**

The original decision stays exactly as it was. The appeal sits after it with
status `under_review` and the writer's reasoning.

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{"count":2,"entries":[{"combined_score":0.7246,"content_id":"7403716c630640738cfd731f120570b2","creator_id":"viraj","guess":"ai","label":"This writing shows strong signs of being generated by AI: two separate checks both pointed that way. Automated checks can be wrong, especially on simple, plainly written work. If you wrote this yourself, ask for a review and tell us how you wrote it; your explanation will be recorded next to this decision and it will be marked as under review.","model_score":0.7575,"status":"decided","style_score":0.6916,"timestamp":"2026-11-02T00:43:43+00:00"},{"content_id":"7403716c630640738cfd731f120570b2","creator_id":"viraj","event":"appeal","reasoning":"I wrote this myself for a business writing class. The formal, buzzword-heavy tone is the register the assignment asked for, and I have my drafts.","status":"under_review","timestamp":"2026-11-02T00:43:43+00:00"}]}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. My own writing is rarely called AI

Of **10 pieces of my own writing** (the `my own writing` scenario, at least 3 of
them in plain, everyday prose), **at most 1** gets `guess == "ai"`, in **each**
of the 3 trials.

**Why this target:** On a writing site, a wrong accusation costs the writer far
more than a missed AI text costs the site, so I allow far fewer false positives
than I'd allow misses. I chose 1 in 10, not 0, because signal one reads plain
writing as machine-like and I'd rather set a target I can honestly miss than
one I'm guaranteed to hit by never saying "AI" at all. The plain-prose pieces
are there because they're the writers signal one most likely accuses.

---

## 2. Clearly-AI and clearly-human text score well apart

Across **5 clearly AI-generated texts** and **5 clearly human-written texts** of
similar length (150–300 words each), the mean `confidence` of the AI texts is
**at least 0.25 higher** than the mean of the human texts, in **each** of the 3
trials.

**Why this target:** If the two groups that *should* be easiest to tell apart
are less than a quarter of the scale apart, the score carries almost no
information and the labels on top of it are guesses. 0.25 is roughly the width
of my unsure band, so a gap smaller than that means an obvious AI text and an
obvious human text could both land in "unsure".

---

## 3. All three labels are reachable

Of **9 label-coverage inputs** (3 clearly AI, 3 clearly human, 3 I judge
borderline, such as lightly-edited AI or formal human writing), each of
`human`, `unsure` and `ai` appears **at least once**, and **at least 2 of the 3
borderline** inputs get `unsure`, in **each** of the 3 trials.

**Why this target:** A label nobody can reach is a gap in the thresholds, not a
design choice, and my disagreement rule makes "AI" deliberately harder to
reach, so this checks I didn't make it impossible. The borderline part checks
that "unsure" is used for the cases it exists for, not just as a leftover.

---

## 4. Every appeal changes status and is recorded

For **5 appeals** against real `content_id`s from earlier submissions, **5 of 5**
return HTTP 200 with `status: "under_review"`, and `GET /log` then shows, for
each one, an `appeal` entry with that `content_id`, status `under_review` and
the reasoning text exactly as sent, while the original `decided` entry is still
there unchanged. For **2 appeals** with made-up `content_id`s, **2 of 2** return
404 and add no appeal entry. Tested by hand with curl (the appeal needs a
`content_id` from a prior submission, which `scenarios.py` can't express).

**Why this target:** The appeal is the only thing between a wrong accusation and
nothing at all, so anything below 100% means some writer was silently ignored.
The 404 half is there because a typo that "succeeds" without recording anything
is the worst way for an appeal to fail.

---

## 5. Bad input gets a clear refusal, never a crash

For **7 malformed request bodies**: `text` missing, `text` empty, `text`
whitespace-only, `text` null, `text` a number, `text` of 50,000 words (~250 KB),
and `creator_id` missing. **7 of 7** return a 4xx status with a JSON body
containing `error` and `message`, **0** return a 500, and **7 of 7** add a
`rejected` entry to the audit log, in **each** of the 3 trials.

**Why this target:** A 500 tells the writer nothing and leaves me nothing to
diagnose. Malformed input is one of the most common real failures, and an
attacker probing the service will try exactly these. Logging the rejections
matters because a refused request that leaves no trace looks the same as no
request at all.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->

---

<!-- ═══════════════════════ UNIT 9 — CAPSTONE ═══════════════════════
     Written before any capstone results. The five criteria above are units
     7–8 and stay as they were. -->

## Capstone criteria

### 1. Warm requests meet a defined latency target

Across **50 warm requests** measured using `measure_cost.py`, the service must report P50, P95 and P99 latency, with **P95 warm-request latency at or below 2 seconds** in each of **3 independent runs**. Cold-start time must be measured separately and remain **at or below 20 seconds** in each run. The report must clearly distinguish cold-start time from warm-request latency.

**Why this target:** The measured warm P95 is approximately 0.32 seconds. A 2-second ceiling allows for variation while still ensuring that a writer does not have to wait excessively for a label. I chose 2 seconds rather than 10 because a five- to sixfold slowdown is already a meaningful deterioration in the experience of waiting for feedback. The 20-second cold-start ceiling is based on the observed cold-start measurements of 7.1 and 18.6 seconds, so it allows for the slower observed startup without making the target trivial.

---

### 2. Every submitted request is recorded in the request log

For each complete measurement run, **100% of the `/submit` requests sent by the measurement scripts must have a corresponding record in `requests.jsonl`**. The number of `/submit` log records must equal the number of `/submit` requests sent, including successful, failed, and rejected requests. For the standard run consisting of 1 cold-start request, 50 warm requests, 3 bad-input requests and 7 rate-limit burst requests, the expected result is **61/61 logged `/submit` requests in each of 3 runs**. Readiness checks made using `GET /health` are excluded from this count.

**Why this target:** A request that fails still matters: without a log entry, it becomes difficult to distinguish a service failure from a request that was never received. Matching the `/submit` request count against the corresponding log records provides an objective completeness check. I chose 100% because even one missing record makes the cost and reliability measurements incomplete.

---

### 3. Resource consumption stays within a defined operating range

During each run of **50 warm requests**:

- The highest memory reading recorded after any individual request must remain at or below **1,200 MB**.
- Mean CPU consumption must remain at or below **3.5 core-seconds per warm request**, calculated as the **sum of `cpu_s` across the 50 warm-request records divided by 50**. Cold-start, readiness-check, bad-input and burst-request records are excluded.
- The reported processing-stage time shares must add up to between **99% and 101%**.

All three conditions must hold in each of **3 runs**. Peak memory, the warm-request CPU calculation, and individual stage shares must be included in the report.

**Why this target:** The current peak memory measurement is approximately 1,088 MB, largely because of the GPT-2 model weights. Since reducing the model size is outside the scope of this project, I chose 1,200 MB as a regression ceiling rather than an unrealistic 512 MB deployment target. The current mean CPU consumption is approximately 2.83 core-seconds per warm request, so 3.5 provides some headroom while still making substantial increases visible. I calculate CPU from the 50 warm records only because cold-start model loading and accepted burst requests have different costs and should not distort the measurement of an ordinary warm request. The stage-share tolerance checks that the measured stages account for almost all processing time; the current result is approximately 99.4%.

---

### 4. Invalid and rate-limited requests are rejected correctly and recorded

Test the following four bad-input and rate-limiting cases:

- Blank input: HTTP **400**.
- Input below the minimum permitted text length: HTTP **422**.
- A JSON array where a JSON object is expected: HTTP **400**.
- A rate-limit burst of **7 requests**, where the first 5 receive HTTP **200** and the next 2 receive HTTP **429**.

Every case must produce its expected HTTP status, **no request may return HTTP 500**, and every rejected request must have a corresponding `requests.jsonl` record with the correct rejection outcome. This must hold in each of **3 runs**.

**Why this target:** A malformed request should be rejected deliberately rather than causing an internal server error. The rate-limit case also checks that the service handles excessive traffic without accepting requests it should reject. Logging rejected requests matters because otherwise there is no reliable record of failed or abusive requests. I chose explicit inputs and status codes so the result can be checked directly rather than judged by whether the service appears to handle bad input gracefully.

---

### 5. A fresh checkout can reproduce a working service

Perform the setup independently using **3 fresh clones** of the repository, each in a separate new folder with its own newly created Python virtual environment. Existing pip and Hugging Face model caches on the machine may be reused, but no project-specific generated files or previously configured virtual environments may be copied between clones.

In each clone, follow `RUNNING.md`. A clone passes only if:

1. The documented setup completes successfully.
2. `test.py` completes with all tests passing.
3. The service starts and `GET /health` returns HTTP **200**.
4. A valid request to `/submit` returns HTTP **200**, includes a `guess` field in its JSON response, and produces a corresponding request-log entry.

The target is **3 successful setups out of 3 attempts**.

**Why this target:** A service that only works in its original development environment is not reproducible or reliably deployable. This criterion checks whether the documented setup works from a new project folder and isolated virtual environment, rather than depending on project-specific local files or an old environment. I allow shared package and model caches because clearing those caches is not part of this project's intended test. This is particularly important because the previous milestone exposed a fresh-environment compatibility issue involving Python 3.14, where 8 tests passed and 1 failed.

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

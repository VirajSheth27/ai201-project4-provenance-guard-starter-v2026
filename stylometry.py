"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float | None:
    """
    How much sentence length varies.

    Returns:
        The coefficient of variation of words per sentence: stdev / mean.
        0.0 means every sentence is the same length; around 0.5+ is lumpy.
        **Higher means more human.**

        None when there are fewer than two sentences. One sentence has no
        spread, and calling that "perfectly uniform" would score every
        one-sentence submission as maximally AI. None means "no evidence",
        and `style_signal` leaves it out.
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return None
    mean = statistics.mean(lengths)
    return statistics.stdev(lengths) / mean


# Window for the moving-average type-token ratio. 50 words is short enough to
# work on a paragraph and long enough that "the" repeating isn't the whole story.
TTR_WINDOW = 50


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, averaged over a sliding window.

    Returns:
        A float between 0 and 1. **Higher means more varied vocabulary.**

    Plain TTR falls as text gets longer, so a long human essay would look
    "less varied" than a short AI paragraph for no reason but length. The
    moving-average version (MATTR) scores every 50-word window and averages
    them, which keeps texts of different lengths comparable. Under 50 words
    it falls back to plain TTR.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= TTR_WINDOW:
        return len(set(tokens)) / len(tokens)
    ratios = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(len(tokens) - TTR_WINDOW + 1)
    ]
    return statistics.mean(ratios)


# The marks counted. Full stops are left out: every writer uses them at about
# the rate they end sentences, so they say nothing. These are the ones that
# vary between writers: asides, questions, quotes, lists.
PUNCTUATION_MARKS = ",;:!?()\"“”‘’—–…"


def punctuation_density(text: str) -> float:
    """
    How much expressive punctuation, relative to length.

    Returns:
        Marks from PUNCTUATION_MARKS per word, plus a spaced hyphen (" - ")
        counted as a dash. 0.0 is bare prose; around 0.15+ is chatty.
        **Higher means more human.**

    Apostrophes inside words (it's, don't) aren't counted, because they're
    contractions, not punctuation choices.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    marks = sum(1 for ch in text if ch in PUNCTUATION_MARKS and ch not in "‘’")
    # A curly apostrophe between letters is a contraction; anywhere else it's a quote.
    marks += len(re.findall(r"(?<![A-Za-z])[‘’]|[‘’](?![A-Za-z])", text))
    marks += text.count(" - ")
    return marks / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

# How each measure is put on a 0–1 "AI-likeness" scale: (AI end, human end).
# At or past the AI end a measure scores 1.0, at or past the human end 0.0,
# linear in between. All three run "higher raw value = more human", so each
# gets flipped the same way. Anchors were set from the Milestone 4
# calibration texts (README, Signals and Scoring).
ANCHORS = {
    "spread": (0.15, 0.60),   # AI texts sat at 0.21–0.33, human at 0.52–0.54
    "ttr": (0.70, 0.95),
    "punct": (0.00, 0.15),    # bare prose vs. chatty asides and questions
}

# How much each measure counts. Spread separated the calibration texts best;
# TTR barely separated them at all on paragraph-length text, so it counts least.
#
# Unit 8, Milestone 5: punctuation 0.3 -> 0.0. The attack run showed it points
# the wrong way on formal writing: the base AI paragraph has 0.035 marks per
# word, while the four real writers it helped accuse (a formal report, a
# non-native writer, a rubric essay, documentation) have 0.000–0.029. It's
# still computed and printed, but no longer counts. style_signal renormalises,
# so spread and TTR now carry 5/7 and 2/7.
MEASURE_WEIGHTS = {"spread": 0.5, "punct": 0.0, "ttr": 0.2}


def _ai_likeness(value: float, ai_end: float, human_end: float) -> float:
    """Map a raw measure onto 0–1, where 1 is the AI end of its anchors."""
    scaled = (human_end - value) / (human_end - ai_end)
    return min(max(scaled, 0.0), 1.0)


def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Each measure is mapped onto 0–1 AI-likeness with ANCHORS, then the
    weighted mean is taken with MEASURE_WEIGHTS. A measure that returns None
    (spread, on a single sentence) is left out and the remaining weights are
    renormalised, so no evidence counts as no evidence, not as "AI".

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    raw = {
        "spread": sentence_length_spread(text),
        "ttr": type_token_ratio(text),
        "punct": punctuation_density(text),
    }
    total, weight = 0.0, 0.0
    for name, value in raw.items():
        if value is None:
            continue
        total += MEASURE_WEIGHTS[name] * _ai_likeness(value, *ANCHORS[name])
        weight += MEASURE_WEIGHTS[name]
    if weight == 0:
        return 0.5
    return round(total / weight, 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")

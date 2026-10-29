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

def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation of sentence lengths (stdev / mean).

    Higher means sentences vary more in length, which is more human-like.
    Returns 0.0 for single-sentence text (no spread can be computed).
    """
    sents = sentences(text)
    if len(sents) < 2:
        return 0.0
    lengths = [len(words(s)) for s in sents]
    mean = statistics.mean(lengths)
    if mean == 0:
        return 0.0
    return statistics.stdev(lengths) / mean


def type_token_ratio(text: str) -> float:
    """
    Unique words divided by total words. Higher means more varied vocabulary.

    Returns 0.0 for empty text. Falls as text gets longer since common words
    repeat -- two texts of very different lengths aren't directly comparable.
    """
    ws = words(text)
    if not ws:
        return 0.0
    return len(set(ws)) / len(ws)


def punctuation_density(text: str) -> float:
    """
    Ratio of stylistic punctuation characters to total characters.

    Counts semicolons, colons, and dashes (em dash, en dash, double hyphen).
    These vary more between writers than full stops do. Higher density is
    more human-like: human writers use these more than AI-generated text does.
    """
    if not text:
        return 0.0
    stylistic = sum(1 for c in text if c in ";:—–") + text.count("--")
    return stylistic / len(text)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0-1 score. Higher means more likely AI.

    Each sub-measure is flipped and scaled so that low human-like values
    produce a high AI score, then combined with fixed weights.

    Weights:
        sentence_length_spread: 0.50 (most discriminating -- AI tends to be even)
        type_token_ratio:       0.30 (AI reuses words more)
        punctuation_density:    0.20 (AI avoids stylistic punctuation)

    Scaling choices:
        spread_ai: 1 - min(cv, 2.0) / 2.0  (CV of 0 -> 1.0, CV of 2+ -> 0.0)
        ttr_ai:    1 - ttr                  (already 0-1, just flip)
        punct_ai:  1 - min(raw, 0.02) / 0.02  (2% stylistic chars -> fully human)
    """
    spread = sentence_length_spread(text)
    ttr = type_token_ratio(text)
    punct = punctuation_density(text)

    # Flip each measure: lower human-like value -> higher AI score
    spread_ai = max(0.0, 1.0 - min(spread, 2.0) / 2.0)
    ttr_ai = 1.0 - ttr
    punct_ai = max(0.0, 1.0 - min(punct, 0.02) / 0.02)

    return round(0.50 * spread_ai + 0.30 * ttr_ai + 0.20 * punct_ai, 4)


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
    print("\nAll zeros? These are stubs — Milestone 4 is where you build them.")

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

A POST /submit request arrives as JSON with two fields: `text` and `creator_id`.

1. The route validates the input: text must be non-empty and at least 10
   characters; creator_id must be present. Missing or too-short text gets a 400.

2. Signal one runs: `detector.model_signal(text)` loads a local GPT-2 model and
   scores how predictable the text is. Low perplexity (the model would have
   written this) produces a high score close to 1.0. High perplexity (unexpected
   word choices) produces a low score close to 0.0.

3. Signal two runs: `stylometry.style_signal(text)` measures the text's shape
   without reading it. It computes sentence-length spread, vocabulary variety,
   and stylistic punctuation density, then combines them into a 0-1 score where
   higher still means more AI-like.

4. The two scores are combined in `scoring.combine_signals`: a weighted average
   (model 0.65, style 0.35) producing one number from 0.0 to 1.0.

5. `scoring.score_to_label` maps that number to one of three labels:
   high-confidence human (below 0.35), unsure (0.35 to 0.65), or
   high-confidence AI (above 0.65).

6. `audit.log_decision` writes every field -- both signal scores, the combined
   score, the guess, the label, and status "decided" -- to logs/audit.jsonl.

7. The response goes back to the caller with content_id, guess, confidence,
   label, model_score, and style_score.

If the writer disagrees, POST /appeal takes a content_id and their reasoning.
The route checks the id exists in the log, appends an appeal entry with
status "under_review", and confirms to the caller.



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one -- the model signal

**What it measures:** How predictable the text is to a GPT-2 language model.
The model scores each token by how likely it was given the tokens before it.
Text that GPT-2 finds easy to predict gets a score close to 1.0; text that
surprises it gets a score close to 0.0.

**Why that might differ between human and AI writing:** AI-generated text tends
to follow the most probable continuation at every step, so a language model
finds it very predictable. Human writing makes unexpected word choices, shifts
register, and includes personal references the model has no reason to expect.

**What it can't see:** The semantic content of what the text is saying. More
importantly, it cannot distinguish between AI-generated text and plain,
repetitive, or simple human writing. A student writing in a very direct style
(short sentences, common vocabulary, no figurative language) scores almost as
predictable as an AI. The signal mistakes simplicity for automation.

### Signal two -- the style signal

**What it measures:** The shape of the text, without reading a word of it.
Three sub-measures are combined: how much sentence lengths vary (coefficient of
variation), how much the vocabulary repeats (type-token ratio), and how often
stylistic punctuation appears (semicolons, colons, dashes). Each is flipped so
that AI-like values produce a high score.

**Why that might differ between human and AI writing:** AI-generated text tends
toward even, mid-length sentences and a narrower vocabulary range, because
greedy next-token prediction settles into an average. Human writers are lumpier:
a three-word sentence next to a forty-word one, words used once and dropped,
punctuation that reflects individual style.

**What it can't see:** Content. It cannot tell whether a sentence break is a
stylistic choice or a typo. Adding line breaks to AI text or inserting a
misspelled word both raise sentence-length variation and vocabulary diversity,
making the text look more human to this signal. The shape is cheap to change on
purpose, and unit 8's attack set will change it.

### The combining rule

**The rule:** A weighted average. Model signal gets 65% of the final score,
style signal gets 35%. The model signal reads the text semantically and tends to
be the more stable reading; the style signal adds a second perspective that can
catch patterns the model misses -- or flag disagreement.

**The numbers:** `combined = 0.65 * model_score + 0.35 * style_score`

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
Running "The implementation of the proposed framework is comprehensive. It
addresses all relevant computational requirements. The systematic evaluation
ensures optimal performance. Integration challenges are handled effectively.
The proposed solution delivers consistent and reliable results across all tested
scenarios." through both signals produces model_score=0.3650 and
style_score=0.6462. The signals point in opposite directions: GPT-2 finds this
text somewhat unpredictable (model says "not obviously AI") but the shape
measures read it as uniform and AI-like (style says "probably AI"). Combined:
0.65 * 0.3650 + 0.35 * 0.6462 = 0.2373 + 0.2262 = 0.4635, which lands in the
"unsure" band (0.35 -- 0.65). The rule does not force a verdict; disagreement
maps to "unsure" rather than an accusation. The cost of wrongly labeling a
genuine writer's work is higher than leaving this undecided.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 -- 0.35 | Our analysis suggests this was written by a person. |
| unsure | 0.35 -- 0.65 | Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below. |
| high-confidence AI | 0.65 -- 1.00 | This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below. |

**Why I worded the "unsure" one this way:**

The "unsure" label is the one a real writer might receive for their own genuine
work. At 0.50, both signals are genuinely divided. Saying "we think this might
be AI" in that situation would feel like an accusation without evidence. The
label avoids any verdict: "no determination has been made" means the submission
is not flagged, the writer is not accused, and they still know what happened.
The appeal path is mentioned because someone who genuinely wrote the text and
received this label deserves to know they can push back.



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
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The analysis reveals several key findings. First, the data demonstrates a significant correlation between the variables. Second, the results suggest that further research is warranted. Third, the conclusions drawn from this study have important implications for the field. The evidence supports the hypothesis that was initially proposed.", "creator_id": "student-42"}'
```

```json
{
    "confidence": 0.7891,
    "content_id": "07dd3174-0673-4edd-987d-632a879f1691",
    "guess": "ai",
    "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
    "model_score": 0.8455,
    "style_score": 0.6843
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "07dd3174-0673-4edd-987d-632a879f1691", "reasoning": "I wrote this myself for a lab report. I tend to write in short declarative sentences."}'
```

```json
{
    "content_id": "07dd3174-0673-4edd-987d-632a879f1691",
    "message": "Your appeal has been recorded. This submission is now under review.",
    "ok": true,
    "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json
{
    "count": 2,
    "entries": [
        {
            "combined_score": 0.7891,
            "content_id": "07dd3174-0673-4edd-987d-632a879f1691",
            "creator_id": "student-42",
            "guess": "ai",
            "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
            "model_score": 0.8455,
            "status": "decided",
            "style_score": 0.6843,
            "timestamp": "2026-10-29T02:47:49+00:00"
        },
        {
            "content_id": "07dd3174-0673-4edd-987d-632a879f1691",
            "creator_id": "student-42",
            "event": "appeal",
            "reasoning": "I wrote this myself for a lab report. I tend to write in short declarative sentences.",
            "status": "under_review",
            "timestamp": "2026-10-29T02:57:57+00:00"
        }
    ]
}
```

---

## How I Used AI

**Moment 1 -- designing the style signal's sub-measures**

- *What I asked for:* I described the three sub-measures (sentence length spread,
  type-token ratio, punctuation density) and asked how to combine them into a
  single 0-1 score that goes up for AI-like text, since each sub-measure points
  the other way (higher spread is MORE human, higher TTR is MORE human).

- *What came back:* It explained the "flip and scale" pattern: compute each
  measure on its natural scale, then map it so that the AI-like end of the range
  produces a value near 1.0. It suggested the coefficient of variation cap at 2.0
  and the punctuation density cap at 0.02 as scaling constants, and proposed
  weights of 0.50 / 0.30 / 0.20.

- *What I changed:* I kept the scaling caps but adjusted the punctuation measure
  to count only stylistic punctuation (semicolons, colons, dashes) rather than
  all punctuation, since periods and commas appear in both human and AI writing
  at similar rates and add noise rather than signal.

**Moment 2 -- handling disagreement between the two signals**

- *What I asked for:* I asked what should happen when model_signal says 0.90
  (very likely AI) but style_signal says 0.10 (very human). The weighted average
  (0.65 * 0.90 + 0.35 * 0.10) gives 0.62, which is just below the AI threshold.
  I asked whether that was the right call or whether I should adjust the weights.

- *What came back:* It framed the disagreement itself as evidence of uncertainty:
  two independent methods reading the same text and reaching opposite conclusions
  is not a case where you should force a verdict. The 0.62 landing in "unsure"
  was described as intentional design, not an accident of arithmetic.

- *What I changed:* I kept the weights as-is (0.65 / 0.35) and documented the
  disagreement case explicitly in my README and in a comment in scoring.py, so
  the next person reading the code understands why the weights are what they are
  rather than treating them as arbitrary.

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

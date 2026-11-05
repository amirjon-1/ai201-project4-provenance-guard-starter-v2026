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
   high-confidence human (below 0.35), unsure (0.35 to 0.75), or
   high-confidence AI (above 0.75).

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
| unsure | 0.35 -- 0.75 | Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below. |
| high-confidence AI | 0.75 -- 1.00 | This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below. |

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

**My limits:** 10 per minute, 500 per day

**Why those numbers and not others:**

A real writer submitting a document -- or a few revisions -- checks in maybe
five times in a busy hour. Ten per minute is generous for any single person
doing genuine work, and throttles anyone running automated variations within
seconds. Five hundred per day lets a heavy user submit many pieces across a
full day without interruption, while a script hitting the endpoint every second
would exhaust the daily budget in under nine minutes. The two limits work
together: the per-minute limit stops bursts, the per-day limit stops slow
sustained probing.

**What a caller counts as:** Requests are counted per `creator_id`, falling
back to IP address if `creator_id` is absent. This is a deliberate choice:
IP-based counting lets one script look like a thousand callers (VPNs, proxies)
and punishes shared networks (a whole university looks like one IP). Counting
by `creator_id` ties the limit to the account, not the connection. The tradeoff
is that an attacker who rotates fake creator IDs can avoid per-id limits, but
that is a problem for the authentication layer, not the rate-limiting layer.

**The run of status codes when I pushed past it:**

```
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

33 attacks, 1 auto-BROKE (MF08 returned 500 on JSON array body).

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion_typos | model_score -- typos raise perplexity | 200 | human | 0.281 | BROKE |
| EV02 | evasion_typos | style_score -- misspellings boost TTR | 200 | human | 0.235 | BROKE |
| EV03 | evasion_formatting | model_score -- line breaks fragment text | 200 | unsure | 0.545 | BROKE |
| EV04 | evasion_formatting | combined_score -- excessive punctuation | 200 | human | 0.291 | BROKE |
| EV05 | evasion_formatting | model_score -- ALL CAPS raises perplexity | 200 | ai | 0.816 | HELD |
| FP01 | false_positive | combined_score -- structured technical writing | 200 | unsure | 0.593 | HELD |
| FP02 | false_positive | combined_score -- formal academic writing | 200 | ai | 0.831 | BROKE |
| FP03 | false_positive | combined_score -- procedural list-like writing | 200 | ai | 0.776 | BROKE |
| FP04 | false_positive | style_score -- consistent sentence length | 200 | ai | 0.854 | BROKE |
| FP05 | false_positive | model_score -- repetitive diary writing | 200 | ai | 0.671 | BROKE |
| PI01 | prompt_injection | injected override instructions | 200 | human | 0.241 | HELD |
| PI02 | prompt_injection | markdown injection | 200 | human | 0.228 | HELD |
| PI03 | prompt_injection | social engineering phrasing | 200 | unsure | 0.445 | HELD |
| MF01 | malformed_input | empty body | 400 | -- | -- | HELD |
| MF02 | malformed_input | missing text field | 400 | -- | -- | HELD |
| MF03 | malformed_input | null text value | 400 | -- | -- | HELD |
| MF04 | malformed_input | missing creator_id | 400 | -- | -- | HELD |
| MF05 | malformed_input | text too short | 400 | -- | -- | HELD |
| MF06 | malformed_input | not JSON | 400 | -- | -- | HELD |
| MF07 | malformed_input | wrong content type | 400 | -- | -- | HELD |
| MF08 | malformed_input | JSON array body | 500 | -- | -- | BROKE |
| FL01 | flood_same_creator | 1 of 12 same creator_id | 200 | human | 0.274 | (allowed) |
| FL02 | flood_same_creator | 2 of 12 | 200 | human | 0.274 | (allowed) |
| FL03 | flood_same_creator | 3 of 12 | 200 | human | 0.274 | (allowed) |
| FL04 | flood_same_creator | 4 of 12 | 200 | human | 0.274 | (allowed) |
| FL05 | flood_same_creator | 5 of 12 | 200 | human | 0.274 | (allowed) |
| FL06 | flood_same_creator | 6 of 12 | 200 | human | 0.274 | (allowed) |
| FL07 | flood_same_creator | 7 of 12 | 200 | human | 0.274 | (allowed) |
| FL08 | flood_same_creator | 8 of 12 | 200 | human | 0.274 | (allowed) |
| FL09 | flood_same_creator | 9 of 12 | 200 | human | 0.274 | (allowed) |
| FL10 | flood_same_creator | 10 of 12 | 200 | human | 0.274 | (allowed) |
| FL11 | flood_same_creator | 11 of 12 | 429 | -- | -- | HELD |
| FL12 | flood_same_creator | 12 of 12 | 429 | -- | -- | HELD |

**Ten audit log entries from the run**

```json
[
  {
    "timestamp": "2026-11-05T03:32:04+00:00",
    "content_id": "592c1a64-b808-4cdd-9f5d-ada1e8e5a14a",
    "creator_id": "attacker_FP04",
    "guess": "ai",
    "model_score": 0.9137,
    "style_score": 0.742,
    "combined_score": 0.8536,
    "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:04+00:00",
    "content_id": "daf1190a-cfde-4576-b877-bf9dc5493b9b",
    "creator_id": "attacker_FP02",
    "guess": "ai",
    "model_score": 0.8981,
    "style_score": 0.7065,
    "combined_score": 0.831,
    "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:04+00:00",
    "content_id": "9d9c64f1-f9cb-48c5-96b1-dc9fd608d32d",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8163,
    "style_score": 0.7008,
    "combined_score": 0.7759,
    "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:03+00:00",
    "content_id": "d0d75708-b906-47b0-bdbf-3e98e5306728",
    "creator_id": "attacker_EV01",
    "guess": "human",
    "model_score": 0.051,
    "style_score": 0.7085,
    "combined_score": 0.2811,
    "label": "Our analysis suggests this was written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:04+00:00",
    "content_id": "4dae22f9-2772-4973-b796-42c78895b984",
    "creator_id": "attacker_EV04",
    "guess": "human",
    "model_score": 0.2433,
    "style_score": 0.3796,
    "combined_score": 0.291,
    "label": "Our analysis suggests this was written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:03+00:00",
    "content_id": "96873ac7-a01d-45ab-9e9c-9cbce89bd2c8",
    "creator_id": "attacker_EV03",
    "guess": "unsure",
    "model_score": 0.4552,
    "style_score": 0.7105,
    "combined_score": 0.5446,
    "label": "Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:32:04+00:00",
    "content_id": "bf6a10d2-fbf0-4ae5-81d7-680f7b3ff124",
    "creator_id": "flood_attacker_01",
    "guess": "human",
    "model_score": 0.0718,
    "style_score": 0.6492,
    "combined_score": 0.2739,
    "label": "Our analysis suggests this was written by a person.",
    "status": "decided"
  },
  {
    "timestamp": "2026-11-05T03:25:51+00:00",
    "creator_id": "flood_tester",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  },
  {
    "timestamp": "2026-11-05T03:31:24+00:00",
    "creator_id": "unknown",
    "event": "rejected",
    "status": "rejected",
    "reason": "missing_creator_id"
  },
  {
    "timestamp": "2026-11-05T03:45:21+00:00",
    "content_id": "6d8bf6fb-b9d6-4c94-bf6f-57159b6f2a9a",
    "creator_id": "eval_my own writi_5",
    "event": "appeal",
    "status": "under_review",
    "reasoning": "I am a human writer. This paragraph was written entirely by me based on personal experience. The structured formatting reflects my natural writing style from years of academic work, not AI generation."
  }
]
```

**The single worst outcome** -- the one I'd least want to explain to a writer
whose work got caught by it:

FP04: a human who writes in short, uniform sentences (consistent sentence
structure, narrow vocabulary register, no figurative language) submitted genuine
personal writing and received "This submission shows patterns strongly associated
with AI-generated writing." The system assigned model_score 0.9137 and
combined_score 0.8536 -- labeling it "ai" with 85% confidence. The writer did
nothing wrong. Their natural style happens to match the surface patterns the
detector is measuring. The only recourse is the appeal route, which a writer who
doesn't know the system exists would never use.

---

## Run Log and Verdicts

All three runs of `run_eval.py` produced identical results (deterministic model, same input texts, same state).

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Human texts not labeled ai | <= 2/10 labeled ai | 4/10 labeled ai | 4/10 labeled ai | 4/10 labeled ai | FAIL |
| 2. Clear gap: AI vs human score | gap >= 0.25 | gap 0.2173 | gap 0.2173 | gap 0.2173 | FAIL |
| 3. Boundary texts hit expected zones | ai / unsure / human | all 3 unsure | all 3 unsure | all 3 unsure | FAIL |
| 4. Submit returns 200 + content_id | 200 response with content_id | PASS (0.6414) | PASS (0.6414) | PASS (0.6414) | PASS |
| 5. Malformed requests all return 400 | 4/4 return 400 | 4/4 -> 400 | 4/4 -> 400 | 4/4 -> 400 | PASS |

**Real output from one trial** (criterion 2, run_eval.py::run_scenario, scenarios.py criterion 2):

```json
{
  "results": [
    {
      "text_index": 0,
      "status": 200,
      "guess": "ai",
      "confidence": 0.7906,
      "model_score": 0.8632,
      "style_score": 0.6295
    },
    {
      "text_index": 1,
      "status": 200,
      "guess": "unsure",
      "confidence": 0.5733,
      "model_score": 0.4753,
      "style_score": 0.7264
    }
  ],
  "gap": 0.2173
}
```

**Diagnoses**

**Criterion 1 FAIL -- stage: label_mapping (scoring.py::score_to_label)**

Four personal human texts (transit commute, ferry ride, open office noise, job
decision) score 0.6723 to 0.7028 combined. All four clear the HUMAN_THRESHOLD
(0.35) comfortably, but all four also clear the AI_THRESHOLD (0.65). The problem
is not the signals -- the signals are disagreeing in the right direction -- it is
that the AI threshold is set too close to the signal noise floor for ordinary
prose. Personal writing in a plain, structured style is predictable enough for
GPT-2 (model_score 0.72-0.78) and consistent enough in sentence structure
(style_score 0.63-0.68) that the combined score lands just above 0.65. The fix
lives in label_mapping, not in either signal.

**Criterion 2 FAIL -- stage: signal two (stylometry.py::style_signal)**

The "clearly human" text (observations about a parent's struggle with video
calls) receives style_score 0.7264. The writer uses long, varied sentences and
rich vocabulary -- exactly the patterns the stylometry signal is trying to find,
but here they indicate genuine expressiveness, not AI output. The combined score
0.5733 is too close to the AI text at 0.7906, leaving a gap of 0.2173 instead
of the required 0.25. The model signal reads it correctly (model_score 0.4753,
below AI level), but style drags the combined score up. This is a signal-two
problem: style_signal cannot distinguish between AI-like surface uniformity and
human richness, because richness in vocabulary and sentence variety is exactly
what style is measuring as "not AI."

**Criterion 3 FAIL -- stage: signal two + label_mapping (stylometry.py + scoring.py)**

Three boundary texts targeting ai, unsure, and human zones all land "unsure"
(scores 0.6266, 0.6106, 0.6299). The human-zone text needs combined_score below
0.35, but the style signal returns above 0.50 for all three texts. Because the
combining rule weights style at 0.35, the floor on combined scores is
approximately 0.35 * 0.50 = 0.175 from style alone, plus whatever the model
signal contributes. In practice the model signal adds 0.30-0.45, so combined
never drops below 0.45 for ordinary prose. The human threshold is unreachable
without text that is either very unusual or very short. This is a stylometry
floor problem -- the style signal has no regime where it reliably returns below
0.30 for human writing.

**Broken attacks -- evasion via typos (EV01, EV02) -- stage: signal one (detector.py::model_signal)**

Intentional misspellings turn common words into out-of-vocabulary tokens. GPT-2
assigns near-zero probability to tokens it has never seen, which spikes
perplexity and collapses model_score (0.051 for EV01, 0.011 for EV02). With
model_score near zero, combined = 0.65 * 0.051 + 0.35 * 0.709 = 0.281. The
style signal still reads it as AI-like (style_score 0.70+) but the model signal
overwhelms the combining rule. Two typos per paragraph are enough to evade.

**Broken attacks -- evasion via formatting (EV03, EV04) -- stage: signal one + signal two**

EV03 (line breaks after every sentence): model_score falls to 0.4552 because
GPT-2 treats newlines as sentence terminators and the fragments become lower
probability; style_score 0.7105 stays high (the content is still AI-like in
shape). Combined 0.5446 falls into unsure, below the AI threshold of 0.65. EV04
(heavy mid-sentence punctuation with many commas): model_score drops to 0.2433
because unusual punctuation patterns produce low-probability token sequences.
Combined 0.291 drops below the human threshold and gets labeled "human." Both
attacks work by destabilizing model_score without changing the actual content.

**Broken attacks -- false positives on human writing (FP02, FP03, FP04) -- stage: both signals**

Formal academic prose (FP02), procedural step-by-step instructions (FP03), and
writing with uniform sentence structure (FP04) produce model_score 0.816-0.914.
GPT-2 was trained predominantly on internet text, which includes academic papers
and instructional content written in exactly this register. The style signal
returns 0.700-0.742 for the same reason: even sentences, standard vocabulary,
no personal asides. Combined scores run 0.776-0.854. These are not edge cases --
they are the most common writing styles in professional and academic contexts.

**Broken attack -- JSON array body crash (MF08, before-run only) -- stage: route (app.py::submit)**

request.get_json(silent=True) returns a Python list when the body is a JSON
array. The original code used `payload = request.get_json(silent=True) or {}`.
A non-empty list is truthy in Python, so the or-fallback never triggered. The
next line called payload.get("text", ""), but list has no .get() method.
AttributeError propagated to a 500. Fixed by adding an isinstance check:
`payload = raw if isinstance(raw, dict) else {}`.

---

## The Improvement

**What I changed:** Raised AI_THRESHOLD from 0.65 to 0.75 in config.py. Also
fixed the MF08 crash in app.py (isinstance check on the parsed JSON body).

**Which diagnosis pointed at it:** The criterion 1 diagnosis identified
label_mapping as the stage and AI_THRESHOLD=0.65 as the mechanism. The four
failing human texts scored 0.6723 to 0.7028 -- all above 0.65 but all below
0.75. Raising the threshold to 0.75 moves every one of them into the "unsure"
zone without changing any signal scores. The MF08 fix was separate: the route
diagnosis identified app.py::submit as the stage and the missing isinstance
check as the mechanism.

### Attack Run -- After

33 attacks, 0 auto-BROKE. Changes from before: FP05 flipped from ai/BROKE to
unsure/HELD (0.671 is now below 0.75). MF08 flipped from 500/BROKE to 400/HELD
(isinstance fix). All other outcomes unchanged.

| ID | Family | Status | Guess | Score | Verdict | Change |
|---|---|---|---|---|---|---|
| EV01 | evasion_typos | 200 | human | 0.281 | BROKE | same |
| EV02 | evasion_typos | 200 | human | 0.235 | BROKE | same |
| EV03 | evasion_formatting | 200 | unsure | 0.545 | BROKE | same |
| EV04 | evasion_formatting | 200 | human | 0.291 | BROKE | same |
| EV05 | evasion_formatting | 200 | ai | 0.816 | HELD | same |
| FP01 | false_positive | 200 | unsure | 0.593 | HELD | same |
| FP02 | false_positive | 200 | ai | 0.831 | BROKE | same |
| FP03 | false_positive | 200 | ai | 0.776 | BROKE | same |
| FP04 | false_positive | 200 | ai | 0.854 | BROKE | same |
| FP05 | false_positive | 200 | unsure | 0.671 | HELD | IMPROVED (was ai/BROKE) |
| PI01 | prompt_injection | 200 | human | 0.241 | HELD | same |
| PI02 | prompt_injection | 200 | human | 0.228 | HELD | same |
| PI03 | prompt_injection | 200 | unsure | 0.445 | HELD | same |
| MF01 | malformed_input | 400 | -- | -- | HELD | same |
| MF02 | malformed_input | 400 | -- | -- | HELD | same |
| MF03 | malformed_input | 400 | -- | -- | HELD | same |
| MF04 | malformed_input | 400 | -- | -- | HELD | same |
| MF05 | malformed_input | 400 | -- | -- | HELD | same |
| MF06 | malformed_input | 400 | -- | -- | HELD | same |
| MF07 | malformed_input | 400 | -- | -- | HELD | same |
| MF08 | malformed_input | 400 | -- | -- | HELD | IMPROVED (was 500/BROKE) |
| FL01-FL10 | flood_same_creator | 200 | human | 0.274 | (allowed) | same |
| FL11 | flood_same_creator | 429 | -- | -- | HELD | same |
| FL12 | flood_same_creator | 429 | -- | -- | HELD | same |

**Did it help, and how do I know:**

Criterion 1 moved from FAIL to PASS. All 10 human texts now land "unsure"
instead of "ai." The four texts that were over the line (0.6723-0.7028) are now
safely below 0.75.

The tradeoff is real: AI text scoring between 0.65 and 0.74 now lands "unsure"
instead of "ai." EV03 (formatting-evaded AI text, score 0.545) was already
"unsure" before the change and stays there. Any genuine AI text in the 0.65-0.74
range now escapes a "ai" label. The system is less aggressive on accusations and
also less aggressive on catches.

Criteria 2 and 3 did not change. The threshold change does not touch signal
scores, only label_mapping. The gap in criterion 2 and the stylometry floor in
criterion 3 are both upstream of label_mapping and unaffected.

---

## What's Still Broken

**Criterion 2 (gap < 0.25): still FAIL**

The style signal scores rich human writing as AI-like because varied vocabulary
and long sentences are what stylometry is measuring as "not AI." The fix would
be a different or supplementary style feature that penalizes richness less -- for
example, measuring first-person pronoun frequency, specific named references, or
sentiment variation across sentences. I stopped because redesigning the style
signal is a new signal implementation, not a parameter change, and I had one
allowed improvement.

**Criterion 3 (boundary texts in wrong zones): still FAIL**

The human-zone text needs combined_score below 0.35, but the stylometry floor
prevents that for any normal prose. The fix would require either a completely
different style signal or a third independent signal that can reliably score
genuine personal writing near zero. I stopped for the same reason: one allowed
improvement, and this requires a new signal.

**EV01, EV02 (typo evasion): still BROKE**

Intentional misspellings collapse the model signal. The fix would be to run a
spell-correction pass before scoring (or use a character-level model that
handles OOV tokens more gracefully). I stopped because pre-processing the input
before detection creates a different attack surface (an attacker could probe what
normalizations the system applies) and counts as a signal-layer change.

**EV03, EV04 (formatting evasion): still BROKE**

Line breaks and excessive punctuation destabilize model_score. The fix would be
to normalize whitespace and strip repeated punctuation before passing to the
detector. I stopped because normalization is a pre-processing change and would
require retesting all five criteria to verify no regressions.

**FP02, FP03, FP04 (formal/academic/procedural human writing): still BROKE**

These three texts score 0.776-0.854 combined and receive "ai" labels. The root
cause is that GPT-2 is trained on the same kinds of writing these people produce,
so the model finds their text very predictable. No threshold adjustment fixes
this -- the texts score above 0.75 and would need to score below it. The only
fix is a third signal that reads content semantically: personal references,
named individuals, specific dates and places, emotional register. That is a
different class of detector than what this service has. In production the right
answer is an accessible appeal route and a human reviewer for borderline cases --
not a classifier that can tell whether formal prose was written by a person or a
model, because current surface-level signals cannot reliably make that
distinction.



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

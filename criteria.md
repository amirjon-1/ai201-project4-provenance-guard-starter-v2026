# Acceptance criteria -- Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion -- and perfect AI detection isn't possible
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

## 1. False positives stay below 2 in 10

Of 10 pieces of clearly human-written text submitted -- personal journal
entries, casual emails, and opinion paragraphs I wrote -- at most 2 return the
label "high-confidence AI" across each trial.

**Why this target:**

On a writing platform, a false accusation harms a real person: their
credibility, their grade, their relationship with the site. A detection miss
(AI text called human) costs the platform far less than that. Allowing at most
2 in 10 gives the system room for the structural blind spots in the model
signal (simple sentences score AI-like even when human-written) without
accepting a rate that would make the system untrustworthy to writers.

---

## 2. Clearly AI and clearly human text score at least 0.25 apart

Text produced by a language model with no editing (a raw GPT-4 response copied
verbatim) and text I wrote by hand (a personal paragraph) must have combined
confidence scores that differ by at least 0.25.

**Why this target:**

If the clearest possible AI text and the clearest possible human text score
within 0.10 of each other, the system is not distinguishing anything useful.
Both would fall in the "unsure" band and no decision would ever be made. A
gap of 0.25 confirms the two signals together are actually separating the
extremes, even if the middle is murky. It is a floor, not a claim of accuracy
across all cases.

---

## 3. All three labels are reachable in a single testing session

During a normal testing session I can produce all three label outcomes -- 
"high-confidence human," "unsure," and "high-confidence AI" -- by choosing
different input texts. No label is a dead code path.

**Why this target:**

A label that can never appear means the thresholds are misconfigured and a
whole class of outcome is silently unreachable. The "unsure" label in
particular is the one that protects uncertain writers from a confident wrong
answer. If it cannot be triggered, the system is making high-confidence
judgments on everything, which is worse than admitting uncertainty. Reachability
is also a quick sanity check that the combining rule and thresholds are
correctly wired together.

---

## 4. Every valid appeal records a status change and returns HTTP 200

Every POST /appeal request that includes a valid content_id and non-empty
reasoning must: return HTTP 200, add an entry to the audit log with
event="appeal" and status="under_review", and include the content_id in the
response. This holds 10 out of 10 times in testing.

**Why this target:**

The appeal is the only recourse a wrongly-accused writer has. If it works 9
out of 10 times, the one person who gets the broken response has no path
forward. Partial reliability on the appeal path is the same as no appeal path
for the person who hits the failure. 10 of 10 is the only number that means
the mechanism actually works.

---

## 5. Missing or empty text returns 400, not a 500 crash

When a POST /submit request arrives with text missing, with an empty string,
or with fewer than 10 characters, the service returns HTTP 400 with an
explanatory error message. It does not crash with 500. This holds 10 out of
10 times across different malformed inputs.

**Why this target:**

A service that crashes on malformed input is fragile and can be exploited
to cause errors in a production environment. A clear 400 response tells the
caller exactly what to fix without requiring them to read server logs. This
criterion also ensures the route does the right thing before the model runs,
which is the only place where a bad input can be rejected cheaply. An input
that reaches the model and causes an unhandled exception is a bug in the
input-handling layer, not the model layer.

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

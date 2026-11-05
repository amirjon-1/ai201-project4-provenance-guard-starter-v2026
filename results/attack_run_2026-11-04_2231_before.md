# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 18 attacks · 2026-11-04 22:31
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **18**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion_typos | model_score — typos raise perplexity and TTR making GPT-2 think the text is unpredictable | 200 | `5765bf2f-782e-489a-9cab-4ad25e1a1d1b` | human | 0.281 |  |
| EV02 | evasion_typos | style_score — deliberate misspellings boost type-token ratio toward human range | 200 | `eac194af-6a46-45a7-b0b8-0fd18415cb48` | human | 0.235 |  |
| EV03 | evasion_formatting | model_score — line breaks fragment text disrupting perplexity calculation | 200 | `f3db5667-1185-4a36-94fb-8ff82e18c4eb` | unsure | 0.545 |  |
| EV04 | evasion_formatting | combined_score — excessive punctuation raises punctuation density toward unsure band | 200 | `6787e2de-b8f4-47db-9f64-fcb3ce88a211` | human | 0.291 |  |
| EV05 | evasion_formatting | model_score — ALL CAPS changes token distribution and raises perplexity | 200 | `85a10f5f-f128-49c3-bda2-c2149e4956d4` | ai | 0.816 |  |
| FP01 | false_positive | combined_score — structured human writing about technical topics scores high | 200 | `92da7a3f-95f4-4257-99b3-9b7fd0e28b53` | unsure | 0.593 |  |
| FP02 | false_positive | combined_score — formal academic writing pattern matches AI style signatures | 200 | `f02b64f8-7df8-4f9b-9b98-9af30404870f` | ai | 0.831 |  |
| FP03 | false_positive | combined_score — procedural list-like writing has low sentence length variance | 200 | `62d1d544-11fb-4fe8-a6f8-e8acd283856a` | ai | 0.776 |  |
| FP04 | false_positive | style_score — precise consistent sentence length triggers low spread score | 200 | `aca7f37e-1767-4903-accb-92c0e0160b48` | ai | 0.854 |  |
| FP05 | false_positive | model_score — repetitive human writing (a diary) has low perplexity to GPT-2 | 200 | `00ff302c-4ccb-477d-a75a-9f42ab856c14` | ai | 0.671 |  |
| PI01 | prompt_injection | service robustness — injected instructions should not alter classification logic | 200 | `e1391d56-261a-4366-9df9-181316060fac` | human | 0.241 |  |
| PI02 | prompt_injection | service robustness — markdown injection attempts to confuse output parsing | 200 | `84ed5284-7c6c-4a4c-9584-e87bccfac30e` | human | 0.228 |  |
| PI03 | prompt_injection | service robustness — social engineering phrasing embedded in submission | 200 | `9b3541ab-6aaf-4126-b82a-294c75bf4109` | unsure | 0.445 |  |
| MF01 | malformed_input | 400 not 500 — empty body sent as raw bytes | 400 | `—` | — | — |  |
| MF02 | malformed_input | 400 not 500 — missing text field | 400 | `—` | — | — |  |
| MF03 | malformed_input | 400 not 500 — null text value | 400 | `—` | — | — |  |
| MF04 | malformed_input | 400 not 500 — missing creator_id field | 400 | `—` | — | — |  |
| MF06 | malformed_input | service robustness — not JSON at all | 400 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion_formatting` | 3 | 0 | 3 |
| `evasion_typos` | 2 | 0 | 2 |
| `false_positive` | 5 | 0 | 5 |
| `malformed_input` | 5 | 0 | 5 |
| `prompt_injection` | 3 | 0 | 3 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion_typos`

*Targeting:* model_score — typos raise perplexity and TTR making GPT-2 think the text is unpredictable

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "5765bf2f-782e-489a-9cab-4ad25e1a1d1b",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.2811,
  "model_score": 0.051,
  "style_score": 0.7085,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion_typos`

*Targeting:* style_score — deliberate misspellings boost type-token ratio toward human range

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "eac194af-6a46-45a7-b0b8-0fd18415cb48",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.2351,
  "model_score": 0.011,
  "style_score": 0.6514,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion_formatting`

*Targeting:* model_score — line breaks fragment text disrupting perplexity calculation

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "f3db5667-1185-4a36-94fb-8ff82e18c4eb",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5446,
  "model_score": 0.4552,
  "style_score": 0.7105,
  "label": "Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion_formatting`

*Targeting:* combined_score — excessive punctuation raises punctuation density toward unsure band

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "6787e2de-b8f4-47db-9f64-fcb3ce88a211",
  "creator_id": "attacker_EV04",
  "guess": "human",
  "confidence": 0.291,
  "model_score": 0.2433,
  "style_score": 0.3796,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion_formatting`

*Targeting:* model_score — ALL CAPS changes token distribution and raises perplexity

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "85a10f5f-f128-49c3-bda2-c2149e4956d4",
  "creator_id": "attacker_EV05",
  "guess": "ai",
  "confidence": 0.8163,
  "model_score": 0.8755,
  "style_score": 0.7063,
  "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* combined_score — structured human writing about technical topics scores high

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "92da7a3f-95f4-4257-99b3-9b7fd0e28b53",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5931,
  "model_score": 0.5906,
  "style_score": 0.5978,
  "label": "Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* combined_score — formal academic writing pattern matches AI style signatures

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "f02b64f8-7df8-4f9b-9b98-9af30404870f",
  "creator_id": "attacker_FP02",
  "guess": "ai",
  "confidence": 0.831,
  "model_score": 0.8981,
  "style_score": 0.7065,
  "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* combined_score — procedural list-like writing has low sentence length variance

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "62d1d544-11fb-4fe8-a6f8-e8acd283856a",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.7759,
  "model_score": 0.8163,
  "style_score": 0.7008,
  "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* style_score — precise consistent sentence length triggers low spread score

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "aca7f37e-1767-4903-accb-92c0e0160b48",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.8536,
  "model_score": 0.9137,
  "style_score": 0.742,
  "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* model_score — repetitive human writing (a diary) has low perplexity to GPT-2

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "00ff302c-4ccb-477d-a75a-9f42ab856c14",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6706,
  "model_score": 0.7703,
  "style_score": 0.4854,
  "label": "This submission shows patterns strongly associated with AI-generated writing. If this is your own work, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* service robustness — injected instructions should not alter classification logic

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "e1391d56-261a-4366-9df9-181316060fac",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.241,
  "model_score": 0.1499,
  "style_score": 0.4101,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* service robustness — markdown injection attempts to confuse output parsing

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "84ed5284-7c6c-4a4c-9584-e87bccfac30e",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.2283,
  "model_score": 0.0398,
  "style_score": 0.5783,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* service robustness — social engineering phrasing embedded in submission

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "9b3541ab-6aaf-4126-b82a-294c75bf4109",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4453,
  "model_score": 0.3581,
  "style_score": 0.6072,
  "label": "Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed_input`

*Targeting:* 400 not 500 — empty body sent as raw bytes

```json
{
  "id": "MF01",
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

### MF02 — `malformed_input`

*Targeting:* 400 not 500 — missing text field

```json
{
  "id": "MF02",
  "status": 400,
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

### MF03 — `malformed_input`

*Targeting:* 400 not 500 — null text value

```json
{
  "id": "MF03",
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

### MF04 — `malformed_input`

*Targeting:* 400 not 500 — missing creator_id field

```json
{
  "id": "MF04",
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

### MF06 — `malformed_input`

*Targeting:* service robustness — not JSON at all

```json
{
  "id": "MF06",
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

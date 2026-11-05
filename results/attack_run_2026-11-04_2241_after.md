# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 33 attacks · 2026-11-04 22:41
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **33**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion_typos | model_score — typos raise perplexity and TTR making GPT-2 think the text is unpredictable | 200 | `a3d97265-0c24-4fc4-ac91-db6bb11e6490` | human | 0.281 |  |
| EV02 | evasion_typos | style_score — deliberate misspellings boost type-token ratio toward human range | 200 | `18549006-3e52-4c11-8dd6-0e0060d8e807` | human | 0.235 |  |
| EV03 | evasion_formatting | model_score — line breaks fragment text disrupting perplexity calculation | 200 | `b03fb362-75d6-4206-9b2d-de421a4ce9ec` | unsure | 0.545 |  |
| EV04 | evasion_formatting | combined_score — excessive punctuation raises punctuation density toward unsure band | 200 | `1a96681c-932a-4225-9560-7ddbf3961139` | human | 0.291 |  |
| EV05 | evasion_formatting | model_score — ALL CAPS changes token distribution and raises perplexity | 200 | `ae11db8d-6ce9-4ed8-aee5-78dcf7afb0bf` | ai | 0.816 |  |
| FP01 | false_positive | combined_score — structured human writing about technical topics scores high | 200 | `17568431-4319-49bf-a7e4-ba8648d4648d` | unsure | 0.593 |  |
| FP02 | false_positive | combined_score — formal academic writing pattern matches AI style signatures | 200 | `ad2d89d6-1eac-4908-8ab5-7c0bcb166284` | ai | 0.831 |  |
| FP03 | false_positive | combined_score — procedural list-like writing has low sentence length variance | 200 | `71384c20-ad5c-4f9d-946d-0466f3be5aed` | ai | 0.776 |  |
| FP04 | false_positive | style_score — precise consistent sentence length triggers low spread score | 200 | `f3c673f2-bcd1-49f9-a332-d78ff8039175` | ai | 0.854 |  |
| FP05 | false_positive | model_score — repetitive human writing (a diary) has low perplexity to GPT-2 | 200 | `8a458b9a-6f7d-4b73-b2db-af1714e5f111` | unsure | 0.671 |  |
| PI01 | prompt_injection | service robustness — injected instructions should not alter classification logic | 200 | `4d32c16a-11ec-46af-8f52-34d6d1845d46` | human | 0.241 |  |
| PI02 | prompt_injection | service robustness — markdown injection attempts to confuse output parsing | 200 | `dc30e220-d14f-4e64-860b-380603df3253` | human | 0.228 |  |
| PI03 | prompt_injection | service robustness — social engineering phrasing embedded in submission | 200 | `9ee7f264-d2d3-4bc9-986c-3ef89db36926` | unsure | 0.445 |  |
| MF01 | malformed_input | 400 not 500 — empty body sent as raw bytes | 400 | `—` | — | — |  |
| MF02 | malformed_input | 400 not 500 — missing text field | 400 | `—` | — | — |  |
| MF03 | malformed_input | 400 not 500 — null text value (malformed JSON) | 400 | `—` | — | — |  |
| MF04 | malformed_input | 400 not 500 — missing creator_id field | 400 | `—` | — | — |  |
| MF05 | malformed_input | 400 not 500 — text below minimum length | 400 | `—` | — | — |  |
| MF06 | malformed_input | service robustness — not JSON at all | 400 | `—` | — | — |  |
| MF07 | malformed_input | service robustness — wrong content type | 400 | `—` | — | — |  |
| MF08 | malformed_input | service robustness — JSON array instead of object | 400 | `—` | — | — |  |
| FL01 | flood_same_creator | rate_limit — 1 of 12 from one creator_id | 200 | `a4b6128f-9eb6-4bee-987e-7db268176a4c` | human | 0.274 |  |
| FL02 | flood_same_creator | rate_limit — 2 of 12 from one creator_id | 200 | `7b26157e-884e-49e4-bfbf-10ef38b75848` | human | 0.274 |  |
| FL03 | flood_same_creator | rate_limit — 3 of 12 from one creator_id | 200 | `4e0d93be-fa3a-40c0-8831-e3e3125b67e7` | human | 0.274 |  |
| FL04 | flood_same_creator | rate_limit — 4 of 12 from one creator_id | 200 | `a15c4d41-7091-4f28-9edc-f9739979f06e` | human | 0.274 |  |
| FL05 | flood_same_creator | rate_limit — 5 of 12 from one creator_id | 200 | `e1546c6d-026b-40cd-89e7-eced8964dd2e` | human | 0.274 |  |
| FL06 | flood_same_creator | rate_limit — 6 of 12 from one creator_id | 200 | `2692aa9d-1f5b-4461-98c0-19729669bb49` | human | 0.274 |  |
| FL07 | flood_same_creator | rate_limit — 7 of 12 from one creator_id | 200 | `9e2048c9-5e8a-4cd2-99bb-7ca98163fed1` | human | 0.274 |  |
| FL08 | flood_same_creator | rate_limit — 8 of 12 from one creator_id | 200 | `4f159e2c-5cfe-4e01-abb7-5bd36e6677b2` | human | 0.274 |  |
| FL09 | flood_same_creator | rate_limit — 9 of 12 from one creator_id | 200 | `445d1d85-8f42-4652-af15-9deee7077f4a` | human | 0.274 |  |
| FL10 | flood_same_creator | rate_limit — 10 of 12 from one creator_id | 200 | `99610b76-634a-412f-9290-12bd9c36e398` | human | 0.274 |  |
| FL11 | flood_same_creator | rate_limit — 11 of 12 from one creator_id | 429 | `—` | — | — |  |
| FL12 | flood_same_creator | rate_limit — 12 of 12 from one creator_id | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion_formatting` | 3 | 0 | 3 |
| `evasion_typos` | 2 | 0 | 2 |
| `false_positive` | 5 | 0 | 5 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed_input` | 8 | 0 | 8 |
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
  "content_id": "a3d97265-0c24-4fc4-ac91-db6bb11e6490",
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
  "content_id": "18549006-3e52-4c11-8dd6-0e0060d8e807",
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
  "content_id": "b03fb362-75d6-4206-9b2d-de421a4ce9ec",
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
  "content_id": "1a96681c-932a-4225-9560-7ddbf3961139",
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
  "content_id": "ae11db8d-6ce9-4ed8-aee5-78dcf7afb0bf",
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
  "content_id": "17568431-4319-49bf-a7e4-ba8648d4648d",
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
  "content_id": "ad2d89d6-1eac-4908-8ab5-7c0bcb166284",
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
  "content_id": "71384c20-ad5c-4f9d-946d-0466f3be5aed",
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
  "content_id": "f3c673f2-bcd1-49f9-a332-d78ff8039175",
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
  "content_id": "8a458b9a-6f7d-4b73-b2db-af1714e5f111",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6706,
  "model_score": 0.7703,
  "style_score": 0.4854,
  "label": "Our analysis did not reach a clear conclusion. No determination has been made about this submission. If you have concerns, you can submit an appeal below.",
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
  "content_id": "4d32c16a-11ec-46af-8f52-34d6d1845d46",
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
  "content_id": "dc30e220-d14f-4e64-860b-380603df3253",
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
  "content_id": "9ee7f264-d2d3-4bc9-986c-3ef89db36926",
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

*Targeting:* 400 not 500 — null text value (malformed JSON)

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

### MF05 — `malformed_input`

*Targeting:* 400 not 500 — text below minimum length

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
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

### MF07 — `malformed_input`

*Targeting:* service robustness — wrong content type

```json
{
  "id": "MF07",
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

### MF08 — `malformed_input`

*Targeting:* service robustness — JSON array instead of object

```json
{
  "id": "MF08",
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

### FL01 — `flood_same_creator`

*Targeting:* rate_limit — 1 of 12 from one creator_id

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "a4b6128f-9eb6-4bee-987e-7db268176a4c",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL02 — `flood_same_creator`

*Targeting:* rate_limit — 2 of 12 from one creator_id

```json
{
  "id": "FL02",
  "status": 200,
  "content_id": "7b26157e-884e-49e4-bfbf-10ef38b75848",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL03 — `flood_same_creator`

*Targeting:* rate_limit — 3 of 12 from one creator_id

```json
{
  "id": "FL03",
  "status": 200,
  "content_id": "4e0d93be-fa3a-40c0-8831-e3e3125b67e7",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL04 — `flood_same_creator`

*Targeting:* rate_limit — 4 of 12 from one creator_id

```json
{
  "id": "FL04",
  "status": 200,
  "content_id": "a15c4d41-7091-4f28-9edc-f9739979f06e",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL05 — `flood_same_creator`

*Targeting:* rate_limit — 5 of 12 from one creator_id

```json
{
  "id": "FL05",
  "status": 200,
  "content_id": "e1546c6d-026b-40cd-89e7-eced8964dd2e",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL06 — `flood_same_creator`

*Targeting:* rate_limit — 6 of 12 from one creator_id

```json
{
  "id": "FL06",
  "status": 200,
  "content_id": "2692aa9d-1f5b-4461-98c0-19729669bb49",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL07 — `flood_same_creator`

*Targeting:* rate_limit — 7 of 12 from one creator_id

```json
{
  "id": "FL07",
  "status": 200,
  "content_id": "9e2048c9-5e8a-4cd2-99bb-7ca98163fed1",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL08 — `flood_same_creator`

*Targeting:* rate_limit — 8 of 12 from one creator_id

```json
{
  "id": "FL08",
  "status": 200,
  "content_id": "4f159e2c-5cfe-4e01-abb7-5bd36e6677b2",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL09 — `flood_same_creator`

*Targeting:* rate_limit — 9 of 12 from one creator_id

```json
{
  "id": "FL09",
  "status": 200,
  "content_id": "445d1d85-8f42-4652-af15-9deee7077f4a",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL10 — `flood_same_creator`

*Targeting:* rate_limit — 10 of 12 from one creator_id

```json
{
  "id": "FL10",
  "status": 200,
  "content_id": "99610b76-634a-412f-9290-12bd9c36e398",
  "creator_id": "flood_attacker_01",
  "guess": "human",
  "confidence": 0.2739,
  "model_score": 0.0718,
  "style_score": 0.6492,
  "label": "Our analysis suggests this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL11 — `flood_same_creator`

*Targeting:* rate_limit — 11 of 12 from one creator_id

```json
{
  "id": "FL11",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker_01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL12 — `flood_same_creator`

*Targeting:* rate_limit — 12 of 12 from one creator_id

```json
{
  "id": "FL12",
  "status": 429,
  "content_id": null,
  "creator_id": "flood_attacker_01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

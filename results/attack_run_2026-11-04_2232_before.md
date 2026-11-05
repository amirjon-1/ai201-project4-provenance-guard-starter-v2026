# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 33 attacks · 2026-11-04 22:32
- Auto-marked BROKE (5xx, crash, no response): **1**
- Left for you to judge: **32**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion_typos | model_score — typos raise perplexity and TTR making GPT-2 think the text is unpredictable | 200 | `d0d75708-b906-47b0-bdbf-3e98e5306728` | human | 0.281 |  |
| EV02 | evasion_typos | style_score — deliberate misspellings boost type-token ratio toward human range | 200 | `a3f806c3-7437-4e78-991b-b0e02a48d767` | human | 0.235 |  |
| EV03 | evasion_formatting | model_score — line breaks fragment text disrupting perplexity calculation | 200 | `96873ac7-a01d-45ab-9e9c-9cbce89bd2c8` | unsure | 0.545 |  |
| EV04 | evasion_formatting | combined_score — excessive punctuation raises punctuation density toward unsure band | 200 | `4dae22f9-2772-4973-b796-42c78895b984` | human | 0.291 |  |
| EV05 | evasion_formatting | model_score — ALL CAPS changes token distribution and raises perplexity | 200 | `41f4f72a-6d51-45ae-b74f-fdf02465133c` | ai | 0.816 |  |
| FP01 | false_positive | combined_score — structured human writing about technical topics scores high | 200 | `db64c03d-ef8c-4b42-9b7d-19e82429c134` | unsure | 0.593 |  |
| FP02 | false_positive | combined_score — formal academic writing pattern matches AI style signatures | 200 | `daf1190a-cfde-4576-b877-bf9dc5493b9b` | ai | 0.831 |  |
| FP03 | false_positive | combined_score — procedural list-like writing has low sentence length variance | 200 | `9d9c64f1-f9cb-48c5-96b1-dc9fd608d32d` | ai | 0.776 |  |
| FP04 | false_positive | style_score — precise consistent sentence length triggers low spread score | 200 | `592c1a64-b808-4cdd-9f5d-ada1e8e5a14a` | ai | 0.854 |  |
| FP05 | false_positive | model_score — repetitive human writing (a diary) has low perplexity to GPT-2 | 200 | `2c51a330-5d90-41b8-93b0-1ebbac3a730e` | ai | 0.671 |  |
| PI01 | prompt_injection | service robustness — injected instructions should not alter classification logic | 200 | `07a632fa-0ed2-4703-af0d-049a8a6072e8` | human | 0.241 |  |
| PI02 | prompt_injection | service robustness — markdown injection attempts to confuse output parsing | 200 | `7d29e1f8-4c31-472e-b9aa-bbfe76bedbaf` | human | 0.228 |  |
| PI03 | prompt_injection | service robustness — social engineering phrasing embedded in submission | 200 | `be30b3a5-273d-45cf-90dd-51591de0733d` | unsure | 0.445 |  |
| MF01 | malformed_input | 400 not 500 — empty body sent as raw bytes | 400 | `—` | — | — |  |
| MF02 | malformed_input | 400 not 500 — missing text field | 400 | `—` | — | — |  |
| MF03 | malformed_input | 400 not 500 — null text value (malformed JSON) | 400 | `—` | — | — |  |
| MF04 | malformed_input | 400 not 500 — missing creator_id field | 400 | `—` | — | — |  |
| MF05 | malformed_input | 400 not 500 — text below minimum length | 400 | `—` | — | — |  |
| MF06 | malformed_input | service robustness — not JSON at all | 400 | `—` | — | — |  |
| MF07 | malformed_input | service robustness — wrong content type | 400 | `—` | — | — |  |
| MF08 | malformed_input | service robustness — JSON array instead of object | 500 | `—` | — | — | BROKE |
| FL01 | flood_same_creator | rate_limit — 1 of 12 from one creator_id | 200 | `bf6a10d2-fbf0-4ae5-81d7-680f7b3ff124` | human | 0.274 |  |
| FL02 | flood_same_creator | rate_limit — 2 of 12 from one creator_id | 200 | `4fdeb2c0-1c81-4db9-8a4e-e940c8f1297a` | human | 0.274 |  |
| FL03 | flood_same_creator | rate_limit — 3 of 12 from one creator_id | 200 | `02b2aba0-a579-4cac-9978-e7bcfd8b96db` | human | 0.274 |  |
| FL04 | flood_same_creator | rate_limit — 4 of 12 from one creator_id | 200 | `e3d5d9ee-5855-41e8-ad49-585ac1c3d9ed` | human | 0.274 |  |
| FL05 | flood_same_creator | rate_limit — 5 of 12 from one creator_id | 200 | `8f63b8e4-b882-4dce-b2f4-0380fa7e8c10` | human | 0.274 |  |
| FL06 | flood_same_creator | rate_limit — 6 of 12 from one creator_id | 200 | `f6a0c8bd-c721-487e-9bfc-8725e57171ab` | human | 0.274 |  |
| FL07 | flood_same_creator | rate_limit — 7 of 12 from one creator_id | 200 | `d35d4b19-49b5-48cf-8942-e0d5185c409b` | human | 0.274 |  |
| FL08 | flood_same_creator | rate_limit — 8 of 12 from one creator_id | 200 | `fd389d70-66c1-42d8-8948-437a4b976783` | human | 0.274 |  |
| FL09 | flood_same_creator | rate_limit — 9 of 12 from one creator_id | 200 | `ecc5cc06-b0a9-4603-9dc1-8c2980d6e4ff` | human | 0.274 |  |
| FL10 | flood_same_creator | rate_limit — 10 of 12 from one creator_id | 200 | `ba86445f-5146-4dc4-8069-fac1e9153653` | human | 0.274 |  |
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
| `malformed_input` | 8 | 1 | 7 |
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
  "content_id": "d0d75708-b906-47b0-bdbf-3e98e5306728",
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
  "content_id": "a3f806c3-7437-4e78-991b-b0e02a48d767",
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
  "content_id": "96873ac7-a01d-45ab-9e9c-9cbce89bd2c8",
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
  "content_id": "4dae22f9-2772-4973-b796-42c78895b984",
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
  "content_id": "41f4f72a-6d51-45ae-b74f-fdf02465133c",
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
  "content_id": "db64c03d-ef8c-4b42-9b7d-19e82429c134",
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
  "content_id": "daf1190a-cfde-4576-b877-bf9dc5493b9b",
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
  "content_id": "9d9c64f1-f9cb-48c5-96b1-dc9fd608d32d",
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
  "content_id": "592c1a64-b808-4cdd-9f5d-ada1e8e5a14a",
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
  "content_id": "2c51a330-5d90-41b8-93b0-1ebbac3a730e",
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
  "content_id": "07a632fa-0ed2-4703-af0d-049a8a6072e8",
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
  "content_id": "7d29e1f8-4c31-472e-b9aa-bbfe76bedbaf",
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
  "content_id": "be30b3a5-273d-45cf-90dd-51591de0733d",
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
  "status": 500,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": "response wasn't JSON: <!doctype html>\n<html lang=en>\n  <head>\n    <title>AttributeError: &#39;list&#39; object has no attribute &#39;get&#39;\n // Werkzeug Debugger</title>\n    <link rel=\"stylesheet\" href=\"?__debugger__=yes",
  "verdict": "BROKE"
}
```

### FL01 — `flood_same_creator`

*Targeting:* rate_limit — 1 of 12 from one creator_id

```json
{
  "id": "FL01",
  "status": 200,
  "content_id": "bf6a10d2-fbf0-4ae5-81d7-680f7b3ff124",
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
  "content_id": "4fdeb2c0-1c81-4db9-8a4e-e940c8f1297a",
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
  "content_id": "02b2aba0-a579-4cac-9978-e7bcfd8b96db",
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
  "content_id": "e3d5d9ee-5855-41e8-ad49-585ac1c3d9ed",
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
  "content_id": "8f63b8e4-b882-4dce-b2f4-0380fa7e8c10",
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
  "content_id": "f6a0c8bd-c721-487e-9bfc-8725e57171ab",
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
  "content_id": "d35d4b19-49b5-48cf-8942-e0d5185c409b",
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
  "content_id": "fd389d70-66c1-42d8-8948-437a4b976783",
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
  "content_id": "ecc5cc06-b0a9-4603-9dc1-8c2980d6e4ff",
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
  "content_id": "ba86445f-5146-4dc4-8069-fac1e9153653",
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

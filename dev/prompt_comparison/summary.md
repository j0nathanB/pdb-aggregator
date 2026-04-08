# Old vs New Pipeline — Prompt & I/O Comparison

## Size Comparison

### Country Editor (Mexico)
| | Old (Feb 15) | New (Feb 22) |
|---|---|---|
| System prompt | 44,707 chars | 43,802 chars |
| User message | 19,790 chars | 23,668 chars |
| **Response** | **5,921 chars** | **2,268 chars** |

### Regional Editor
| Region | Old input | Old output | New input | New output |
|---|---|---|---|---|
| Frontline | 8,452 | 1,541 | 1,456 | 881 |
| Western Europe | 13,378 | 3,165 | 1,505 | 727 |
| Middle East | 10,061 | 2,053 | 1,321 | 1,053 |
| Americas | 10,009 | 2,029 | 1,540 | 871 |

### Executive Editor
| | Old | New |
|---|---|---|
| User message | 10,785 chars | 4,254 chars |
| **Response** | **2,374 chars** | **2,225 chars** |

### Copyeditor (Mexico)
| | Old | New |
|---|---|---|
| User message | 6,052 chars | 4,236 chars |
| **Response** | **5,977 chars** | **2,160 chars** |

### Style Editor (Mexico)
| | Old | New |
|---|---|---|
| User message | 5,979 chars | 2,314 chars |
| **Response** | **5,573 chars** | **2,217 chars** |

## Key Differences

### 1. Regional Editor Input (BIGGEST GAP)
**Old:** Receives the full rendered regional lead with ALL cross-cutting dynamics detail — each dynamic's assessment + significance expanded into paragraphs, plus gap paragraphs. 8-13K chars of rich prose.

**New:** Receives a compact JSON with just the `regional_lead` (a single paragraph summary from the regional agent's `regional_overview`), `gap_paragraphs`, and `card_summary_seed`. 1.3-1.7K chars.

**Problem:** The new regional editor has ~85% less material. The regional_overview from the regional agent is already a condensed summary. The old editor got the individual cross-cutting dynamics with their full assessments and significance paragraphs, which gave it much more to work with.

**Fix needed:** Pass the full `cross_cutting_dynamics` list to the regional editor, not just the pre-condensed `regional_lead`.

### 2. Country Editor Input (OK, but response too short)
**Old:** 19.8K user message = assembled markdown section + raw analysis JSON
**New:** 23.7K user message = structured JSON with full raw_analysis (actually MORE input)

Response is 38% of old size. The input is richer now but the LLM is producing shorter JSON responses. The JSON wrapper overhead may be causing the LLM to be more concise. The lack of the full Ukraine example in earlier runs (now added) likely contributed.

### 3. Executive Editor (CLOSE)
Old response: 2,374 chars. New response: 2,225 chars. This is the closest match — the executive editor works similarly in both pipelines because it receives structured items in both cases.

### 4. Copyeditor/Style Editor Cascade
Each pass receives the output of the previous pass. If the editor produces shorter output, the copyeditor and style editor have less to work with, compounding the problem.

### 5. JSON Parse Failures
All style editor traces show `status: raw` — the LLM returned prose instead of JSON, triggering the fallback that keeps the original. This means the style editor pass had NO EFFECT on most sections.

## Recommendations

1. **Regional editor:** Pass full `cross_cutting_dynamics` data, not just the condensed `regional_lead`
2. **Style editor JSON fallback:** If JSON parse fails, treat the entire response as the polished version of the input field
3. **Country editor:** The Ukraine example (now added) should help with response length. Consider adding explicit minimum length guidance.
4. **Executive editor:** Working well enough — minor length difference.

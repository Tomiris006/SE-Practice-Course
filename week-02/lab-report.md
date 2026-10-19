# Lab report — Practice #02: The Prompt Is an Engineering Input

**Name:** Yernur
**Group:** Monday 16:00 - 19:00
**Date:** 19.09.26

> Fill in every section. **Do not delete or renumber the headings** — the grading pass reads them
> by number. If something did not happen, write "did not happen" and why; an empty section and a
> fabricated one are graded the same way.

---

## 1. The frozen experiment

| | |
| --- | --- |
| AI assistant | ChatGPT |
| Exact model name | GPT-5.6 Sol |
| Implementation language | Python |
| Date of the runs | 19.09.26 |

**Non-Python students only** — paste your substituted Prompt B text here, so the substitution can
be checked:

```
(paste here, or write "n/a — used Python")
```

**Confirmations:**

- Each prompt was sent in a **fresh chat**: yes 
- No follow-up questions were asked before Part 7: yes 
- Every output was saved **before** any editing: yes 

---

## 2. Prompt A — minimal

**Prompt sent** (should be exactly one sentence):

```
Write Python code to analyze student marks.
```

**Assumptions the AI made that I never gave it** — list them, one per line. A data format, a pass
threshold, a rounding rule, an input method, an invented feature all count.

1. AI assumed pass_mark must also be numeric and within 0 to 100; otherwise ValueError is raised.
2. AI assumed pass_rate is rounded to 2 decimal places to match the example
3. AI added a rule to reject True and False as marks, even though I never explicitly requested it.

**Questions it should have asked and did not:**

1. I asked questions for clarifying like what if first validates that the list is non-empty and that every mark is numeric and between 0 and 100. It would be valueerror?
2. He did not ask

**Is the function named `analyze_marks` with the required signature?** yes, in a and b it just marks as ai generated:

**First impression before testing** (one sentence — you will compare this with section 6 later):

---

## 3. Prompt B — structured context

**Prompt sent** (paste it in full, including any substitutions):

```
You are a Python developer. Implement analyze_marks(marks, pass_mark=50).
Return average, highest, lowest, and pass_rate in a dictionary. Accept marks
from 0 to 100; raise ValueError for an empty list, non-numeric values, or
out-of-range values. Use no external libraries. Return code plus a short
explanation.

```

**What B fixed compared to A:**

1. It specified `analyze_marks(marks, pass_mark=50)` and a returned dictionary containing average, highest, lowest, and pass_rate.
2. It required `ValueError` for empty, non-numeric, or out-of-range marks instead of ignoring them.

**What B still leaves open:**

1. It does not prescribe the rounding precision of `pass_rate`, so the AI returned 66.66666666666666 for the first harness case.
2. It does not expressly resolve whether booleans and invalid `pass_mark` values count as acceptable inputs; the AI introduced extra validation rules.


---

## 4. Prompt C — examples and tests

**What I appended to Prompt B:**

```
Example: analyze_marks([40, 60, 80], 50) -> average 60, highest 80,
lowest 40, pass_rate 66.67. Include tests for: one mark, decimals, custom
pass_mark, empty list, text value, and marks below 0 or above 100. State any
remaining assumptions before the code.
```

**Tests the AI wrote for itself** — how many, and which situations do they cover?

| Situation | Covered by the AI's tests? |
| --- | --- |
| one mark | Yes — `[75]`|
| decimals | Yes — `[50.5, 70.5, 90.5]` |
| custom pass_mark | Yes — `analyze_marks([40, 60, 80], 70)` |
| empty list | Yes — `[]` must raise `ValueError` |
| text value | Yes — `[40, "60", 80]` must raise `ValueError`|
| below 0 / above 100 | Yes — two separate checks for -1 and 101|

**Do the AI's own tests pass against the AI's own code?** **yes** Executing the transcribed C code printed `All tests passed.`

**Do they agree with the harness in section 6?** **Yes for the six harness cases:**

**Assumptions C stated explicitly before the code:**

- `pass_mark` must be numeric and between 0 and 100, otherwise `ValueError` is raised.
- Passing means `mark >= pass_mark`.
- `pass_rate` is rounded to two decimal places.

## 5. Prompt D — my combined prompt

**The complete prompt I wrote** (one message, sent to a fresh chat):

```
Return a dictionary with exactly: `average`, `highest`, `lowest`, and `pass_rate`.

Requirements: Marks may be integers or decimals from 0 to 100. A mark passes if `mark >= pass_mark`. Raise `ValueError` for an empty list, non-numeric values, or marks outside 0–100. Do not ignore invalid values. Use no external libraries. Return numeric values, not strings.

```

**What I deliberately added that A, B and C did not have:**

1. The output dictionary must have **exactly** the four named keys, with no extras.
2. Return values must be **numeric, not strings** (previous results were numeric, but earlier prompts did not explicitly require this).
3. The prompt states **“Do not ignore invalid values”** and provides a self-contained requirement for integer/decimal marks instead of relying on an appended message; this reinforces B's existing `ValueError` instruction rather than inventing a new behavior.

**The ambiguity I found in the specification, and how I resolved it inside Prompt D:**

The specified `66.67` for three marks implies a **two-decimal pass-rate result**, resolving B's unrounded 66.66666666666666 in practice. D resolves it through the example, not an explicit rounding sentence; the unambiguous wording would be “round `pass_rate` to two decimal places.”

---

## 6. Test results — the evidence

Six cases × four prompts. Verdicts are **PASS**, **FAIL** or **ERROR** only.

| # | Call | Required | A | B | C | D |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `analyze_marks([40, 60, 80], 50)` | avg 60 · high 80 · low 40 · rate 66.67 | ERROR | FAIL | PASS | PASS |
| 2 | `analyze_marks([100], 50)` | avg 100 · high 100 · low 100 · rate 100 | ERROR | PASS | PASS | PASS |
| 3 | `analyze_marks([49.5, 50], 50)` | avg 49.75 · high 50 · low 49.5 · rate 50 | ERROR | PASS | PASS | PASS |
| 4 | `analyze_marks([], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 5 | `analyze_marks([40, "60"], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| 6 | `analyze_marks([-1, 50, 101], 50)` | raises ValueError | ERROR | PASS | PASS | PASS |
| | **Totals** | | **0/6** | **5/6** | **6/6** | **6/6** |

**For every FAIL and ERROR above, one line: what was returned or raised instead.**

| Prompt | Case | What actually happened |
| --- | --- | --- |
| A | 1 | `NameError: name 'analyze_marks' is not defined` — no callable function. |
| A | 2 | `NameError: name 'analyze_marks' is not defined` — no callable function. |
| A | 3 | `NameError: name 'analyze_marks' is not defined` — no callable function. |
| A | 4 | `NameError: name 'analyze_marks' is not defined` instead of `ValueError`. |
| A | 5 | `NameError: name 'analyze_marks' is not defined` instead of `ValueError`. |
| A | 6 | `NameError: name 'analyze_marks' is not defined` instead of `ValueError`. |
| B | 1 | Returned `{'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 66.66666666666666}`, not the required 66.67 pass rate. |

### Pasted terminal output — all four runs

> This is the part that makes the table above count. Paste the **whole** output, unedited,
> including the header lines. A table with nothing behind it is not accepted.

**Prompt A**

```
=== PROMPT A ===
Original code stdout:
Number of valid marks: 6
Average: 71.17
Highest: 100
Lowest: 45
Pass rate: 83.3%
Case 1: ERROR | analyze_marks([40, 60, 80], 50) | NameError: name 'analyze_marks' is not defined
Case 2: ERROR | analyze_marks([100], 50) | NameError: name 'analyze_marks' is not defined
Case 3: ERROR | analyze_marks([49.5, 50], 50) | NameError: name 'analyze_marks' is not defined
Case 4: ERROR | analyze_marks([], 50) | NameError: name 'analyze_marks' is not defined
Case 5: ERROR | analyze_marks([40, '60'], 50) | NameError: name 'analyze_marks' is not defined
Case 6: ERROR | analyze_marks([-1, 50, 101], 50) | NameError: name 'analyze_marks' is not defined
TOTAL: 0/6
```

**Prompt B**

```
=== PROMPT B ===
Original code stdout:
{'average': 72.0, 'highest': 100, 'lowest': 45, 'pass_rate': 80.0}
Case 1: FAIL | analyze_marks([40, 60, 80], 50) | returned {'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 66.66666666666666}; expected {'average': 60, 'highest': 80, 'lowest': 40, 'pass_rate': 66.67}
Case 2: PASS | analyze_marks([100], 50) | {'average': 100.0, 'highest': 100, 'lowest': 100, 'pass_rate': 100.0}
Case 3: PASS | analyze_marks([49.5, 50], 50) | {'average': 49.75, 'highest': 50, 'lowest': 49.5, 'pass_rate': 50.0}
Case 4: PASS | analyze_marks([], 50) | ValueError: Marks list cannot be empty.
Case 5: PASS | analyze_marks([40, '60'], 50) | ValueError: All marks must be numeric.
Case 6: PASS | analyze_marks([-1, 50, 101], 50) | ValueError: Marks must be between 0 and 100.
TOTAL: 5/6
```

**Prompt C**

```
=== PROMPT C ===
Original code stdout:
All tests passed.
Case 1: PASS | analyze_marks([40, 60, 80], 50) | {'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 66.67}
Case 2: PASS | analyze_marks([100], 50) | {'average': 100.0, 'highest': 100, 'lowest': 100, 'pass_rate': 100.0}
Case 3: PASS | analyze_marks([49.5, 50], 50) | {'average': 49.75, 'highest': 50, 'lowest': 49.5, 'pass_rate': 50.0}
Case 4: PASS | analyze_marks([], 50) | ValueError: Marks list cannot be empty.
Case 5: PASS | analyze_marks([40, '60'], 50) | ValueError: All marks must be numeric.
Case 6: PASS | analyze_marks([-1, 50, 101], 50) | ValueError: Marks must be between 0 and 100.
TOTAL: 6/6
```

**Prompt D**

```
=== PROMPT D ===
Original code stdout:
All tests passed.
Case 1: PASS | analyze_marks([40, 60, 80], 50) | {'average': 60.0, 'highest': 80, 'lowest': 40, 'pass_rate': 66.67}
Case 2: PASS | analyze_marks([100], 50) | {'average': 100.0, 'highest': 100, 'lowest': 100, 'pass_rate': 100.0}
Case 3: PASS | analyze_marks([49.5, 50], 50) | {'average': 49.75, 'highest': 50, 'lowest': 49.5, 'pass_rate': 50.0}
Case 4: PASS | analyze_marks([], 50) | ValueError: Marks list cannot be empty.
Case 5: PASS | analyze_marks([40, '60'], 50) | ValueError: All marks must be numeric.
Case 6: PASS | analyze_marks([-1, 50, 101], 50) | ValueError: Marks must be between 0 and 100.
TOTAL: 5/6
```

---

## 7. Scoring

0–2 per criterion, using the rubric in `README.md` Part 7.

| Criterion | A | B | C | D |
| --- | --- | --- | --- | --- |
| Correctness (cases passed) | 0 | 1 | 2 | 2 |
| Requirement coverage | 0 | 1 | 2 | 2 |
| Verifiability (tests) | 0 | 0 | 2 | 2 |
| Assumptions stated | 0 | 0 | 2 | 2 |
| Noise (2 = none) | 0 | 1 | 1 | 1 |
| **Total / 10** | **0** | **3** | **9** | **9** |

**Prompt length, in words:** A **7** · B **44** · C **84** · D **95**

**Words added per point gained** — B over A, C over B, D over C. One line on what that ratio says:

**(44−7)/(3−0) = 12.33** extra words/point; C/B: **(84−44)/(9−3) = 6.67** extra words/point; D/C: **not defined** (0 additional points), despite D being a self-contained rewrite rather than a literal addition. This suggests examples and executable tests added more measurable value than rewriting an already passing contract.

---

## 8. Conclusion — 150–200 words

Answer in this order: (1) which prompt scored best, and whether it is the one you would actually
use at work; (2) which single addition bought the most correctness, naming the exact case that
changed verdict; (3) what was pure noise; (4) the ambiguity and your resolution.

Name test cases and real returned values. "More detailed prompts work better" scores zero.

```
Prompts C and D tied for the highest provisional score (9/10), and both passed all six harness cases. I would use D at work because its single message defines the exact dictionary keys and requires numeric results; C relied on B plus an appended request. A passed 0/6 because the supplied script never defined analyze_marks: case 2 raised NameError instead of returning an average of 100. B improved to 5/6 once the function and validation contract were specified. The clearest single addition was C's expected pass_rate of 66.67 for [40, 60, 80]; it changed case 1 from B's returned 66.66666666666666 (FAIL) to 66.67 (PASS). C and D correctly returned 49.75 for the decimal average in case 3, and raised ValueError for the empty input in case 4. The extra validation of boolean marks and restrictions on pass_mark were not requested; they did not affect these six cases and added specification noise. The rounding rule was ambiguous in B. C stated the 66.67 expected result and its response explicitly assumed two decimal places. D reused that example, but could make the rule clearer by directly requiring round(pass_rate, 2).

```

**Word count:** 187

---

## 9. Two questions for the debrief

Written before class, answered in class.

1. If the example states 66.67 but the prompt does not explicitly say “round to two decimal places,” should the harness require exact equality or use a tolerance?
2. How should a prompt-engineering experiment distinguish a bad prompt from a missing function caused by an output that was not the requested code (as happened with the first reply to A)?

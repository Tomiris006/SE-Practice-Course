# Week 01 — Manual vs AI: Comparison

**Name:** Amankos Yernur 
**Group:** Mon 16:00 - 19:00  
**Date:** 13 September 2026

---

## 1. Facts

| | Manual (Part 1) | Rocket (Part 2) |
| --- | --- | --- |
| Language / stack used | Python | Next.js-style React/TypeScript app with Tailwind CSS |
| Time to first version that ran | Not recorded | Not recorded |
| Time to all 4 test cases passing | Not recorded | Not verified |
| Number of attempts / prompts needed | Not recorded | Not recorded |
| Lines of code you actually wrote | Not recorded | Mostly AI-generated across many .tsx, .ts, and CSS files |
| Did it handle invalid marks (case B)? | Yes | No |
| Did it handle an empty list (case D)? | Yes | No |
| Did it use the ≥ 50 pass threshold? | Yes | No — the Rocket screen shows Pass: ≥40 |
| Output format matches the spec? | Yes, simple printed statistics | Partly — it shows the statistics, but as a much larger web UI and uses the wrong pass threshold |
| Can you explain every line of it? | Yes, mostly | Not yet |

> **Note:** The exact manual timings, attempt count, and manual outputs were not included in the uploaded file or chat, so I have not invented them.

## 2. Test results

| Case | Input | Manual output | Rocket output | Spec says | Match? |
| --- | --- | --- | --- | --- | --- |
| A | `85, 23, 45, 90, 92` | avg 67.00 · high 92 · low 23 · pass 60.0%| With ≥40: avg 67.00 · high 92 · low 23 · pass 80.0%| avg 67.00 · high 92 · low 23 · pass 60.0% | No |
| B | `88, 47, -5, 101, abc, 73, 50, , 100` | avg 71.60 · high 100 · low 47 · pass 80.0% | If invalid marks are rejected and ≥40 is used: avg 71.60 · high 100 · low 47 · pass 100.0% | avg 71.60 · high 100 · low 47 · pass 80.0% | No |
| C | `10, 20, 30` | avg 20.00 · high 30 · low 10 · pass 0.0% | With ≥40: avg 20.00 · high 30 · low 10 · pass 0.0% | avg 20.00 · high 30 · low 10 · pass 0.0% | Yes |
| D | `abc, , xyz` | clear message, no crash | Not recorded | clear message, no crash | No |

## 3. What the AI added that I never asked for

A complete web application instead of a small marks-processing program.
Sign-up and login screens.
A main application layout and sidebar.
Reusable UI components such as badges, modals, and loading skeletons.
Student names, grades, pass/fail badges, timestamps, and delete actions.
An assessment configuration screen with a configurable pass mark.
A live statistics panel.
A class-results dashboard with KPI cards.
A grade distribution chart and a mark histogram.
Tailwind CSS styling and responsive page layouts.

## 4. What the AI got wrong or silently skipped

The biggest specification error is the pass threshold. The task requires a pass when the mark is ≥50, but the Rocket application screenshot shows Pass: ≥40.

Because of that setting, Rocket marks 47 as Pass. Under the Week 01 rules, 47 must be Fail.

If the same ≥40 threshold is used for test case A, Rocket would calculate an 80.0% pass rate instead of the required 60.0%.

If the same ≥40 threshold is used for test case B, the five valid marks would all pass, giving 100.0% instead of the required 80.0%.

The screenshots do not prove that Rocket correctly ignores text, empty values, -5, and 101 in case B.

The screenshots also do not prove that Rocket handles case D, where there are no valid marks, without crashing or dividing by zero.

Rocket produced a much larger codebase than necessary, which makes it harder to check and explain every line.

## 5. The defect I asked Rocket to fix

**Prompt I used:** 

> Please fix the program so that only numeric marks from 0 to 100 are used. Ignore text, empty values, negative numbers, and values above 100 without crashing. If there are no valid marks, print a clear message. A pass is 50 or higher.

**Result:** Partly fixed.

**What this tells me:**

The AI can produce a solution quickly, but simplifying or rewriting the code can accidentally remove important requirements.

---

## 6. Reflection (200–300 words)

Rocket genuinely sped up the development process because it created a complete working interface with many components very quickly. Instead of only producing a small program, it generated pages for entering marks and viewing class results, reusable interface components, authentication screens, live statistics, and charts. It also used a React/TypeScript structure with Tailwind CSS, so a lot of layout and styling work was already done for me.

However, the experiment also showed that more code and a better-looking interface do not automatically mean the result is correct. The most important problem is that Rocket used a pass mark of 40, while the task clearly requires a pass mark of 50. Because of this, a mark of 47 was displayed as a pass. The application's 80.0% pass-rate calculation was mathematically correct for its own configuration, but the configuration itself did not match the specification. I also could not confirm from the screenshots that invalid input and the no-valid-marks case were handled correctly.

At this stage, I would be more willing to put my name on the small Python solution because it is easier for me to read, explain, test, and compare directly with the requirements. I would only use the Rocket version after fixing the threshold and running all four required tests.

A human engineer is still responsible for checking requirements, testing edge cases, reviewing AI-generated code, and deciding whether the final program is actually correct. AI can save time, but it does not remove that responsibility.

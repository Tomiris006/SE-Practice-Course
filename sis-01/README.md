# SIS #01 — Software Engineering Fundamentals, With an AI in the Loop

**AI-Driven Software Engineering · KBTU SITE · Fall 2026**
**SIS #01 · 2 points · individual · deadline Sunday 11 October 2026, 23:59**
**AI use: required** — Level D, and the working process below is built around it.

> **Your choice, frozen once made.** Use any AI assistant you have access to — ChatGPT, Claude,
> Gemini, DeepSeek or another. Use one assistant for Prompts A, B and C (the same one is enough),
> and record the **exact model** it shows. "ChatGPT" is a tool, not a model. If the tool does not
> show the model, write `not displayed` — that is an accepted answer.
>
> **What stays identical for everyone:** the ten topics, the five-stage process, the three prompts
> word for word except their bracketed fields, the word limits, the two evidence tables, and the
> file names in this folder. That is what makes forty reports comparable and gradeable.
>
> **Coding is optional.** This assignment assesses analysis, not programs.

This is **Assignment #01** of the course — the same ten questions, the same process and the same
prompts that every group receives. The report is a Markdown file in your repository, you get a
checker you can run yourself, and the rubric is written below.

**The submission is the link to your open pull request, pasted into the Teams assignment** — not a
file upload.

---

## What you hand in

```
sis-01/
├── README.md            this file — read-only
├── report.md            ← the ONLY file you write your report in: report, reflection,
│                          references and the AI evidence appendix, in numbered sections
├── AI_USAGE.md          ← your AI disclosure, as every week
├── submission.yml       ← the declaration: facts only, filled in last (§10)
└── tests/
    ├── check_report.py         checks the SHAPE of report.md — do not edit
    └── validate_submission.py  checks submission.yml against report.md — do not edit
```

**Time:** plan for about 4–5 hours in total, spread over at least two days — stage 4 (checking
sources) needs a library or a textbook open, and you want a night between the draft and the review.

---

## 1. Choose ONE topic (≈ 10 min)

Based on Sommerville, *Software Engineering* 10th ed., chapter 1 exercises, and Lessons 01–02.
Write its number on the `**Topic:**` line at the top of `report.md`.

| # | Topic | What to do |
| --- | --- | --- |
| 1.1 | Professional software delivery | Explain what a customer needs beyond program code. Use AI to propose a delivery checklist, then justify the documents, tests and support your scenario needs. |
| 1.2 | Generic and custom software | Compare who controls requirements and product changes. Use AI to compare a generic product with a custom solution, then explain the consequences for users. |
| 1.3 | Software engineering and cost | Explain how engineering methods can reduce costs over a system's life. Challenge AI claims that faster code generation always means lower total cost. |
| 1.4 | Ethical responsibilities | Discuss at least three ethical issues in software development. Ask AI for examples, then analyze stakeholders, possible harms and safeguards in your scenario. |
| 1.5 | Different application types | Compare two application types and the engineering techniques they need. Check whether AI gives useful distinctions about risk, testing and system constraints. |
| 1.6 | Fundamental engineering principles | Apply process, dependability, requirements management and reuse to your scenario. Evaluate what AI can assist with and what engineers must still decide. |
| 1.7 | Connected development teams | Explain how online collaboration supports development teams. Use AI to propose a workflow, then assess review, coordination and responsibility for changes. |
| 1.8 | Competence and professional practice | Discuss risks when developers lack independently verified competence. Assess AI advice about skills, review and accountability. Label any legal claim for verification. |
| 1.9 | The software engineering code of ethics | Use the eight principles in the ACM/IEEE-CS short code. Ask AI for one example per principle, then check each mapping and explain your corrections. |
| 1.10 | Software-controlled drones | Discuss social challenges of drone systems, including privacy, safety and accountability. Critique AI suggestions and justify safeguards for one hypothetical use. |

For 1.9, use the **short version** of the code:
<https://www.acm.org/code-of-ethics/software-engineering-code>.

## 2. Your scenario (≈ 20 min) → `report.md` section 1

Choose one small scenario that fits your topic — equipment booking, a marks analyzer, a drone that
inspects buildings, or your own. For 1.2 and 1.5, a **justified comparison of two systems** is
allowed instead of one scenario; say so in *Question*.

Fill the six labels in section 1: **Question, Users, Problem, Constraints** (two of them),
**Risk** (one important failure or misuse risk) and **Assumptions** (label every fictional detail
as fictional). Use these details in every prompt and throughout your answer.

AI use is required in your *working process*. The system you describe does **not** need an AI
feature.

## 3. The working process

| Stage | Your action | Evidence you save | Where it goes |
| --- | --- | --- | --- |
| 1. Prepare | Write 5 initial points **yourself**, before any prompt | Initial outline and scenario | sections 1 and 7 |
| 2. Draft | Run Prompt A with your context | The complete prompt and response | section 8, B1 |
| 3. Critique | Run Prompt B; evaluate its feedback | The critique, and your judgment of it | section 8, B2; section 3 |
| 4. Check | Verify 2 factual claims in real sources | Source checks and citations | section 9, verification table; section 6 |
| 5. Revise | Run Prompt C, then edit yourself | The revised output, the change log, the final report | section 8, B3; section 9, change log; sections 2–4 |

**Commit as you go — three commits minimum, and this order is the one we expect to see:**

```
git commit -m "sis-01: scenario and initial outline, before Prompt A"
git commit -m "sis-01: exchanges A, B, C and both evidence tables"
git commit -m "sis-01: final report, reflection and declaration"
```

The first commit, pushed before you run Prompt A, is your evidence that the outline was yours.

## 4. The three prompts — use them word for word

Replace **every** `[bracketed field]` with your own text, change nothing else, and run each one in
the order given. Save the **complete** prompt you actually sent and the **complete** response,
before editing anything. The checker looks for the fixed sentences below and for any bracket you
forgot.

**Prompt A — a contextual draft** → section 8, B1

```text
Act as a software engineering tutor. Help me analyze topic [number and question] for a first-year-level university assignment.

My scenario is [users, problem, constraints and risk]. My initial ideas are [five points]. Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
```

**Prompt B — a critical review** → section 8, B2

```text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: [paste]. Scenario: [paste]. Draft: [paste the full Prompt A response].
```

The same assistant is enough. **Its critique is another claim to evaluate, not independent
evidence** — you accept, qualify or reject each point, and say why in section 3.

**Prompt C — a revision using evidence** → section 8, B3 (run it *after* stage 4)

```text
Revise the draft using my review decisions and source notes below. Keep the answer relevant to my scenario and preserve uncertainty where evidence is limited.

My decisions: [accepted or rejected feedback and reasons]. Verified evidence: [notes with citations]. Draft: [paste].

Show what you changed and why. Use only the sources I supplied. Flag remaining gaps instead of inventing details.
```

In Prompt C, `Draft: [paste]` is the Prompt A response. Read the revised output, **edit it
yourself**, and make sure you can explain every final claim without the assistant.

## 5. Verify at least two claims (≈ 60 min) → section 9 and section 6

Pick two factual claims from the draft or the critique. **Open and read** the relevant lecture,
textbook section or authoritative publication yourself. For each claim, fill one row of the
verification table:

| Column | What goes in it |
| --- | --- |
| AI claim | the exact wording, copied |
| Source and locator | title + page, slide, section or chapter — or title + URL + access date (YYYY-MM-DD) |
| Evidence found | what the source actually supports, in your words |
| Decision | one word: `keep`, `qualify` or `reject` |

Give every source a full reference in section 6; every URL in the table must also appear there.
If you cannot find evidence for a claim, mark it unverified in section 3, remove or qualify it in
your answer, and pick two other claims you *can* check.

## 6. The report — `report.md`, sections 1–5

| Section | Required content | Words |
| --- | --- | --- |
| 1. Scenario | Question, users, problem, constraints and risk | 100–150 |
| 2. Analysis | Your answer, the trade-offs, the application to your scenario, at least two engineering decisions and why they fit | 350–400 |
| 3. Review | Two revisions and two source checks, with reasons; what you did with Prompt B's critique | 250–300 |
| 4. Conclusion | Your recommendation and its main limitation | 100–150 |
| **Main report total** | sections 1–4; references and appendix excluded | **800–1,000** |
| 5. Reflection | Separate: what helped, what you changed, what you learned — **written by you** | 150–200 |

**How words are counted:** every whitespace-separated token with a letter or digit in it, the
**Label:** words in section 1 included, `<!-- comments -->` excluded. The checker prints each
count; trust it over your editor.

**Specific beats generic — this is the difference between a strong and a weak review:**

| Worthless | Worth something |
| --- | --- |
| "The AI's answer was mostly correct." | "The draft said most software cost is development. Sommerville ch. 1, Figure 1.1, says evolution often costs more for custom software, so I qualified it (verification row 2)." |
| "I improved the wording." | "Change-log row 1: 'the tests prove the program is correct' became 'the tests show the agreed cases behave as specified' — tests cannot prove the absence of errors." |

The assignment's own example of a substantive correction:

> **Illustrative AI claim:** "Once the program runs correctly, professional software development
> is complete."
> **Student correction:** A marks analyzer also needs agreed calculation rules, test evidence,
> user instructions and a plan for maintenance. A successful run proves only the behavior observed
> in that run.

## 7. The AI evidence appendix — sections 7, 8 and 9

- **Section 7 — Appendix A:** the initial outline and scenario notes, written **before** Prompt A.
  Five numbered points.
- **Section 8 — Appendix B:** at least three meaningful exchanges — draft (B1), critique (B2),
  revision (B3) — each with **Tool, Model, Date, Purpose**, the complete prompt and the complete
  response **as text**, never screenshots. Extra exchanges go in B4, B5 …
- **Section 9 — Appendix C:** the verification table (≥ 2 rows) and the change log (≥ 2
  substantive revisions: your final version must differ from the AI wording, and the reason must
  name the evidence or the scenario constraint behind it).

## 8. Responsibility

- Use fictional or anonymized scenario data. No personal information, passwords or confidential
  material in any prompt.
- Write the reflection and the initial outline yourself.
- **Do not fabricate prompts, responses, evidence or references.** A source you did not open is a
  fabricated source. This follows the university's academic-integrity policy, and it is the one
  failure the rubric cannot forgive.
- Be ready to discuss, in class and without the assistant: *What did you change? What evidence
  supports it? What remains uncertain?*

## 9. Check your work

The checker reads `report.md` and runs **24 checks** of its shape: sections, word counts, the six
scenario labels, five outline points, three complete exchanges, the fixed prompt sentences,
leftover brackets, the draft carried into Prompts B and C, both tables, the references, and
leftover `(write here)` markers.

**It checks shape, never quality.** 24 PASS means your report can be graded — not that it is good.
Your analysis, your review and your reflection are read by a person.

```
PASS   the check is satisfied
FAIL   the thing is there but wrong: a word count outside its range, a table with one row,
       a prompt with a [bracketed field] never replaced
ERROR  the thing cannot be checked at all: report.md missing, a section heading deleted
```

**Path A — you have Python 3 (any version from 3.8):**

```
cd sis-01
python tests/check_report.py
```

**Path B — no Python on your machine:** you lose nothing and install nothing. On GitHub, open
your repository → **Code → Codespaces → Create codespace on sis-01**. The terminal at the bottom
of that browser editor has Python; run the same two commands there. A free account includes more
than enough hours for this.

A shipped template gives `pass=3 fail=19 error=2` on the first run. That is the intended start.

## 10. The declaration — `submission.yml` (≈ 5 min, last)

Facts only — who you are, your topic, the assistant and exact model (the one in B1), your checker
numbers, your counts, your decisions, and the IDs of any check still failing. Nothing is written
twice: explanations stay in `report.md`.

```
python tests/check_report.py          # the final run — copy its three numbers
git add . && git commit -m "sis-01: final report"
git rev-parse --short HEAD            # this hash goes in checker.commit
python tests/validate_submission.py   # then fix anything it flags, commit and push
```

**`checker.commit` is the commit you ran the checker at** — normally the one just before the
commit that adds your filled declaration. That one-commit gap is expected.

Two things that decide marks:

- **Your numbers are re-run.** We run `check_report.py` on your pull request ourselves. Numbers
  that match are settled automatically. Numbers that do not match — with no change to `report.md`
  after the commit you named — cost the whole workflow criterion.
- **A FAIL you report costs you nothing extra.** If a section is 410 words and you decided that was
  right, list `W2` under `known_fails` and say why in section 3. Hiding it is what costs.

## 11. Submit

```
git checkout main
git pull
git checkout -b sis-01
# unzip SIS_01.zip (from the Teams assignment) into your repository root,
# so that sis-01/ sits next to week-01/, week-02/ ... then work and commit
git push -u origin sis-01
```

1. Branch **`sis-01`** off `main`, folder **`sis-01/`** at the top of your `se-practice`
   repository. Never commit to `main`.
2. At least **3 meaningful commits**, authored by your own GitHub account (§3 shows the order).
3. Open **one pull request `sis-01 → main`** in your own repository.
   Title: `SIS 01 — Topic 1.N — <your topic title>`.
   Description: the five-section shape from `SETUP.md` §4 — What I built · AI tools used · What the
   AI got wrong · Time spent · What I would do differently.
4. **Leave the PR open. Do not merge it.**
5. In the Teams assignment: **+ Add work → Link → paste the pull request URL.**
   It looks like `https://github.com/<you>/se-practice/pull/N`. Not the repository URL.

**Deadline: Sunday 11 October 2026, 23:59 (Almaty).** Lateness is read from GitHub's server-side
push time, not from commit dates. Late work follows the course policy.

## 12. Grading — 2 points, 8 criteria × 0.25

| # | Criterion | Full 0.25 | Half 0.125 | Zero |
| --- | --- | --- | --- | --- |
| 1 | **Topic & scenario** | One topic; users, problem, two constraints, one risk; fictional details labelled; the scenario is used in the answer | A label thin or generic, or the scenario disappears after section 1 | No scenario, or a different topic from the one declared |
| 2 | **Analysis** | Answers the chosen question; real trade-offs; at least two engineering decisions justified by the scenario | Answers the question, but decisions are generic or not tied to the scenario | Off-topic, or the unedited AI draft |
| 3 | **Critique handled** | Each Prompt B point accepted, qualified or rejected, with a reason; at least one AI claim challenged on substance | Critique summarized but not judged | Critique missing or accepted wholesale |
| 4 | **Verification** | Two claims checked in sources actually read; exact locators; keep / qualify / reject each justified | One claim properly checked, or locators vague | No real checks — or a source you did not open |
| 5 | **Revisions** | Two substantive changes in the change log, each visible in the final text, each with its evidence or constraint | One substantive change, or reasons that name no evidence | No real changes (wording swaps only) |
| 6 | **Conclusion & reflection** | A recommendation and its main limitation; a reflection in your own words that names specific moments | Generic conclusion or reflection | Missing, or written by the assistant |
| 7 | **AI evidence appendix** | Outline before Prompt A; three complete exchanges with tool, model, date, purpose; prompts used as given, every bracket replaced | One exchange incomplete, or metadata missing | Exchanges missing, paraphrased or fabricated |
| 8 | **Structure & workflow** | Word counts in range (or declared under `known_fails` with a reason), references complete; `sis-01` branch, ≥ 3 commits by you, open PR in the standard shape, `AI_USAGE.md` complete, `submission.yml` validating | One element missing | Committed to `main`, PR merged, no disclosure, **or declared checker numbers that do not match the re-run** |

**A FAIL you report and explain costs you nothing; one you hide costs the whole criterion.**
An accurately reported "I could not verify this claim, so I removed it" scores full marks on
criterion 4. The assistant you chose never affects the mark.

**Not accepted (0 for the SIS):** a file upload instead of a pull-request link · a report
that is not in `sis-01/report.md` · a merged PR, a repository link or a branch with no PR ·
fabricated prompts, responses or references.

## 13. FAQ

**Can I upload a PDF or a Word file to Teams instead?** No. The report is `sis-01/report.md`,
and the only thing you paste into Teams is the pull-request link.

**My tool does not show the model.** Write `not displayed` in B1–B3 and in `submission.yml`.

**Can I use two assistants?** Yes — record each exchange's own tool and model. `submission.yml`
names the one you used for Prompt A.

**The AI's response contains its own ``` code block and breaks my report.** Open and close that
response block with `~~~~` instead of ```` ``` ````.

**My analysis is 405 words and I think it is right.** Then say so: list `W2` under `known_fails`
and give the reason in section 3. That is a decision, not a violation.

**Can I delete the `<!-- -->` guidance comments?** Yes. Never delete the headings or the
**Label:** words.

**The checker says E7: Prompt B contains 12% of the Prompt A response.** You shortened or
summarized the draft when pasting it into Prompt B. The prompt says *the full Prompt A response* —
paste all of it and run B again.

**I finished early — can I add code?** You may, in `sis-01/code/`. It is optional and not graded.

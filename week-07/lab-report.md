# Week 07 — Testing AI-Generated Code

**Course:** AI-Driven Software Engineering (Fall 2026, KBTU SITE)
**Practice work #07** · 1 point · AI-use level: **D (AI-integrated, disclosure required)**
**Deadline:** Friday 6 November 2026, 23:59 (Almaty). Practice #08 builds on this suite and is due
on Sunday, so finish this one first.

> **This week continues your Week 06 Bolt project.** You pull its booking decision out into one
> function, `canBook`, then you ask an assistant to write the tests for it. The lab is about
> **judging those tests**. You check the expected values against the criteria, run the tests for
> real, and plant three defects to see whether the suite catches them.
>
> **Fixed for everyone:** the test runner is **Vitest**, the deck's tool. The project's language is
> whatever Bolt generated, usually TypeScript, sometimes JavaScript, and both work the same way here.
> **Your choice:** the assistant that writes the tests. Bolt's own chat is the easiest, because it
> already sees your code. ChatGPT, Claude, Copilot or any other assistant works too, if you paste
> the code into it. Freeze the assistant and record its exact model.
>
> **Also identical for everyone:** the scenario and AC1–AC6 (§3), the function's interface (§3),
> the case plan T01–T14 (§6), the deck's two prompts (§5), the three defects M1–M3 (§5, Part 6),
> and the file layout (§2).
>
> **No Week 06 project?** You missed Practice #06, or your export is broken. Use `starter/`
> (Part 0) and declare it in `submission.yml`. It costs you nothing.

---

## 1. The idea of this lab

Week 05's checker ran your tests against ten broken versions of `can_book` and told you which ones
slipped through. This week you are the checker. An assistant writes the suite, and you decide
whether it deserves your trust.

Generated tests can be wrong in a way that looks right. An assistant that misreads AC2 writes code
that rejects exactly 120 minutes, and then writes a test that expects exactly that. Both come from
the same misunderstanding, so both agree, and the suite is green. A test only means something when
its expected value comes from the acceptance criteria, **not from the code it is testing**.

So you work through the deck's seven tasks in order:

1. Extract `canBook` so that the test and the page call the same code.
2. Compute the expected results yourself.
3. Generate the tests.
4. Review them before you run them.
5. Run them, diagnose the failures, and improve the suite.
6. Plant three defects to see whether the suite notices.
7. Check by hand the parts no unit test can see.

**Main message (the deck's own rule):** a passing suite is evidence only for the cases and the
assertions it actually checks.

**Time budget:** ~45 min in class (Parts 0–3) + ~90 min at home (Parts 4–8).

---

## 2. Deliverables

By the deadline, your branch `week-07` must contain:

```
week-07/
├── README.md                  # this file (read-only)
├── lab-report.md              # THE worksheet — fill in all 10 sections
├── AI_USAGE.md                # AI disclosure (every week)
├── submission.yml             # machine-readable declaration — facts only
├── app/                       # YOUR project (source only, no node_modules/)
│   ├── package.json           #   with vitest in devDependencies
│   └── src/
│       ├── booking.ts         #   canBook, extracted in Task 1   (or booking.js)
│       ├── booking.test.ts    #   your FINAL suite, beside it    (or booking.test.js)
│       └── App.tsx …          #   the page, which imports canBook
├── suites/first/
│   └── booking.test.ts        # the assistant's FIRST suite, exactly as generated
├── evidence/
│   └── ui-1.png … ui-5.png    # the five manual UI checks (ui-4 at phone width)
├── starter/                   # provided — only if you have no Week 06 project
└── tests/
    ├── check_suite.py         # provided checker — do not edit
    └── validate_submission.py # provided validator for submission.yml — do not edit
```

**Never commit `node_modules/` or a `.env` file.** Make sure `node_modules/` is in your
repository's `.gitignore` (`SETUP.md` §5) **before** you run `npm install`.

---

## 3. The task

The scenario is the one from the Lesson 07 practice deck, unchanged. AC1–AC6 are word for word
those of Practice #06, the project you are continuing:

```text
User story: As a student, I want to check a room's availability so that I can choose a valid booking time.
Continue the final Smart Campus prototype from Practice #06. One room, fictional bookings, and an availability decision.
Keep the scope: no login, database, or saved bookings.

AC1: Accept a candidate interval only when 0 ≤ start < end ≤ 1440 and start is after the supplied current time.
AC2: Reject a booking longer than 120 minutes.
AC3: Reject the request when the selected room is blocked.
AC4: Reject any interval that overlaps an existing booking; touching endpoints are allowed.
AC5: Show a clear Available / Unavailable decision without changing the existing booking data.
AC6: The page remains usable at desktop and narrow/mobile width and gives understandable validation feedback.

Automate the booking rules and data-preservation checks. Check the visible page behavior separately.
```

**The interface.** Every student uses the same one, so every suite reads the same way and
Practice #08 can drop a replacement function into your project:

```ts
export function canBook({ start, end, now, blocked, bookings }): boolean
// start, end, now: minutes after midnight on the same day (600 = 10:00, 1440 = 24:00)
// blocked: true when the room is blocked
// bookings: the room's existing bookings, e.g. [{ start: 600, end: 660 }]
// returns true (Available) or false (Unavailable)
```

It lives in `src/booking.ts` (or `src/booking.js` in a JavaScript project), and **the page must
call it**. The deck's example interface and fixture are exactly this. We fix it so that it is the
same for everyone.

**Test levels in this lab** (deck): *unit* tests check `canBook` alone (Parts 3–6). An
*integration* check makes sure the page really uses the same function, which the checker verifies
by reading the imports. *Manual UI* checks cover what a unit test cannot see (Part 7).

**One question is deliberately open.** No AC says what `canBook` should do when an **existing**
booking is invalid, for example `{ start: 700, end: 650 }`. Find out what *yours* does, declare it
(`assumptions.invalid_existing_booking`) and discuss it in §9.3. Any answer is acceptable, but you
have to actually check.

---

## 4. Before class

- Your Week 06 project. Either your `week-06` branch, with the final export in
  `week-06/prototype/`, or the Bolt project itself, signed in.
- **Somewhere to run Node and Vitest.** Pick one before class and try it:
  - **Your computer:** Node.js 18 or newer (`node --version`).
  - **Bolt.new's terminal:** open your project, use the terminal tab. You run the tests there,
    then download the project into `app/` at the end.
  - **GitHub Codespaces:** your repository → **Code → Codespaces → Create codespace**. Node and
    Python are already installed.
- Python 3.8+ to run the checker, or the same Codespace.

---

## 5. The lab

### Part 0 — Setup (~5 min, in class)

1. `git checkout main && git pull && git checkout -b week-07` (full steps in `SETUP.md`).
2. Bring your project into `week-07/app/`, **before** you unzip anything:
   - **From your Week 06 branch** (the usual case):
     ```text
     mkdir week-07
     git checkout week-06 -- week-06/prototype
     git mv week-06/prototype week-07/app
     ```
   - **From Bolt:** download the project again and unzip it so that `week-07/app/package.json`
     exists.
3. Unzip `Week_07.zip` into the root of your repository, so that `week-07/README.md` sits next to
   `week-07/app/`. **No Week 06 project?** Run `cp -r week-07/starter week-07/app` now.
4. Check that `node_modules/` is in your `.gitignore`. Fill in `lab-report.md` §1.
5. Commit: `week-07: baseline project from week 06` (or `… from starter`). **This commit is your
   "before".** The deck asks you to save a version before editing, and this is that version.

### Part 1 — Task 1: baseline and extraction (~10 min, in class)

1. Find where the project decides Available / Unavailable. Bolt often puts it inside the page
   component. Fill in the "before" table of §2.
2. Create `src/booking.ts` (or `.js`) with `export function canBook({ start, end, now, blocked,
   bookings })`, and move the decision into it. **Do not change the behaviour on purpose.** Copy
   the conditions as they are, even the ones you suspect. If one is wrong, the tests will show it,
   and that is the point.
3. Make the page call it: `import { canBook } from './booking'`. The conversion from `HH:MM` to
   minutes and the validation messages stay in the page.
4. Check in the browser that the page still behaves the same. Write §2.
5. Install Vitest in `app/`: `npm install` then `npm install -D vitest`, and add
   `"test": "vitest run"` to the `scripts` in `package.json`. In Bolt, use Bolt's terminal.
   If you run out of AI credits, you can still edit and run tests by hand. You do not need the
   assistant for this part.
6. Commit: `week-07: extract canBook into src/booking`.

### Part 2 — Task 2: the test plan (~10 min, in class)

The fourteen cases are in §6. **Before you open any assistant**, write in §3 of the worksheet the
**reason** for each expected result, in your own words. "Because the AC says so" is not a reason.
"660 is excluded from 600–660, so the intervals only touch" is a reason.

Then add **two cases of your own**, X1 and X2. Each is a boundary or a state that T01–T14 do not
reach, with its expected result and its AC. Examples of what kind, not answers: the other end of
the day, two bookings at once, a request that touches two bookings.

Commit: `week-07: test plan with reasons`.

### Part 3 — Task 3: generate the first suite (~10 min, in class)

1. Send the deck's prompt in a **fresh** chat. `[our test framework]` becomes `Vitest`, and the
   only other thing you add is your case table from §3 and, unless the assistant already sees it,
   the code of `booking.ts`:

```text
Generate tests for the existing booking function using [our test framework]. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.
```

2. Save the test file it returns **exactly as generated** as `suites/first/booking.test.ts` (or
   `.js`). Do not fix anything in it yet. Paste the prompt as sent and the rest of the answer (run
   command, AC mapping, flagged requirements) into §4.
3. Copy the same file to `app/src/booking.test.ts`. That copy is the one you will change.
4. Commit: `week-07: first suite as generated`.

### Part 4 — Task 4: review before you run (~15 min, at home)

Read the first suite against your plan **before running it**. These are the deck's four weak
tests:

| Weak test | Why it is weak | Improvement |
| --- | --- | --- |
| No exception occurred | Wrong answers may still pass | Assert the exact decision |
| Expected = current output | Copies the behavior under test | Derive expected from an AC |
| Only valid requests | Misses rejection rules | Include limits and overlaps |
| Mocked booking function | Never exercises the real logic | Import the function used by UI |

Also check the imports, the expected values, isolation (one shared array that every test
changes?), duplicate cases and skipped tests. Write at least **two** decisions in §5: *accept*,
*revise* or *reject*, each with the AC or the reason.

**Rules for the final suite**, which the checker reads (§7):

- One test per case, with **the ID in its title**: `test('T05 AC1: past the end of the day …')`.
  No `test.each`, so that every ID has its own name.
- Every T test asserts the exact decision, `.toBe(true)` or `.toBe(false)`. Never
  `toBeTruthy`, and never "it did not throw".
- An **AC5** test: call `canBook` on an **Available** request, then compare `bookings` with a copy
  taken before the call (`JSON.stringify`, or `toEqual` against `structuredClone`). A rejected
  request may never reach the code that changes them.
- Your **X1** and **X2** tests. That makes at least **17 tests**.
- Fixed time: `now` is a number, and there is no `Date.now()` and no `new Date()`. Use a fresh
  fixture per test.
- `import { canBook } from './booking'`: the real module. No `vi.mock`, no `.skip`, no `.only`.

### Part 5 — Task 5: run, diagnose, improve (~20 min, at home)

1. Run the **first** suite as it is: `npx vitest run`. Paste the **real** output into §6.1, from
   the `RUN  v…` line to the `Tests` line. A build success or an assistant saying "tests pass" is
   not a run. Write the Vitest version into §1.
2. Diagnose every failure in the §6.1 table (deck):

   | Observed failure | First check | Next action |
   | --- | --- | --- |
   | Import / runner error | Path, export, dependency, config | Fix setup and rerun |
   | Assertion mismatch | Input + expected result against AC | Correct the test or the code |
   | Changing result per run | Clock, shared state, test order | Fix time and reset fixtures |
   | No tests discovered | Filename and test command | Use a detected test file |

   **A failing test is not automatically a bad test.** If the expected value matches the AC, the
   code is wrong. Keep the test, make the smallest fix in `booking.ts` and record it. If the
   expected value contradicts the AC, the test is wrong. Never change a correct expectation to
   match buggy code.
3. Send the deck's improvement prompt with the actual output from step 1 below it. Paste the
   prompt as sent and the answer into §6.2:

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.
```

4. Apply what you accept from the answer and your own review from Part 4, so that the final suite
   follows every rule above. Run it until it is green. Commit: `week-07: improved suite`.

### Part 6 — Task 6: deliberate defects (~15 min, at home)

You need a reviewed, **passing** suite first. Then try each change below **one at a time** in
`booking.ts`. Leave the tests unchanged, run, write down which test failed, then **restore**
the code (`git checkout -- app/src/booking.ts`). Never commit a defect.

| Trial | Intentional change | Test that should fail |
| --- | --- | --- |
| M1 | Reject duration `>= 120` instead of `> 120` | T06: exactly 120 is allowed |
| M2 | Treat touching endpoints as an overlap | T01 or T08: touching is allowed |
| M3 | Remove the blocked-room rejection | T13: blocked room is rejected |

A relevant **assertion failure** counts as detection. A syntax or import error does not. If a
defect **survives**, inspect the test and the import path, improve the suite, and try again. Record
it honestly in the §7 table, because a survivor you explain is a finding. Paste each run, at least
the failing names and the `Tests` line, into §7.

After the last trial, restore the code and run the full suite again. **That** run goes in §6.3.

### Part 7 — Task 7: manual UI checks (~10 min, at home)

Some things no unit test here can see. Open the page in a browser with `now = 09:00` and the
`10:00–11:00` booking, and do the five checks in §8 of the worksheet (deck). Save one screenshot per
check: `evidence/ui-1.png` … `ui-5.png`. Take **ui-4 at phone width**: open the page in its own
tab, press F12, switch on the device toolbar, pick a phone (about 375 px), and use the toolbar's
"capture screenshot". The result is portrait.

If your page cannot set the current time or block a room, the check is **Not testable**. Write
that down, because it is a real finding about the page.

Commit: `week-07: mutants and UI checks`.

### Part 8 — Report, declaration, submit (~15 min, at home)

1. Fill in §9.2 (first suite against improved suite, the deck's table) and §9.3, and write the
   conclusion in §10 (120–180 words).
2. From inside `week-07/`, run the checker: `python tests/check_suite.py`. Every FAIL or ERROR you
   keep goes in §9.1 with the reason.
3. Fill in `AI_USAGE.md`.
4. Commit everything, then note the hash with `git rev-parse --short HEAD`.
5. Fill in `submission.yml` (§8 below), run the validator, commit, push, and open the PR (§9).

---

## 6. The test plan

**Default fixture:** `now = 540` (09:00), `blocked = false`, `bookings = [{ start: 600, end: 660 }]`
(10:00–11:00). Use fresh data in every test. Change only what the row says.

| ID | Candidate start–end / changed input | Expected | Requirement |
| --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 |
| T02 | 540–570 (starts now) | false | AC1 |
| T03 | 720–720 (zero duration) | false | AC1 |
| T04 | 750–720 (reversed) | false | AC1 |
| T05 | 1380–1441 (past day end) | false | AC1 |
| T06 | 720–840 (120 minutes) | true | AC2 |
| T07 | 720–841 (121 minutes) | false | AC2 |
| T08 | 570–600 (touching before) | true | AC4 |
| T09 | 630–690 (partial overlap) | false | AC4 |
| T10 | 570–690 (contains booking) | false | AC4 |
| T11 | 615–645 (inside booking) | false | AC4 |
| T12 | 600–660 (identical interval) | false | AC4 |
| T13 | 660–720, blocked = true | false | AC3 |
| T14 | 630–690, bookings = [] | true | AC4 |
| AC5 | an Available request; the bookings after the call equal the bookings before | true, data unchanged | AC5 |
| X1, X2 | yours: a boundary or a state T01–T14 do not reach | yours, from an AC | yours |

T01–T14 are the deck's plan, unchanged. **The Expected column comes from AC1–AC4, never from the
code.** The checker compares your tests' expected values with this table. A test you "corrected"
to match the code is a FAIL.

T05 cannot be typed into a time input, but `canBook` receives numbers, so it can be tested.
That is exactly why a unit test and a UI check are different levels.

---

## 7. Checking your work

### Verdicts

```
PASS   the check found what it was looking for
FAIL   the content is there but wrong, or not enough of it
ERROR  it could not check: a file, a folder or a section is missing
```

From inside `week-07/`:

```text
python tests/check_suite.py
```

It runs 33 checks:

| Checks | What they look at |
| --- | --- |
| **A1–A5** | `app/`: the project is there (A1); `booking.ts` / `.js` exports `canBook` (A2); a page file imports it from the booking module and calls it (A3); no `node_modules/`, no `.env`, under 5 MB (A4); `vitest` is in `package.json` (A5). |
| **S1–S10** | Your **final** suite beside the module: it imports `vitest` and the real `./booking` (S1); nothing is mocked, skipped, focused or table-driven (S2); 17 tests or more (S3); T01–T14 each named (S4), each asserting the exact expected decision (S5) on the plan's input (S6); the AC5 comparison on an Available call (S7); X1 and X2 (S8); no clock, no random (S9); and `suites/first/` kept and different from the final (S10). |
| **R1–R3** | §6.1 holds a real first run (R1). §6.3 holds the final run: nothing failed, and **its test count equals the tests in your committed files** (R2). The Vitest version is recorded and agrees with the run (R3). |
| **M1–M4** | §7: each mutant is Detected, with the IDs of tests that exist in your final suite, or Survived, with an explanation (M1–M3); three runs are pasted (M4). |
| **U1–U3** | Five different screenshots `ui-1` … `ui-5` (U1), `ui-4` in portrait (U2), and the §8 table observed and judged (U3). |
| **L1–L8** | The worksheet: setup (L1), the extraction (L2), a reason for every case (L3), the generation prompt as sent (its fixed sentences are checked, and `[our test framework]` must be replaced) and the answer (L4), two review decisions (L5), failures diagnosed and the improvement prompt as sent (L6), the comparison (L7), the conclusion (L8). |

**The checker never runs your tests.** It reads your test file and your pasted output, and checks
that the two agree. The grader can run your suite: a §6.3 output that the committed suite cannot
produce costs the whole *Evidence and honesty* criterion.

The first run on the untouched folder gives `0 PASS · 16 FAIL · 17 ERROR`. That is the intended
start.

---

## 8. The declaration — `submission.yml`

Facts only. From inside `week-07/`:

```text
python tests/validate_submission.py
```

Three things decide marks:

- **`checker.commit` is the commit you ran the checker at.** Normally that is the one just before
  the commit that adds the declaration. It must be a commit on your `week-07` branch.
- **Your numbers are re-run at the last commit of your pull request.** We run `check_suite.py`
  there ourselves. Numbers that match are settled automatically. Numbers that do not match cost the
  whole *Evidence and honesty* criterion. If you change anything after your last checker run, run
  it again and update `submission.yml`.
- **A FAIL you report costs you nothing extra.** If your page cannot be shown at phone width
  without breaking, write `Fail` in U4, list what fails in `known_fails`, and say why in §9.1.
  Hiding it is what costs.

---

## 9. Submit

1. Push the branch: `git push -u origin week-07`.
2. Open a Pull Request `week-07 → main` in your own repository. Title: `Week 07 — Testing
   AI-Generated Code`. Write the description in the fixed shape from `SETUP.md` §4.
3. **Leave the PR open. Do not merge it.**
4. In the Teams assignment *Practice #07*: **+ Add work → Link → paste the pull request URL.**

The practice deck asks you to email screenshots to the main lecturer. **That does not apply to our
groups.** The PR link in Teams is the only submission. It already contains everything the email
would have: the project with runnable tests, the first and improved suites, the prompts, the review
decisions, the real output, the mutation log, the UI evidence, the comparison and one remaining
limitation.

**Deadline:** Friday 6 November 2026, 23:59 (Almaty). Late submissions follow the course
policy. The Teams assignment closes on Sunday 15 November 2026, 23:59.

---

## 10. Grading — 1 point, 4 × 0.25

| Criterion | 0.25 when … |
| --- | --- |
| **Test plan and suite** | `canBook` is extracted and the page calls it; §3 gives a reason for every case and two justified cases of your own; the final suite covers T01–T14, AC5, X1 and X2 with exact decisions on the plan's inputs, imports the real function, mocks nothing and reads no clock. |
| **Runs and mutants** | The first and final runs in §6 are real and unedited; every failure is diagnosed as a test repair or an implementation fix; all three mutants were tried, with each detection named or each survivor explained; the five UI checks were done and photographed. |
| **Review decisions** | `suites/first/` holds the assistant's suite as generated; §5 has two or more decisions, each with an AC; both of the deck's prompts were sent as written; no correct expectation was changed to match the code; §9.2 compares the first and improved suites honestly. |
| **Evidence and honesty** | §10 and §9 are your own; `AI_USAGE.md` is complete; `submission.yml` passes the validator and its numbers match the re-run; the PR is open with 3 or more meaningful commits, the baseline commit before the extraction. |

**A FAIL you report and explain costs you nothing. One you hide costs the whole criterion.**

**Not accepted:** a suite that mocks `canBook` or imports a copy of it · an expected value changed
to match the code · `suites/first/` edited or written after the review · pasted output that the
committed suite cannot produce, or no output at all ("all tests passed") · a defect committed
instead of restored · `node_modules/` or a `.env` committed · findings that name no test, no AC
and no defect ("the AI tests were good") · a merged PR, a repo link, or an emailed submission.

---

## 11. FAQ

**My project is JavaScript, not TypeScript.** Use `booking.js` and `booking.test.js`. Everything
else is the same.

**Bolt put the logic in `App.tsx` and it returns a message, not a boolean.** Keep the message in
the page. `canBook` only answers true or false, and the page can still decide which message to
show. The page must call `canBook` for the decision itself.

**My Week 06 page has no current-time input, so `now` is the real clock.** Then the page reads
`Date.now()` or `new Date()` and passes it in. That is fine for the page. In `canBook` and in the
tests, `now` is a number you pass. Write in §8 that U1–U3 with `now = 09:00` are Not testable,
or add a current-time input to the page as a small change, logged in §2.

**The first run failed on a test that I think is right.** Then the code is wrong. This is the
deck's "keep a valid failing test when it reveals a real defect". Make the smallest fix in
`booking.ts`, mark it *implementation fix* in §6.1, and check the page again.

**The assistant changed a test to make it pass.** Look at whether the expected value still matches
the plan. If it does not, reject the change in §5. That is exactly what this lab is about.

**A mutant survived.** Say why in §7. Maybe your T06 used 721–841, or your touching test was
missing. Then add or fix the test and try the mutant again. You can record both attempts.

**Can I use `describe` blocks and a helper like `check(660, 720)`?** Yes. The checker finds the
numbers of each case in its test, wherever you put them. It needs the ID in the test's title and
an exact `.toBe(true)` or `.toBe(false)`.

**`npm install` is slow or fails in the lab.** Use the Bolt terminal or a Codespace, as in §4.
Only `app/` with its source files is committed. `node_modules/` never is.

**Where does the grader run my files?** The checker reads them and runs nothing. The grader can run
your suite with `npx vitest run` in `app/`, and that is why §6.3 must be the output of the suite
you committed.
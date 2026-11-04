# Week 07 — Lab report

**Name:** Tomiris Erzhankyzy
**Group:** not provided
**Date:** 4 November 2026

---

## 1. Setup

| | |
| --- | --- |
| Project I continue (week-06 or starter) | starter - no Week 06 project/branch was available in the inspected repository |
| Bolt project link (or not shared) | not-shared - the provided starter was used |
| Assistant that generated the tests (tool) | ChatGPT |
| Exact model (with its version, or not displayed) | GPT-6 |
| Where I ran the tests | GitHub Actions hosted Ubuntu runner, Node.js 22.23.4 |
| Vitest version (the RUN v… line) | 3.2.7 |
| Test command | First: npx vitest run --root .. suites/first/booking.test.ts; final: npm test |

## 2. Task 1 — baseline and the booking function

**Before editing:** where did the booking decision live in the project you started from?

| | |
| --- | --- |
| File and function | app/src/App.tsx, inside check() |
| Its inputs | start and end converted to minutes, current time now, blocked flag, and selected room.bookings |
| What it returned | Boolean decision stored in ok |
| How the page used it | check() calculated ok and called setResult(ok), which rendered Available or Unavailable |

**What I changed to extract canBook.**

The starter originally kept the booking decision inside check() in App.tsx. I moved the interval bounds check, start-after-now check, 120-minute duration limit, blocked-room rejection, and overlap loop into the exported canBook function in app/src/booking.ts. The page now imports canBook from ./booking and passes start, end, now, blocked, and the selected room's bookings. The HH:MM conversion, required-field checks, validation message, and result rendering remain in App.tsx. The overlap comparison remains strict (< and >), so intervals that only touch at an endpoint are still allowed. This is an extraction of the same decision, not an intentional change to the booking rules.

## 3. Task 2 — the test plan

Default fixture: now = 540, blocked = false, bookings = [{ start: 600, end: 660 }], fresh for every test.

| ID | Candidate / changed input | Expected | AC | Reason (in my words) |
| --- | --- | --- | --- | --- |
| T01 | 660–720 (touching after) | true | AC4 | The existing interval ends at 660, and the candidate begins at 660; half-open intervals touch but do not overlap. |
| T02 | 540–570 (starts now) | false | AC1 | AC1 requires the start to be later than now, not equal to it. |
| T03 | 720–720 (zero duration) | false | AC1 | Start and end are equal, so the interval has no positive duration. |
| T04 | 750–720 (reversed) | false | AC1 | The end is earlier than the start, violating start < end. |
| T05 | 1380–1441 (past day end) | false | AC1 | 1441 is beyond the maximum allowed end value of 1440. |
| T06 | 720–840 (120 minutes) | true | AC2 | The duration is exactly 120 minutes; AC2 rejects only durations longer than 120. |
| T07 | 720–841 (121 minutes) | false | AC2 | 841 minus 720 is 121 minutes, which is longer than the allowed limit. |
| T08 | 570–600 (touching before) | true | AC4 | The candidate ends at 600, exactly where the existing booking begins, so there is no shared time. |
| T09 | 630–690 (partial overlap) | false | AC4 | The candidate overlaps the existing booking from 630 through 660. |
| T10 | 570–690 (contains booking) | false | AC4 | The candidate covers the whole existing 600–660 booking, so the intervals overlap. |
| T11 | 615–645 (inside booking) | false | AC4 | The candidate is entirely inside the existing 600–660 booking. |
| T12 | 600–660 (identical interval) | false | AC4 | The candidate and existing booking occupy exactly the same interval. |
| T13 | 660–720, blocked = true | false | AC3 | Even though the time interval is free, a blocked room cannot be booked. |
| T14 | 630–690, bookings = [] | true | AC4 | With no existing bookings, there is no interval to overlap. |
| AC5 | Available request; compare bookings before and after | true, data unchanged | AC5 | The check must return Available and leave the original bookings data exactly as it was. |
| X1 | 1320–1440 (ends exactly at 24:00) | true | AC1, AC2 | 1440 is the permitted upper boundary, and this interval is exactly 120 minutes long. |
| X2 | 660–780 with bookings 600–660 and 780–840 | true | AC4 | The candidate touches the end of the first booking and the start of the second, but shares no time with either. |

## 4. Task 3 — the generation prompt and the first suite

**Prompt used (the deck prompt with Vitest and the case plan):**

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

Case table:
T01 660-720 => true (AC4)
T02 540-570 => false (AC1)
T03 720-720 => false (AC1)
T04 750-720 => false (AC1)
T05 1380-1441 => false (AC1)
T06 720-840 => true (AC2)
T07 720-841 => false (AC2)
T08 570-600 => true (AC4)
T09 630-690 => false (AC4)
T10 570-690 => false (AC4)
T11 615-645 => false (AC4)
T12 600-660 => false (AC4)
T13 660-720 with blocked=true => false (AC3)
T14 630-690 with bookings=[] => true (AC4)
AC5: Available request; bookings unchanged.
X1 1320-1440 => true (AC1, AC2)
X2 660-780 with bookings 600-660 and 780-840 => true (AC4)
Default fixture: now=540, blocked=false, bookings=[{start:600,end:660}].
```

**Assistant answer:**

```text
Test file: suites/first/booking.test.ts
Run command: npx vitest run --root .. suites/first/booking.test.ts
Final suite location: app/src/booking.test.ts
AC mapping: T01, T08-T12 and T14 and X2 cover AC4; T02-T05 and X1 cover AC1; T06-T07 cover AC2; T13 covers AC3; AC5 compares bookings before and after an Available call.
Unclear requirement flagged: the handout does not define the result for an invalid existing booking. The function's actual behavior must be called and declared in submission.yml.
The first suite was retained in suites/first/booking.test.ts. Its AC5 snapshot was later strengthened in the improved suite.
```

The first suite was saved before changes. The improved suite is a separate file beside booking.ts.

## 5. Task 4 — review of the first suite

| # | Test or part of the suite | What is weak or wrong | Decision: accept / revise / reject | AC or reason |
| --- | --- | --- | --- | --- |
| 1 | T01-T14 | The tests use the real canBook import and exact boolean expectations based on the case plan. | accept | AC1-AC4 define each expected decision; exact assertions are stronger than checking only that no exception occurred. |
| 2 | AC5 in first suite | A shallow array copy would still share references to nested booking objects and could miss an in-place object mutation. | revise | AC5 requires existing booking data to remain unchanged; the final suite uses structuredClone to make an independent snapshot. |
| 3 | X2 | The extra case checks a free interval that touches two different bookings. | accept | AC4 allows touching endpoints; this reaches two boundaries in one scenario without overlap. |

## 6. Task 5 — running, diagnosing, improving

### 6.1 The first run

Real GitHub Actions Vitest output (Vitest 3.2.7):

```text
RUN v3.2.7 /home/runner/work/SE-Practice-Course/SE-Practice-Course/week-07
✓ suites/first/booking.test.ts (17 tests)
Test Files 1 passed (1)
Tests 17 passed (17)
```

**Each failure, diagnosed:**

| Failing test | Observed failure | First check | Test repair or implementation fix? | Action taken |
| --- | --- | --- | --- | --- |
| none | The first suite completed with 17 passed and 0 failed. | Confirmed the run selected suites/first/booking.test.ts and imported the real booking module. | No repair required for the first run. | Kept the original suite unchanged and reviewed its AC5 snapshot separately. |

### 6.2 The improvement prompt

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

Actual first-run output:
RUN v3.2.7
Test Files 1 passed (1)
Tests 17 passed (17)
```

**Review answer and action taken:**

The expected decisions were retained because they follow AC1–AC4. No implementation failure appeared in the first run. The concrete improvement was the AC5 snapshot: the first suite used a shallow array copy, while the final suite uses structuredClone(f.bookings) before calling canBook and compares the original bookings afterwards. The improved suite still has one individually named test for every T01-T14 case, plus AC5, X1 and X2. The tests import the real ./booking module, use a fixed numeric now value, and do not mock the function.

### 6.3 The final run

Real GitHub Actions output of the committed final suite:

```text
RUN v3.2.7 /home/runner/work/SE-Practice-Course/SE-Practice-Course/week-07/app
✓ src/booking.test.ts (17 tests)
Test Files 1 passed (1)
Tests 17 passed (17)
```

The TypeScript production build also completed successfully with Vite 5.4.21.

## 7. Task 6 — deliberate defects

| Trial | Intentional change | Detected / Survived | Failing test ID(s) | If it survived: why, and what you added |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >= 120 instead of > 120 | Detected | T06, X1, X2 | Not applicable - the exact-120-minute cases failed as expected. |
| M2 | Treat touching endpoints as an overlap | Detected | T01, T08, AC5, X2 | Not applicable - the touching-endpoint cases failed as expected. |
| M3 | Remove the blocked-room rejection | Detected | T13 | Not applicable - the blocked-room case failed as expected. |

**Real mutant run summaries (Vitest 3.2.7):**

```text
RUN v3.2.7
M1: T06 AC2: exactly 120 minutes; X1 AC1: end exactly at 24:00; X2 AC4: free interval touches two bookings
Tests 3 failed | 14 passed (17)
M1: DETECTED
```

```text
RUN v3.2.7
M2: T01 AC4: touching after; T08 AC4: touching before; AC5: available call preserves bookings; X2 AC4: free interval touches two bookings
Tests 4 failed | 13 passed (17)
M2: DETECTED
```

```text
RUN v3.2.7
M3: T13 AC3: blocked room
Tests 1 failed | 16 passed (17)
M3: DETECTED
```

The mutation runner restored the original booking.ts after every trial in a finally block. The subsequent final suite run passed all 17 tests.

## 8. Task 7 — manual UI checks

These checks still require a person to interact with the page in a browser. They were not performed by the GitHub Actions unit-test runner. No manual screenshots are claimed yet.

| # | Action | Expected observation | AC | What I observed | Pass / Fail / Not testable |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available, with the fixed sample booking | AC5 | Not performed yet; browser interaction and screenshot still required. | Not testable |
| U2 | Enable blocked, then check again | Unavailable replaces the earlier result | AC3, AC5 | Not performed yet; browser interaction and screenshot still required. | Not testable |
| U3 | Clear a required input and submit | Understandable validation feedback | AC6 | Not performed yet; browser interaction and screenshot still required. | Not testable |
| U4 | Use a narrow (phone) width | Controls and result remain usable | AC6 | Not performed yet; phone-width browser screenshot still required. | Not testable |
| U5 | Repeat the checks on the same data | Existing bookings remain unchanged | AC5 | Not performed yet; browser interaction and screenshot still required. | Not testable |

## 9. Comparison and what still fails

### 9.1 Checks I am keeping as FAIL or ERROR

| Check | Why it stays |
| --- | --- |
| U1 | The five required manual browser screenshots have not yet been captured; no screenshot evidence is being invented. |
| U2 | The required ui-4 portrait screenshot at approximately 375 px has not yet been captured. |

### 9.2 Original and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | 17 executed / 17 passed / 0 failed | 17 executed / 17 passed / 0 failed |
| Requirements with meaningful tests (AC IDs and gaps) | AC1-AC4, AC5, X1 and X2; exact boolean expectations and fixed time | AC1-AC4, AC5, X1 and X2; AC5 now takes a deep snapshot |
| Selected mutants detected | T06 detects M1, T01/T08 detect M2, T13 detects M3 | M1, M2 and M3 all detected |
| Accepted / revised / rejected tests | 2 accepted, 1 revised | AC5 revised; all expected decisions retained |
| Remaining limitations | Shallow AC5 snapshot; no manual UI evidence | Manual UI interaction and five screenshots still outstanding |

### 9.3 What no AC decides

I called canBook with request 660-720 and bookings=[{start:700,end:650}]. It returns true: the overlap check is start < booking.end && end > booking.start, which becomes 660 < 650 && 720 > 700, so the first comparison is false. None of AC1-AC6 defines behavior for an invalid existing booking. I therefore record the observed behavior as returns-true, not as a new requirement.

## 10. Conclusion (120–180 words)

The first suite covered the fourteen planned cases, but its AC5 check used a shallow copy of the bookings array. That could miss a mutation inside an existing booking object because the copied array would still point to the same object. The final suite uses structuredClone for an independent snapshot. Both the first and improved suites passed all 17 tests. The mutation trials showed that the suite detects three deliberate defects: rejecting exactly 120 minutes, treating touching endpoints as overlaps, and ignoring a blocked room. A green unit-test run proves only that the tested decisions match their expected values for these inputs. It does not prove that the page is usable at phone width or that validation messages are clear. The remaining limitation is the manual UI evidence: the five browser checks and portrait screenshot have not yet been performed. I need to complete those checks before treating the submission as fully verified.

**Student action required:** rewrite this conclusion in your own words before final grading; the course handout explicitly asks for the student's own explanation.

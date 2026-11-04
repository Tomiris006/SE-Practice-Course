# Week 07 — Lab report

**Name:** Tomiris Erzhankyzy
**Group:** not supplied
**Date:** 4 November 2026

## 1. Setup

| | |
| --- | --- |
| Project I continue | starter (provided starter; no Week 06 branch/project was present in the inspected repository) |
| Bolt project link | not-shared — starter used |
| Assistant that generated the tests | ChatGPT |
| Exact model | GPT-6 |
| Where tests were run | Local Node.js 22 environment; Vitest install attempted but npm registry DNS failed |
| Vitest version | not obtained — runner did not start |
| Test command | `npx vitest run` (blocked before execution) |

## 2. Task 1 — baseline and the booking function

| | |
| --- | --- |
| File and function before extraction | `app/src/App.tsx`, inside `check()` |
| Inputs | start/end/current time converted to minutes, blocked flag, selected room bookings |
| Return | boolean |
| Page use | `check()` evaluated rules and stored result using `setResult(ok)` |

The starter originally kept the availability decision inside `check()` in `App.tsx`. I moved the same interval validation, current-time check, 120-minute limit, blocked-room rejection and overlap loop into exported `canBook` in `app/src/booking.ts`. The page imports `canBook` from `./booking` and passes numeric minutes, the blocked flag and selected room bookings. Time conversion, missing-field validation and visible feedback remain in the page. I retained the original comparisons, including strict overlap comparisons, so touching endpoints remain allowed. The extraction itself was intended not to change the booking decision.

## 3. Task 2 — the test plan

Default fixture: `now=540`, `blocked=false`, `bookings=[{start:600,end:660}]`.

| ID | Candidate / changed input | Expected | AC | Reason |
| --- | --- | --- | --- | --- |
| T01 | 660–720 touching after | true | AC4 | Existing booking ends at 660; candidate starts at 660, so they touch but do not overlap. |
| T02 | 540–570 starts now | false | AC1 | Start equals now; AC1 requires a later start. |
| T03 | 720–720 zero duration | false | AC1 | Start equals end; interval is not positive. |
| T04 | 750–720 reversed | false | AC1 | End is earlier than start. |
| T05 | 1380–1441 past day end | false | AC1 | End exceeds 1440. |
| T06 | 720–840 exactly 120 minutes | true | AC2 | AC2 rejects durations longer than 120, not exactly 120. |
| T07 | 720–841 121 minutes | false | AC2 | Duration exceeds 120. |
| T08 | 570–600 touching before | true | AC4 | Candidate ends exactly when existing booking starts. |
| T09 | 630–690 partial overlap | false | AC4 | The intervals share 630–660. |
| T10 | 570–690 contains booking | false | AC4 | Candidate contains the full 600–660 booking. |
| T11 | 615–645 inside booking | false | AC4 | Candidate lies inside the existing booking. |
| T12 | 600–660 identical | false | AC4 | Candidate occupies the same interval. |
| T13 | 660–720, blocked=true | false | AC3 | Blocked room must reject the request. |
| T14 | 630–690, bookings=[] | true | AC4 | No existing booking overlaps the request. |
| AC5 | Available request; compare bookings before/after | true, unchanged | AC5 | Availability check must not mutate existing data. |
| X1 | 1320–1440 ends exactly at 24:00 | true | AC1, AC2 | End equals 1440 and duration is exactly 120 minutes. |
| X2 | 660–780 with bookings 600–660 and 780–840 | true | AC4 | Candidate touches both bookings but overlaps neither. |

## 4. Task 3 — generation prompt and first suite

Prompt used:

```text
Generate tests for the existing booking function using Vitest. Use AC1–AC6 and the reviewed case table below.

Import the real function used by the page. Keep its code unchanged. Use fixed time and fresh fixtures. Assert exact decisions and unchanged booking data.

Return the test file, run command, and AC mapping. Flag unclear requirements. We will run the tests ourselves.

[The complete case table from section 3 was supplied after this prompt.]
```

The first suite was saved as `suites/first/booking.test.ts`; it has 17 named cases and was retained separately from the improved suite. Run command requested: `npx vitest run`. AC mapping: T01/T08–T12/T14/X2 → AC4; T02–T05/X1 → AC1; T06/T07 → AC2; T13 → AC3; AC5 → unchanged bookings. The handout leaves malformed existing-booking behavior unspecified.

## 5. Task 4 — review of the first suite

| # | Test / part | Weakness or finding | Decision | AC / reason |
| --- | --- | --- | --- | --- |
| 1 | T01–T14 | Separate cases import the real function and assert exact boolean decisions. | accept | AC1–AC4; expected values follow criteria. |
| 2 | AC5 in first suite | Shallow array copy retains references to nested booking objects. | revise | AC5 requires existing booking data unchanged; improved suite uses `structuredClone`. |
| 3 | X2 | Tests a free interval touching two separate bookings. | accept | AC4 allows touching endpoints. |

## 6. Task 5 — running, diagnosing, improving

### 6.1 First run

Vitest did not start. Dependency installation failed before the runner could execute:

```text
npm error code EAI_AGAIN
npm error syscall getaddrinfo
npm error errno EAI_AGAIN
npm error request to https://registry.npmjs.org/@types%2freact failed, reason: getaddrinfo EAI_AGAIN
```

No Vitest `RUN v…` line or `Tests` summary exists; no test assertion failure is claimed. Diagnosis: npm registry DNS/network access prevented dependency installation. This is an environment/setup issue, not a test repair or implementation fix.

### 6.2 Improvement prompt

```text
Review this test suite against AC1–AC6 and our case table. Identify incorrect expectations, weak assertions, duplicated cases, and missing boundaries.

For each proposed change, explain the requirement and the defect it could detect. Improve the tests without changing correct expectations to match buggy behavior.

Use the actual failure output below. Separate test repairs from implementation fixes.

Actual output: npm install could not resolve registry.npmjs.org (EAI_AGAIN); Vitest did not start, so there is no assertion output to analyze.
```

Improvement: retained all expected decisions because they follow the acceptance criteria. Replaced the AC5 shallow array snapshot in the final suite with `structuredClone(f.bookings)`, which also copies nested booking objects. No implementation correction based on a Vitest failure was made because Vitest did not run.

### 6.3 Final run

```text
NOT RUN — Vitest dependency installation was blocked by npm registry DNS resolution. No genuine final Vitest output is available.
```

## 7. Task 6 — deliberate defects

| Trial | Intentional change | Result | Expected detector | Evidence |
| --- | --- | --- | --- | --- |
| M1 | Reject duration >=120 | Not run | T06 | Vitest unavailable; no mutant result claimed. |
| M2 | Treat touching endpoints as overlap | Not run | T01 or T08 | Vitest unavailable; no mutant result claimed. |
| M3 | Remove blocked-room rejection | Not run | T13 | Vitest unavailable; no mutant result claimed. |

The mutation runner `tests/run_mutants.py` is included and restores the original source in a `finally` block. It must be run in an environment where dependencies install. The mutants have not been executed here.

## 8. Task 7 — manual UI checks

The page includes current-time and interval inputs, an end-of-day checkbox, a blocked-room checkbox and a visible result. Browser checks were not performed because Vite dependencies could not be installed. No UI screenshots are claimed.

| # | Action | Expected | AC | Observation | Result |
| --- | --- | --- | --- | --- | --- |
| U1 | Check 11:00–12:00, unblocked | Available | AC5 | Not performed; app not launched | Not testable |
| U2 | Enable blocked and check again | Unavailable | AC3, AC5 | Not performed; app not launched | Not testable |
| U3 | Clear required input and submit | Clear validation feedback | AC6 | Not performed; app not launched | Not testable |
| U4 | Narrow phone width | Usable controls and result | AC6 | Not performed; app not launched | Not testable |
| U5 | Repeat on same data | Existing bookings unchanged | AC5 | Not performed; app not launched | Not testable |

## 9. Comparison and what still fails

### 9.1 Checks kept as FAIL / ERROR

| Check | Why it stays |
| --- | --- |
| R1 | No genuine first Vitest run output. |
| R2 | No genuine final Vitest run output. |
| R3 | Vitest version unavailable because runner did not start. |
| M1 | Mutant not executed; T06 is expected detector only. |
| M2 | Mutant not executed; T01/T08 are expected detectors only. |
| M3 | Mutant not executed; T13 is expected detector only. |
| M4 | Three real mutant run outputs are unavailable. |
| U1 | Five browser screenshots were not captured. |
| U2 | Portrait phone-width screenshot is missing. |

### 9.2 First and improved suites

| Measure | First suite | Improved suite |
| --- | --- | --- |
| Executed / passed / failed | Vitest not run | Vitest not run |
| Requirements represented | T01–T14, AC5, X1, X2 | T01–T14, AC5, X1, X2 |
| Mutants detected | Not tested | Not tested; expected detectors T06, T01/T08, T13 |
| Review decisions | 2 accepted, 1 revised | AC5 assertion strengthened |
| Limitations | AC5 shallow copy; no Vitest execution | Vitest, mutation and manual UI evidence outstanding |

### 9.3 What no AC decides

With `bookings=[{start:700,end:650}]` and request 660–720, the current function returns true: the overlap expression `660 < 650 && 720 > 700` is false. No AC defines behavior for an invalid existing booking. Assumption: `returns-true`.

## 10. Conclusion (120–180 words)

The first suite covered the required booking cases, but its AC5 check used a shallow copy of the bookings array. That comparison could miss an in-place change to a booking object, because the saved array would still point to the same object. I revised the check to use structuredClone, while keeping the expected results tied to AC1–AC4 rather than changing them to match the implementation. The test files include boundary cases for touching intervals, the exact 120-minute limit, the end of the day, and two existing bookings. A green test run would only show that the assertions pass for the cases executed; it would not prove that the page is usable on a phone or that every possible booking state is correct. This work is not yet fully verified: Vitest could not be installed because the npm registry could not be resolved, the three mutants were not run, and the manual UI screenshots remain outstanding.

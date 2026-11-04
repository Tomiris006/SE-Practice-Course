# AI Usage Disclosure — Week 07

AI-use level D applies. ChatGPT (GPT-6) assisted with the implementation, test planning, initial suite generation, review, test-run orchestration, mutation-runner script, and report drafting.

| Tool | Exact model | Used for | Files touched |
| --- | --- | --- | --- |
| ChatGPT | GPT-6 | Initial Vitest suite and case mapping | `suites/first/booking.test.ts` |
| ChatGPT | GPT-6 | Extracting canBook and integrating the page | `app/src/booking.ts`, `app/src/App.tsx` |
| ChatGPT | GPT-6 | Improved tests and mutation runner | `app/src/booking.test.ts`, `tests/run_mutants.py` |
| ChatGPT | GPT-6 | Test plan, review, and report drafting | `lab-report.md`, `submission.yml`, `AI_USAGE.md` |

The first suite is retained separately from the improved suite. The first suite and final suite were both executed by GitHub Actions using Vitest 3.2.7. The production build passed. The mutation runner intentionally changed one condition at a time and restored the original booking.ts in a finally block; all three mutants were detected.

AI assistance was used for the code and report. The student must review the code, understand each test, and rewrite the conclusion in their own words as required by the handout. The five manual UI checks and screenshots remain outstanding and are disclosed in lab-report.md.

Signed: Tomiris Erzhankyzy
Date: 4 November 2026

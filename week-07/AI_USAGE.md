# AI Usage Disclosure — Week 07

AI use level D applies. ChatGPT (GPT-6) assisted with implementation, test planning, suite generation/review and report drafting.

| Tool | Exact model | Used for | Files touched |
| --- | --- | --- | --- |
| ChatGPT | GPT-6 | First Vitest suite generation | `suites/first/booking.test.ts` |
| ChatGPT | GPT-6 | Extracting `canBook`, page integration, improved suite | `app/src/booking.ts`, `app/src/App.tsx`, `app/package.json`, `app/src/booking.test.ts` |
| ChatGPT | GPT-6 | Test plan and report draft | `lab-report.md`, `submission.yml`, `AI_USAGE.md` |

Assistant used to extract canBook: yes. The original decision conditions were moved from App.tsx to booking.ts. A Vitest behavior-preservation run is still pending because npm install failed with EAI_AGAIN.

Another assistant used: no.

First suite kept as generated: yes.
Every terminal output shown in the report is real and unedited: yes; the npm install error is real. No Vitest output is claimed.
I can explain every test without the assistant: student must personally confirm before submission.
Anything accepted without full understanding: structuredClone makes an independent deep copy of the bookings fixture; student should confirm understanding.

Signed: Tomiris Erzhankyzy (confirm before submission)
Date: 4 November 2026

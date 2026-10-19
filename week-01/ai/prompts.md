# Part 2

## Answer the questions

### How should marks be entered into the app?
**Answer:** Type them in manually (Enter each student's mark one by one in a form)
### Who is this tool for?
**Answer:** A school or institution (Multiple teachers each manage their own class results)


## Testing program

**A valid mark is a number from 0 to 100 inclusive.**
All entered marks are valid, because every mark is between 0 and 100

**A mark passes if it is ≥ 50 (KBTU grade D starts at 50%)**
There is only one issue, from the one propmt that program run, doesn't match to the pass rule.
if the pass rule is mark ≥ 50, then 47 should be Fail (D), not C.

**Pass rate = passing marks ÷ valid marks × 100**
Totally correct. There are 7 passes, so 7 ÷ 9 × 100 = 77.8%

**If there are no valid marks, print a clear message instead of statistics — no crash, no division by zero**
It doesn't print no valid marks, but instead of that we can't put any valuable strings in the input mark.  

## Fix one defect with a follow-up prompt.
It doesn't work, I tried to fix all pass mark statement and wrote 2 prompts for it but it didn't work.
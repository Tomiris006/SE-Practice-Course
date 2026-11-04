marks = [[40, 60, 80], 50]

valid_marks = []

for mark in marks:
    if isinstance(mark, (int, float)) and 0 <= mark <= 100:
        valid_marks.append(mark)

if len(valid_marks) == 0:
    print("No valid marks found.")
else:
    average = sum(valid_marks) / len(valid_marks)
    highest = max(valid_marks)
    lowest = min(valid_marks)

    passed = 0

    for mark in valid_marks:
        if mark >= 50:
            passed += 1

    pass_rate = (passed / len(valid_marks)) * 100

    print("Number of valid marks:", len(valid_marks))
    print(f"Average: {average:.2f}")
    print("Highest:", highest)
    print("Lowest:", lowest)
    print(f"Pass rate: {pass_rate:.1f}%")
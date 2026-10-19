marks = [88, 47, -5, 101, "abc", 73, 50, 100]

valid_marks = []

for mark in marks:
    if type(mark) == int or type(mark) == float:
        if 0 <= mark <= 100:
            valid_marks.append(mark)

if len(valid_marks) == 0:
    print("No valid marks.")

else:
    count = len(valid_marks)
    average = sum(valid_marks) / count
    highest = max(valid_marks)
    lowest = min(valid_marks)

    passes = 0

    for mark in valid_marks:
        if mark >= 50:
            passes += 1

    pass_rate = passes / count * 100

    print("Number of valid marks:", count)
    print(f"Average: {average:.2f}")
    print("Highest:", highest)
    print("Lowest:", lowest)
    print(f"Pass rate: {pass_rate:.1f}%")
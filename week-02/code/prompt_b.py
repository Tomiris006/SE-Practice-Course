def analyze_marks(marks, pass_mark=50):
    if not marks:
        raise ValueError("Marks list cannot be empty.")

    if not isinstance(pass_mark, (int, float)) or isinstance(pass_mark, bool):
        raise ValueError("Pass mark must be numeric.")

    if not 0 <= pass_mark <= 100:
        raise ValueError("Pass mark must be between 0 and 100.")

    for mark in marks:
        if not isinstance(mark, (int, float)) or isinstance(mark, bool):
            raise ValueError("All marks must be numeric.")

        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    passed = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = (passed / len(marks)) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }


# Example
marks = [75, 88, 45, 100, 52]

result = analyze_marks(marks)
print(result)
def analyze_marks(marks, pass_mark=50):
    # Check for an empty list
    if not marks:
        raise ValueError("Marks list cannot be empty.")

    # Validate pass_mark
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("Pass mark must be numeric.")

    if pass_mark < 0 or pass_mark > 100:
        raise ValueError("Pass mark must be between 0 and 100.")

    # Validate all marks
    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("All marks must be numeric.")

        if mark < 0 or mark > 100:
            raise ValueError("Marks must be between 0 and 100.")

    # Calculate statistics
    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    passed = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = (passed / len(marks)) * 100

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": round(pass_rate, 2)
    }


# --------------------
# Tests
# --------------------

# Given example
result = analyze_marks([40, 60, 80], 50)
assert result == {
    "average": 60,
    "highest": 80,
    "lowest": 40,
    "pass_rate": 66.67
}

# 1. One mark
result = analyze_marks([75])
assert result == {
    "average": 75,
    "highest": 75,
    "lowest": 75,
    "pass_rate": 100.0
}

# 2. Decimal marks
result = analyze_marks([50.5, 70.5, 90.5])
assert result == {
    "average": 70.5,
    "highest": 90.5,
    "lowest": 50.5,
    "pass_rate": 100.0
}

# 3. Custom pass_mark
result = analyze_marks([40, 60, 80], 70)
assert result == {
    "average": 60,
    "highest": 80,
    "lowest": 40,
    "pass_rate": 33.33
}


# Helper for testing expected ValueErrors
def expect_value_error(func):
    try:
        func()
        assert False, "Expected ValueError"
    except ValueError:
        pass


# 4. Empty list
expect_value_error(lambda: analyze_marks([]))

# 5. Text value
expect_value_error(lambda: analyze_marks([40, "60", 80]))

# 6. Mark below 0
expect_value_error(lambda: analyze_marks([-1, 50, 80]))

# 7. Mark above 100
expect_value_error(lambda: analyze_marks([50, 80, 101]))


print("All tests passed.")
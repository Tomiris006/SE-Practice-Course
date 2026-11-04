def analyze_marks(marks, pass_mark=50):

    # Check for empty list
    if not marks:
        raise ValueError("Marks list cannot be empty.")

    # Validate pass_mark
    if isinstance(pass_mark, bool) or not isinstance(pass_mark, (int, float)):
        raise ValueError("Pass mark must be numeric.")

    if not 0 <= pass_mark <= 100:
        raise ValueError("Pass mark must be between 0 and 100.")

    # Validate marks
    for mark in marks:
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("All marks must be numeric.")

        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    # Calculate statistics
    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    passed = sum(1 for mark in marks if mark >= pass_mark)
    pass_rate = round((passed / len(marks)) * 100, 2)

    return {
        "average": average,
        "highest": highest,
        "lowest": lowest,
        "pass_rate": pass_rate
    }


# -----------------------------
# TEST CASES
# -----------------------------

# Test 1: Normal input
assert analyze_marks([40, 60, 80], 50) == {
    "average": 60,
    "highest": 80,
    "lowest": 40,
    "pass_rate": 66.67
}

# Test 2: Decimal marks
assert analyze_marks([49.5, 50], 50) == {
    "average": 49.75,
    "highest": 50,
    "lowest": 49.5,
    "pass_rate": 50.0
}

# Test 3: One mark
assert analyze_marks([100], 50) == {
    "average": 100,
    "highest": 100,
    "lowest": 100,
    "pass_rate": 100.0
}

# Test 4: Custom pass mark
assert analyze_marks([40, 60, 80], 70)["pass_rate"] == 33.33


# Helper function for testing errors
def check_error(marks):
    try:
        analyze_marks(marks)
    except ValueError:
        return True

    return False


# Test 5: Empty list
assert check_error([])

# Test 6: Text value
assert check_error([40, "60"])

# Test 7: Mark below 0
assert check_error([-1, 50, 80])

# Test 8: Mark above 100
assert check_error([50, 80, 101])

print("All tests passed!")
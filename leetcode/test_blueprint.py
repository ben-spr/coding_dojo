import pytest
from ambiguous_coordinates import Solution

SEPARATION_STRING = "==========================================================================="

TEST_DATA = [
    "(123)",
    "(101)",
    "(00011)",
    "(0000001)",
    "(00000011)",
]

EXPECTED_RESULTS = [
    [
        "(1, 23)",
        "(1, 2.3)",
        "(12, 3)",
        "(1.2, 3)",
    ],
    [
        "(1, 0.1)",
        "(10, 1)",
    ],
    [
        "(0, 0.011)",
        "(0.001, 1)",
    ],
    [
        "(0, 0.00001)",
    ],
    [
        "(0, 0.000011)",
        "(0.000001, 1)",
    ],
]

# @pytest.fixture
# def solution():
#     return Solution()

def test_ambiguous_coordinates():
    sol = Solution()
    for test_data, result_exp in zip(TEST_DATA, EXPECTED_RESULTS):
        result_actual = sol.ambiguousCoordinates(test_data)
        assert sorted(result_exp) == sorted(result_actual)

if __name__ == "__main__":
    sol = Solution()
    for test_data, result_exp in zip(TEST_DATA, EXPECTED_RESULTS):
        result_exp.sort()
        result_actual = sorted(sol.ambiguousCoordinates(test_data))
        print("\n" + SEPARATION_STRING)
        print(f"TEST ITERATION DONE!\nTest data: {test_data}\nExpected result: {result_exp}\nActual result: {result_actual}")
        print(SEPARATION_STRING + "\n")
        break

from enum import Enum
from time import perf_counter_ns

from advent_of_code_2023.day_01.step_2.solve_index import (
    calculate_calibration_digits as calculate_calibration_digits_index,
)
from advent_of_code_2023.day_01.step_2.solve_slice import (
    calculate_calibration_digits as calculate_calibration_digits_slice,
)


class Method(Enum):
    INDEX = "index"
    SLICE = "slice"


def _calculate_calibration_digits(line: str, method: Method) -> tuple[int, int]:
    match method:
        case Method.SLICE:
            return calculate_calibration_digits_slice(line)
        case Method.INDEX:
            return calculate_calibration_digits_index(line)


def _calculate_calibration_value(line: str, method: Method) -> int:
    left_digit, right_digit = _calculate_calibration_digits(line, method)

    return left_digit * 10 + right_digit


def solve(input: str, method_choice: str = "slice"):
    # Slice is faster
    method = Method(method_choice)

    now = perf_counter_ns()
    total = sum(
        _calculate_calibration_value(line, method) for line in input.splitlines()
    )
    print(perf_counter_ns() - now)

    return total


# Solution: 53894

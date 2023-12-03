from advent_of_code_2023.resources import read_resource

__DIGITS = "0123456789"


def calculate_calibration_value(line: str) -> int:
    first_value = next((int(d) for d in line if d in __DIGITS), 0)
    last_value = next((int(d) for d in reversed(line) if d in __DIGITS), 0)
    return first_value * 10 + last_value


def calculate_calibration_sum(input: str) -> int:
    return sum((calculate_calibration_value(line) for line in input.splitlines()))


def solve(resource: str):
    input = read_resource(resource)

    calibration_sum = calculate_calibration_sum(input)

    return calibration_sum


# Solution: 53651

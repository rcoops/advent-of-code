from collections.abc import Callable

from advent_of_code_2023.resources import read_resource

__DIGIT_NUMBER_MAPPINGS = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}
__TEXT_NUMBER_MAPPINGS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
} | __DIGIT_NUMBER_MAPPINGS
__NUMBER_MAPPINGS = __TEXT_NUMBER_MAPPINGS | __DIGIT_NUMBER_MAPPINGS
__ALL_NUMBER_KEYS = list(__NUMBER_MAPPINGS.keys())


def calculate_calibration_right_digit_slice(line: str) -> int:
    for i in range(len(line), -1, -1):
        slice_begin = max(0, i - 5)
        grp = line[slice_begin:i]
        length = len(grp)
        if length == 5 and __NUMBER_MAPPINGS.get(grp, False):
            return __NUMBER_MAPPINGS[grp]
        if length >= 4 and __NUMBER_MAPPINGS.get(grp[-4:], False):
            return __NUMBER_MAPPINGS[grp[-4:]]
        if length >= 3 and __NUMBER_MAPPINGS.get(grp[-3:], False):
            return __NUMBER_MAPPINGS[grp[-3:]]
        if __NUMBER_MAPPINGS.get(grp[-1], False):
            return __NUMBER_MAPPINGS[grp[-1]]
        # digit = next((d for d in __ALL_NUMBER_KEYS if d in grp), None)
        # if digit is not None:
        #    return __NUMBER_MAPPINGS[digit]
    return 0


def calculate_calibration_left_digit_slice(line: str) -> int:
    for i in range(0, len(line)):
        slice_end = min(len(line), i + 5)
        grp = line[i:slice_end]
        length = len(grp)
        if length == 5 and __NUMBER_MAPPINGS.get(grp, False):
            return __NUMBER_MAPPINGS[grp]
        if length >= 3 and __NUMBER_MAPPINGS.get(grp[:3], False):
            return __NUMBER_MAPPINGS[grp[:3]]
        if length >= 4 and __NUMBER_MAPPINGS.get(grp[:4], False):
            return __NUMBER_MAPPINGS[grp[:4]]
        if __NUMBER_MAPPINGS.get(grp[0], False):
            return __NUMBER_MAPPINGS[grp[0]]
    return 0


def safe_index(line: str, digit: str, func: Callable[[str, str], int]) -> int | None:
    try:
        return func(line, digit)
    except ValueError:
        return None


def calculate_calibration_digit(
    line: str,
    index_finder: Callable[[str, str], int],
    chooser: Callable[[tuple[int, ...]], int],
) -> int:
    indexes = tuple(safe_index(line, d, index_finder) for d in __ALL_NUMBER_KEYS)
    real_indexes = tuple(i for i in indexes if i is not None)

    return __NUMBER_MAPPINGS[__ALL_NUMBER_KEYS[indexes.index(chooser(real_indexes))]]


def calculate_calibration_for_line(line: str) -> int:
    left_digit = calculate_calibration_digit(line, lambda line, d: line.index(d), min)
    right_digit = calculate_calibration_digit(line, lambda line, d: line.rindex(d), max)

    return left_digit * 10 + right_digit


def calculate_calibrations(input: str) -> int:
    return sum(calculate_calibration_for_line(line) for line in input.splitlines())


def solve(resource: str):
    input = read_resource(resource)

    return calculate_calibrations(input)


# Solution: 53894

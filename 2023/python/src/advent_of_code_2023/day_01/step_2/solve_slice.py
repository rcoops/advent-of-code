from collections.abc import Callable, Sequence
from typing import TypeAlias

from advent_of_code_2023.day_01.step_2.constants import NUMBER_MAPPINGS, Digit

_DIGIT_PATTERN_LENGTHS = (5, 4, 3, 1)


GenerateRange: TypeAlias = Callable[[str, int], Sequence[int]]
SliceLine: TypeAlias = Callable[[str, int, int], str]


def _slice_line_right(line: str, current_start: int, pattern_length: int) -> str:
    slice_begin = max(0, current_start + pattern_length)
    return line[slice_begin:current_start]


def _gen_range_right(line: str, step: int) -> Sequence[int]:
    return range(len(line), -1, step)


def _slice_line_left(line: str, current_start: int, pattern_length: int) -> str:
    slice_end = min(len(line), current_start + pattern_length)
    return line[current_start:slice_end]


def _gen_range_left(line: str, step: int) -> Sequence[int]:
    return range(0, len(line), step)


def _get_functions_for_direction(digit: Digit) -> tuple[GenerateRange, SliceLine]:
    match digit:
        case Digit.LEFT:
            return _gen_range_left, _slice_line_left
        case Digit.RIGHT:
            return _gen_range_right, _slice_line_right


def _calculate_calibration_digit(line: str, direction: Digit) -> int:
    generate_range, generate_slice = _get_functions_for_direction(direction)

    for i in generate_range(line, direction.value):
        for j in _DIGIT_PATTERN_LENGTHS:
            slice = generate_slice(line, i, j * direction.value)
            if match_ := NUMBER_MAPPINGS.get(slice, False):
                return match_
    return 0


def calculate_calibration_digits(line: str) -> tuple[int, int]:
    left = _calculate_calibration_digit(line, Digit.LEFT)
    right = _calculate_calibration_digit(line, Digit.RIGHT)

    return left, right

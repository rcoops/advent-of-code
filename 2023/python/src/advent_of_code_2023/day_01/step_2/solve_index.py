from collections.abc import Callable

from advent_of_code_2023.day_01.step_2.constants import NUMBER_MAPPINGS

_ALL_NUMBER_KEYS = list(NUMBER_MAPPINGS.keys())


def _safe_index(line: str, digit: str, func: Callable[[str, str], int]) -> int | None:
    try:
        return func(line, digit)
    except ValueError:
        return None


def _find_index_right(line: str, digit: str) -> int:
    return line.rindex(digit)


def _find_index_left(line: str, digit: str) -> int:
    return line.index(digit)


def _calculate_calibration_digit(
    line: str,
    find_index: Callable[[str, str], int],
    chooser: Callable[[tuple[int, ...]], int],
) -> int:
    indexes = tuple(_safe_index(line, d, find_index) for d in _ALL_NUMBER_KEYS)
    real_indexes = tuple(i for i in indexes if i is not None)

    return NUMBER_MAPPINGS[_ALL_NUMBER_KEYS[indexes.index(chooser(real_indexes))]]


def calculate_calibration_digits(line: str) -> tuple[int, int]:
    left = _calculate_calibration_digit(line, _find_index_left, min)
    right = _calculate_calibration_digit(line, _find_index_right, max)

    return left, right

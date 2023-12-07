from dataclasses import dataclass
from typing import Callable

"""
each group of digits
what is its start & end index ()
467..114..
467 - 0, 2
is any index start - 1 -> end+1 a symbol on line number -1 -> line number +1

"""


_DIGITS = "0123456789"
_NON_SYMBOLS = f"{_DIGITS}.\n"


@dataclass
class EnginePart:
    value: int
    start_index: int
    end_index: int


def _is_any_index_a_symbol(indexes: tuple[int, ...], input: str) -> bool:
    return any(input[i] for i in indexes if input[i] not in _NON_SYMBOLS)


def _provide_calculate_bounded_index(
    max_input_index: int,
) -> Callable[[int], tuple[int, ...]]:
    def calculate_bounded_index(index: int) -> tuple[int, ...]:
        return () if index <= 0 or index >= max_input_index else (index,)

    return calculate_bounded_index


def _get_safe_range(begin: tuple[int, ...], end: tuple[int, ...]) -> tuple[int, ...]:
    if begin and end:
        return tuple(range(begin[0], end[0]))
    if begin:
        return begin
    return end if end else ()


def _get_indexes(
    part: EnginePart,
    line_length: int,
    calculate_bounded_index: Callable[[int], tuple[int, ...]],
) -> tuple[int, ...]:
    previous_line_begin = calculate_bounded_index(part.start_index - line_length - 1)
    previous_line_end = calculate_bounded_index(part.end_index - line_length + 1)
    same_line_before = calculate_bounded_index(part.start_index - 1)
    same_line_after = calculate_bounded_index(part.end_index)
    next_line_begin = calculate_bounded_index(part.start_index + line_length - 1)
    next_line_end = calculate_bounded_index(part.end_index + line_length + 1)
    return (
        *_get_safe_range(previous_line_begin, previous_line_end),
        *same_line_before,
        *same_line_after,
        *_get_safe_range(next_line_begin, next_line_end),
    )


def solve(input: str) -> int:
    line_length = input.index("\n") + 1
    max_input_index = len(input) - 1
    potential_part_index_code_pairs: list[tuple[int, str]] = []
    for i, c in enumerate(input):
        if c in _DIGITS:
            if i == 0 or input[i - 1] not in _DIGITS:
                potential_part_index_code_pairs.append((i, c))
            else:
                potential_part_index_code_pairs[-1] = (
                    potential_part_index_code_pairs[-1][0],
                    f"{potential_part_index_code_pairs[-1][1]}{c}",
                )
    potential_parts = [
        EnginePart(int(value), index, index + len(value))
        for index, value in potential_part_index_code_pairs
    ]

    calculate_bounded_index = _provide_calculate_bounded_index(max_input_index)
    index_tuples = [
        (part, _get_indexes(part, line_length, calculate_bounded_index))
        for part in potential_parts
    ]
    parts = (
        part for part, indexes in index_tuples if _is_any_index_a_symbol(indexes, input)
    )
    return sum(part.value for part in parts)

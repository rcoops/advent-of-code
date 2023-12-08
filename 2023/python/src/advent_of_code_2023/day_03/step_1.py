from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from typing import TypeAlias

IndexCodePair: TypeAlias = tuple[int, str]
IndexCodePairs: TypeAlias = list[IndexCodePair]
OptionalInt: TypeAlias = tuple[int, ...]


_DIGITS = "0123456789"
_NON_SYMBOLS = f"{_DIGITS}.\n"


@dataclass
class EnginePart:
    value: int
    start_index: int
    end_index: int
    symbol_search_indexes: tuple[int, ...]


def _is_any_index_a_symbol(indexes: OptionalInt, input: str) -> bool:
    return any(input[i] for i in indexes if input[i] not in _NON_SYMBOLS)


def _provide_calculate_bounded_index(
    max_input_index: int,
) -> Callable[[int], OptionalInt]:
    def calculate_bounded_index(index: int) -> tuple[int, ...]:
        return () if index <= 0 or index >= max_input_index else (index,)

    return calculate_bounded_index


def _provide_get_index_code_pairs(
    input: str
) -> Callable[[IndexCodePairs, IndexCodePair], IndexCodePairs]:
    def reduce_index_part_code_pairs(
        agg: IndexCodePairs,
        next: IndexCodePair,
    ) -> list[tuple[int, str]]:
        i, c = next
        if c not in _DIGITS:
            return agg
        if i == 0 or input[i - 1] not in _DIGITS:
            return [*agg, next]
        else:
            last = agg[-1]
            return [*agg[:-1], (last[0], f"{last[1]}{c}")]

    return reduce_index_part_code_pairs


def _provide_to_engine_part(
    line_length: int,
    calculate_bounded_index: Callable[[int], OptionalInt],
) -> Callable[[tuple[int, str]], EnginePart]:
    def to_engine_part(index_value_pair: tuple[int, str]) -> EnginePart:
        index, value_text = index_value_pair
        end_index = index + len(value_text)
        symbol_search_indexes = _get_symbol_search_indexes(
            index,
            end_index,
            line_length,
            calculate_bounded_index,
        )
        return EnginePart(int(value_text), index, end_index, symbol_search_indexes)

    return to_engine_part


def _get_safe_range(begin: OptionalInt, end: OptionalInt) -> OptionalInt:
    if begin and end:
        return tuple(range(begin[0], end[0]))
    if begin:
        return begin
    return end if end else ()


def _get_symbol_search_indexes(
    part_start_index: int,
    part_end_index: int,
    line_length: int,
    calculate_bounded_index: Callable[[int], OptionalInt],
) -> OptionalInt:
    previous_line_begin = calculate_bounded_index(part_start_index - line_length - 1)
    previous_line_end = calculate_bounded_index(part_end_index - line_length + 1)
    same_line_before = calculate_bounded_index(part_start_index - 1)
    same_line_after = calculate_bounded_index(part_end_index)
    next_line_begin = calculate_bounded_index(part_start_index + line_length - 1)
    next_line_end = calculate_bounded_index(part_end_index + line_length + 1)
    return (
        *_get_safe_range(previous_line_begin, previous_line_end),
        *same_line_before,
        *same_line_after,
        *_get_safe_range(next_line_begin, next_line_end),
    )


def solve(input: str) -> int:
    line_length = input.index("\n") + 1
    max_input_index = len(input) - 1
    get_index_code_pairs = _provide_get_index_code_pairs(input)
    calculate_bounded_index = _provide_calculate_bounded_index(max_input_index)
    to_engine_part = _provide_to_engine_part(line_length, calculate_bounded_index)

    index_potential_part_code_pairs = reduce(get_index_code_pairs, enumerate(input), [])
    potential_parts = list(map(to_engine_part, index_potential_part_code_pairs))

    parts = (
        part
        for part in potential_parts
        if _is_any_index_a_symbol(part.symbol_search_indexes, input)
    )

    return sum(part.value for part in parts)


# Solution 525911

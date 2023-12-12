from collections.abc import Callable
from dataclasses import dataclass
from functools import reduce
from typing import TypeAlias

IndexCodePair: TypeAlias = tuple[int, str]
IndexCodePairs: TypeAlias = list[IndexCodePair]
OptionalInt: TypeAlias = tuple[int, ...]


_DIGITS = "0123456789"


@dataclass
class EnginePart:
    part_number: int
    gear_indexes: list[int]


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


def _provide_to_gear_part_pairs(
    input: str,
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
        gear_indexes = [index for index in symbol_search_indexes if input[index] == "*"]

        return EnginePart(int(value_text), gear_indexes)

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


def __reduce_parts(
    gear_index_to_engine_part_value: dict[int, list[int]],
    next_part: EnginePart,
) -> dict[int, list[int]]:
    for gear_index in next_part.gear_indexes:
        if gear_index in gear_index_to_engine_part_value:
            gear_index_to_engine_part_value[gear_index].append(next_part.part_number)
        else:
            gear_index_to_engine_part_value[gear_index] = [next_part.part_number]
    return gear_index_to_engine_part_value


def solve(input: str) -> int:
    line_length = input.index("\n") + 1
    max_input_index = len(input) - 1
    get_index_code_pairs = _provide_get_index_code_pairs(input)
    calculate_bounded_index = _provide_calculate_bounded_index(max_input_index)
    to_engine_part = _provide_to_gear_part_pairs(
        input,
        line_length,
        calculate_bounded_index,
    )

    index_potential_part_code_pairs = reduce(get_index_code_pairs, enumerate(input), [])
    potential_parts = list(map(to_engine_part, index_potential_part_code_pairs))
    potential_gears = reduce(__reduce_parts, potential_parts, {})
    gears = ((g, p[0] * p[1]) for g, p in potential_gears.items() if len(p) == 2)

    return sum(c for _, c in gears)


# Solution: 75805607

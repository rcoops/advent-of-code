from collections.abc import Generator
from functools import reduce

_COLOURS = ("red", "green", "blue")
_COLOUR_COUNT_BASE = {"red": 0, "green": 0, "blue": 0}


def count_colour(colour_count: str) -> tuple[str, int]:
    _, num_str, colour = colour_count.split(" ")

    return colour, int(num_str)


def extract_set_counts(line: str) -> Generator[dict[str, int], None, None]:
    return (
        dict(count_colour(colours) for colours in game_set.split(","))
        for game_set in line.split(";")
    )


def reduce_colour_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return {key: max(a[key], b.get(key, 0)) for key in _COLOURS}


def is_possible(line: str) -> bool:
    set_counts = extract_set_counts(line)
    totals = reduce(reduce_colour_counts, set_counts, _COLOUR_COUNT_BASE)

    return totals["red"] <= 12 and totals["green"] <= 13 and totals["blue"] <= 14


def extract_game_number(line: str) -> tuple[int, str]:
    split = line.split(":")

    return int(split[0][5:]), split[1]


def extract_game_numbers(lines: list[str]) -> Generator[tuple[int, str], None, None]:
    return (extract_game_number(line) for line in lines)


def calculate_possible_games(input: str) -> int:
    return sum(
        (
            game_number
            for game_number, line in extract_game_numbers(input.splitlines())
            if is_possible(line)
        )
    )


def solve(input: str):
    sum_of_possible_game_ids = calculate_possible_games(input)

    return sum_of_possible_game_ids


# Solution 2683

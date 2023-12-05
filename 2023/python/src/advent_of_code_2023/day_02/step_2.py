from collections.abc import Generator
from functools import reduce


def count_colour(colour_count: str) -> tuple[str, int]:
    _, num_str, colour = colour_count.split(" ")

    return colour, int(num_str)


def extract_set_counts(line: str) -> Generator[dict[str, int], None, None]:
    return (
        dict(count_colour(colours) for colours in game_set.split(","))
        for game_set in line.split(";")
    )


def reduce_colour_counts(a: dict[str, int], b: dict[str, int]) -> dict[str, int]:
    return a | {k: (max(v, a[k]) if k in a else v) for k, v in b.items()}


def calculate_cube_powers(line: str) -> int:
    games = line.split(":")[1]
    set_counts = extract_set_counts(games)
    totals = reduce(reduce_colour_counts, set_counts)

    return totals.get("red", 1) * totals.get("green", 1) * totals.get("blue", 1)


def calculate_sum_of_all_cube_powers(input: str) -> int:
    return sum(calculate_cube_powers(line) for line in input.splitlines())


def solve(input: str):
    sum_of_all_cube_powers = calculate_sum_of_all_cube_powers(input)

    return sum_of_all_cube_powers

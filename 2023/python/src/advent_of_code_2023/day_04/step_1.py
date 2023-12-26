from collections.abc import Callable
from functools import reduce


def provide_bitshift_if_present(
    numbers_you_have: list[int],
) -> Callable[[int, int], int]:
    def bitshift_if_present(x: int, y: int) -> int:
        return (x << 1) or 1 if y in numbers_you_have else x

    return bitshift_if_present


def extract_numbers(numbers_text: str) -> list[int]:
    return [int(n) for n in numbers_text.split()]


def solve_line(line: str) -> int:
    if not line:
        return 0
    winning_numbers_text, numbers_you_have_text = line.split(":")[1].split("|")
    winning_numbers = [int(n) for n in winning_numbers_text.split()]
    numbers_you_have = [int(n) for n in numbers_you_have_text.split()]

    bitshift_if_present = provide_bitshift_if_present(numbers_you_have)

    return reduce(bitshift_if_present, winning_numbers, 0)


def solve(input: str) -> int:
    total = sum(solve_line(line) for line in input.splitlines())

    return total


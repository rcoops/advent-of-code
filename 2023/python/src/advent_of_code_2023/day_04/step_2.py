from collections.abc import Callable


def provide_increment_if_present(
    numbers_you_have: list[int],
) -> Callable[[int, int], int]:
    def increment_if_present(x: int, y: int) -> int:
        return x + 1 if y in numbers_you_have else x

    return increment_if_present


def extract_numbers(numbers_text: str) -> list[int]:
    return [int(n) for n in numbers_text.split()]


def solve_line(line: str, counts: dict[int, int], i: int) -> dict[int, int]:
    if not line:
        return {k: v for k, v in counts.items() if k <= i}
    game, numbers = line.split(":")
    card_number = int(game.split()[-1])
    # add one for current card
    counts[card_number] = counts.get(card_number, 0) + 1
    next_card_number = card_number + 1
    winning_numbers_text, numbers_you_have_text = numbers.split("|")
    winning_numbers = extract_numbers(winning_numbers_text)
    numbers_you_have = extract_numbers(numbers_you_have_text)

    card_count = sum(
        1 for winning_number in winning_numbers if winning_number in numbers_you_have
    )
    cards = [*range(next_card_number, next_card_number + card_count)]
    # 1 - 1:1 2:2 3:2 4:2 5:2  -- 2,3,4,5 * 1
    # 2 - 1:1 2:2 3:4 4:4 5:2  -- 3,4 * 2
    # 3 - 1:1 2:2 3:4 4:8 5:6  -- 4,5 * 3
    # 4 - 1:1 2:2 3:4 4:8 5:14 -- 5 * 8
    # 5 - 1:1 2:2 3:4 4:8 5:14
    for card in cards:
        counts[card] = counts.get(card, 0) + counts[card_number]

    return counts


def solve(input: str) -> int:
    counts: dict[int, int] = {}
    for i, line in enumerate(input.splitlines()):
        solve_line(line, counts, i)

    # 30
    return sum(counts.values())

# Solution: 5667240


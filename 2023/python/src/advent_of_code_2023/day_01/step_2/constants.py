from enum import Enum


class Digit(Enum):
    RIGHT = -1
    LEFT = 1


_DIGIT_NUMBER_MAPPINGS = {c: int(c) for c in "123456789"}
_TEXT_NUMBER_MAPPINGS = {
    number: i + 1
    for i, number in enumerate(
        ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    )
} | _DIGIT_NUMBER_MAPPINGS

NUMBER_MAPPINGS = _TEXT_NUMBER_MAPPINGS | _DIGIT_NUMBER_MAPPINGS

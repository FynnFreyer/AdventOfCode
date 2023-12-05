from pathlib import Path
from re import compile, IGNORECASE, VERBOSE, findall

NOT_DIGITS = compile(r"[^0-9]+")


def parse_line(line: str) -> int:
    # strategy for part one:
    # 1. remove anything that is not a digit
    digits_only = NOT_DIGITS.sub("", line)

    # 2. pick first and last digit
    digit_one = digit_two = "0"
    if digits_only:
        digit_one, digit_two = digits_only[0], digits_only[-1]

    # 3. concat and cast to int
    return int(f"{digit_one}{digit_two}")


def parse_file_part_one(file: str | Path) -> int:
    with open(file) as file:
        # do this for every line and sum up the result
        return sum(parse_line(line) for line in file)


# (naive) strategy for part two:
#
# 1. identify all word digits (using findall)
# 2. replace first and last word digit with correct digit
# 3. use solution for part one

LEADING_WORD_DIGIT = compile("""one|two|three|four|five|six|seven|eight|nine""", IGNORECASE | VERBOSE)

# the naive strategy doesn't work, because of overlaps
# and findall returns non-overlapping matches only
#
# possible overlaps:
#   [one, three, five, nine] -> eight
#   eight -> [two, three]
#   two -> one
#
# we can use negative lookaheads to exclude those when finding the last match

CLOSING_WORD_DIGIT = compile(
    r"""
        (?:
            four|six|seven  # those don't overlap, so they're safe
            | (?:on|thre|fiv|nin)(?!eight)e  # match one, three, five, nine only if they are not followed by eight
            | eigh(?!two|three)t  # eight may only match if not followed by two or three
            | tw(?!one)o  # two may not be followed by one
        )(?!.*\d)  # these are only of interest, if not followed by digits
    """, IGNORECASE | VERBOSE
)

REPLACEMENTS: dict[str, str] = {
    # "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def replace_first_and_last_word_digit(line: str) -> str:
    non_overlapping_word_digits = CLOSING_WORD_DIGIT.findall(line)
    if non_overlapping_word_digits:
        last_word = non_overlapping_word_digits[-1]
        line = line.replace(last_word, REPLACEMENTS[last_word])

    first_word_match = LEADING_WORD_DIGIT.search(line)
    if first_word_match:
        first_word = first_word_match[0]
        line = line.replace(first_word, REPLACEMENTS[first_word])
    return line


def parse_file_part_two(file: str | Path) -> int:
    with open(file) as file:
        return sum(parse_line(replace_first_and_last_word_digit(line)) for line in file)


if __name__ == '__main__':
    answer = parse_file_part_two("input.txt")
    print(answer)

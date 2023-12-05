from pathlib import Path
from re import compile

NOT_DIGITS = compile(r"[^0-9]+")


def parse_line(line: str) -> int:
    digits_only = NOT_DIGITS.sub("", line)

    digit_one = digit_two = "0"
    if digits_only:
        digit_one, digit_two = digits_only[0], digits_only[-1]

    return int(f"{digit_one}{digit_two}")


def parse_file(file: str | Path) -> int:
    with open(file) as file:
        return sum(parse_line(line) for line in file)


if __name__ == '__main__':
    answer = parse_file("input.txt")
    print(answer)

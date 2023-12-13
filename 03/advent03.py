from dataclasses import dataclass
from math import prod
from pathlib import Path
from re import compile
from typing import Self, Optional

SYMBOL = compile(r"[^\d.\n]")
NUMBER = compile(r"(\d+)")
GEAR = compile(r"(\*)")


def surroundings(row: int, col: int, max_rows: int = 10, max_cols: int = 10) -> tuple[tuple[int, int], ...]:
    return tuple(
        (x, y)
        for x in range(row - 1, row + 2)  # ranges aren't right inclusive
        for y in range(col - 1, col + 2)  # therefore we use +2 for right
        if 0 <= x <= max_rows and 0 <= y <= max_cols  # are we in bounds?
    )


@dataclass
class PartNumber:
    row: int

    col_start: int
    col_end: int

    value: int

    def __hash__(self):
        return hash((self.row, self.col_start, self.col_end))

    @classmethod
    def from_pos(cls, schematic: str, row: int, col: int) -> Optional[Self]:
        rows = schematic.splitlines()
        numbers = NUMBER.finditer(rows[row])
        for number in numbers:
            col_start, col_end = number.span()
            if col in range(col_start, col_end):
                value = int(number[1])
                return cls(row, col_start, col_end, value)

    @classmethod
    def from_schematic(cls, schematic: str) -> set[Self]:
        part_numbers = set()
        lines = schematic.splitlines()

        max_rows = len(lines)
        max_cols = len(lines[0])

        for symbol_row, line in enumerate(lines):
            matches = SYMBOL.finditer(line)
            for match in matches:
                symbol_col, _ = match.span()
                neighboring_parts = cls.from_neighborhood(schematic, symbol_row, symbol_col,
                                                          max_rows=max_rows, max_cols=max_cols)
                part_numbers.update(neighboring_parts)
        return part_numbers

    @classmethod
    def from_neighborhood(cls, schematic: str, row: int, col: int, max_rows: int = 10, max_cols: int = 10):
        part_numbers = set()
        neighborhood = surroundings(row, col, max_rows=max_rows, max_cols=max_cols)
        for row, col in neighborhood:
            part_number = cls.from_pos(schematic, row, col)
            if part_number is not None:
                part_numbers.add(part_number)
        return part_numbers


def parse_file_part_one(file: str | Path) -> int:
    with open(file) as file:
        schematic = file.read()

    return sum(number.value for number in PartNumber.from_schematic(schematic))


def get_gear_ratios(schematic: str) -> list[int]:
    lines = schematic.splitlines()

    max_rows = len(lines)
    max_cols = len(lines[0])

    gear_ratios = []
    for gear_row, line in enumerate(lines):
        gears = GEAR.finditer(line)
        for gear in gears:
            gear_col, _ = gear.span()
            neighboring_parts = PartNumber.from_neighborhood(schematic, gear_row, gear_col,
                                                             max_rows=max_rows, max_cols=max_cols)
            if len(neighboring_parts) == 2:
                ratio = prod(part.value for part in neighboring_parts)
                gear_ratios.append(ratio)

    return gear_ratios


def parse_file_part_two(file: str | Path) -> int:
    with open(file) as file:
        schematic = file.read()

    return sum(ratio for ratio in get_gear_ratios(schematic))


if __name__ == '__main__':
    sum_of_ratios = parse_file_part_two("input.txt")
    print(sum_of_ratios)

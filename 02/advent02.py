from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from re import compile
from typing import Self

NUMBER = compile(r"(\d+)")


@dataclass
class Game:
    id: int

    red: list[int] = field(default_factory=list)
    green: list[int] = field(default_factory=list)
    blue: list[int] = field(default_factory=list)

    @classmethod
    def from_line(cls, line: str) -> Self:
        id_str, data_str = line.split(":")

        game_id = int(NUMBER.search(id_str)[1])
        data = defaultdict(list)
        for display in data_str.split(";"):
            for cube_count_str in display.split(","):
                num_str, color = cube_count_str.strip().split()
                data[color].append(int(num_str))

        return cls(id=game_id, **data)

    @property
    def max_red(self) -> int:
        return max(self.red)

    @property
    def max_green(self) -> int:
        return max(self.green)

    @property
    def max_blue(self) -> int:
        return max(self.blue)

    def is_possible(self, red: int, green: int, blue: int) -> bool:
        red_plausible = self.max_red <= red
        green_plausible = self.max_green <= green
        blue_plausible = self.max_blue <= blue

        return red_plausible and green_plausible and blue_plausible

    @property
    def power(self) -> int:
        return self.max_red * self.max_green * self.max_blue



def parse_file_part_one(file: str | Path, red: int = 12, green: int = 13, blue: int = 14) -> int:
    with open(file) as file:
        games = [Game.from_line(line) for line in file]

    return sum(game.id for game in games if game.is_possible(red, green, blue))


def parse_file_part_two(file: str | Path) -> int:
    with open(file) as file:
        games = [Game.from_line(line) for line in file]

    return sum(game.power for game in games)


if __name__ == '__main__':
    sum_of_powers = parse_file_part_two("input.txt")
    print(sum_of_powers)

from dataclasses import dataclass, field
from pathlib import Path
from re import compile
from typing import Self

NUMBER = compile(r"(\d+)")


@dataclass
class Card:
    id: int
    winning_numbers: set[int] = field(default_factory=set)
    your_numbers: set[int] = field(default_factory=set)
    multiplier: int = 1

    @property
    def wins(self) -> set[int]:
        return set(number for number in self.your_numbers if number in self.winning_numbers)

    @property
    def win_count(self) -> int:
        return len(self.wins)

    @property
    def points(self) -> int:
        return 2 ** (self.win_count - 1) if self.win_count else 0

    @classmethod
    def from_line(cls, line: str) -> Self:
        card_id_str, card_numbers_str = line.split(":")
        winning_numbers_str, your_numbers_str = card_numbers_str.split("|")

        card_id = int(NUMBER.search(card_id_str)[1])
        winning_numbers = set(int(num) for num in winning_numbers_str.split())
        your_numbers = set(int(num) for num in your_numbers_str.split())

        return cls(card_id, winning_numbers, your_numbers)


def parse_file_part_one(file: str | Path) -> int:
    with open(file) as file:
        cards = (Card.from_line(line) for line in file)
        return sum(card.points for card in cards)


def parse_file_part_two(file: str | Path) -> int:
    with open(file) as file:
        cards = [Card.from_line(line) for line in file]

    # TODO: this is slow as fuck
    for i, card in enumerate(cards):
        for _ in range(card.multiplier):
            for offset in range(card.win_count):
                try:
                    cards[i + offset + 1].multiplier += 1
                except IndexError:
                    break  # end of table -> next card

    return sum(card.multiplier for card in cards)


if __name__ == '__main__':
    sum_of_cards = parse_file_part_two("input.txt")
    print(sum_of_cards)

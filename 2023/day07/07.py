from collections import Counter
from enum import Enum, IntEnum


with open("aoc/2023/day07/data.txt", "r") as file:
    data = file.readlines()

with open("aoc/2023/day07/test.txt", "r") as file:
    test = file.readlines()

Handtype = IntEnum(
    "Handtype",
    list(
        zip(
            ["HIGH_CARD", "PAIR", "TWOPAIR", "THREE", "FULL_HOUSE", "FOUR", "FIVE"],
            range(7),
        )
    ),
)


Card = IntEnum("Card", list(zip("23456789TJQKA", range(13))))


def parse(data: str) -> list[tuple[str, int]]:
    return [(s[0], int(s[1])) for line in data if (s := line.split(" "))]


def handtype(hand: str) -> Handtype:
    pairs = 0
    hastriple, hasquad = False, False
    occs = {}
    for card in hand:
        occs.update({card: occs.get(card, 0) + 1})
    for v in occs.values():
        if v == 2:
            pairs += 1
        elif v == 3:
            hastriple = True
        elif v >= 4:
            return Handtype.FIVE if v == 5 else Handtype.FOUR
    if pairs:
        return Handtype.PAIR if pairs == 1 else Handtype.TWOPAIR
    elif hastriple:
        return Handtype.FULL_HOUSE if pairs else Handtype.THREE
    else:
        return Handtype.HIGH_CARD


def translate(hand: str) -> str:
    return [Card[card] for card in hand]


def get_score(card_order, hands, joker_transform=False):
    def sort_key(hand: tuple[str, int]):
        if joker_transform:
            most_common = Counter(hand[0].replace("J", "")).most_common(1)
            hand = hand[0].replace("J", most_common[0][0] if most_common else "J")
            return (
                tuple(sorted(Counter(hand).values(), reverse=True)),
                tuple(card_order.index(c) for c in hand[0]),
            )
        else:
            return (
                tuple(sorted(Counter(hand[0]).values(), reverse=True)),
                tuple(card_order.index(c) for c in hand[0]),
            )

    return sum([h[1] * rank for rank, h in enumerate(sorted(hands, key=sort_key), 1)])


print(get_score("23456789TJQKA", parse(data)))
print(get_score("J23456789TQKA", parse(data), True))

print(get_score("23456789TJQKA", parse(test)))
print(get_score("J23456789TQKA", parse(test), True))

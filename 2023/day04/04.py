import re


with open("aoc/2023/day04/data.txt", "r") as file:
    data = file.readlines()

with open("aoc/2023/day04/test.txt", "r") as file:
    test = file.readlines()


def parse_data(data):
    cards = []
    for line in data:
        lucky, num = line.split("|")
        cards.append(
            [
                [int(x) for x in (lucky[10:].strip().split(" ")) if x != ""],
                [int(x) for x in num.strip().split(" ") if x != ""],
            ]
        )
    return cards


cards = parse_data(data)
testcards = parse_data(test)


### PART 1
print(
    sum(
        [int(2 ** (sum([lucky in card[1] for lucky in card[0]]) - 1)) for card in cards]
    )
)


def score_cards(cards):
    mult = [1] * len(cards)
    for idx, card in enumerate(cards):
        score = sum([lucky in card[1] for lucky in card[0]])
        for i in range(1, score + 1):
            mult[idx + i] += mult[idx]
    return sum(mult)


print(score_cards(testcards))
print(score_cards(cards))

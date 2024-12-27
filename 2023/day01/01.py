import re


with open("aoc/2023/day01/data.txt", "r") as file:
    data = file.readlines()


def get_cal(input):
    first = re.search(r"(\d).*$", input).group(1)
    last = re.search(r"^.*(\d)", input).group(1)
    return int("".join((first, last)))


def to_int(s: str):
    d = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "zero": 0,
    }
    return str(d[s]) if len(s) > 1 else s


def get_cal(input):
    first = re.search(
        r"(\d|one|two|three|four|five|six|seven|eight|nine|zero).*$", input
    ).group(1)
    last = re.search(
        r"^.*(\d|one|two|three|four|five|six|seven|eight|nine|zero)", input
    ).group(1)
    print(first, last)
    return int("".join((to_int(first), to_int(last))))


print(sum([get_cal(line) for line in data]))


print(get_cal("355knfjsdqjm8\n"))

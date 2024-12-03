import functools

with open("aoc/2024/day02/resources/data.txt", "r") as file:
    data = file.read()


def is_report_safe(rep: list) -> bool:
    if len(rep) <= 1:
        return True
    elif rep[0] == rep[1]:
        return False
    else:
        asc = rep[1] - rep[0] > 0
        for i in range(len(rep) - 1):
            print(rep[i] != rep[i + 1])
            if (
                (rep[i] < rep[i + 1] and not asc)
                or (rep[i] > rep[i + 1] and asc)
                or abs(rep[i] - rep[i + 1]) > 3
                or rep[i] == rep[i + 1]
            ):
                return False
        return True


df = list(map(lambda x: list(map(int, x.split(" "))), data[:-1].split("\n")))

print(sum(map(lambda x: 1 if is_report_safe(x) else 0, df)))

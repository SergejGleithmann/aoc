import re
import operator

with open("03/resources/data.txt", "r") as file:
    data = file.read()


def apply_mult(data: str) -> int:
    matches = re.findall(r"mul\((\d+),(\d+)\)", data)
    return sum(map(lambda args: operator.mul(*map(int, args)), matches))


def clean_do(data: str) -> str:
    return re.sub(r"don't\(\)(.|\n)*?(do\(\)|$)", "", data)


print(apply_mult(clean_do(data)))

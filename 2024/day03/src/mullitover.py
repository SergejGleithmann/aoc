import re
import operator

with open("03/resources/data.txt", "r") as file:
    data = file.read()


## PART 1
def apply_mult(data: str) -> int:
    matches = re.findall(r"mul\((\d+),(\d+)\)", data)
    return sum(map(lambda args: operator.mul(*map(int, args)), matches))


# data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

### PART 2


# Erklärung zum regulären Ausdruck:
# *? versucht so wenig wie möglich zu matchen, $ ist das ende des Strings und
# . matched alles AUSSER \n, daher muss . mit \n verodert werden
def clean_do(data: str) -> str:
    return re.sub(r"don't\(\)(.|\n)*?(do\(\)|$)", "", data)


print(apply_mult(clean_do(data)))

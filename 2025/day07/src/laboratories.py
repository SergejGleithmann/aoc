with open("aoc/2025/day07/resources/input.txt", "r") as file:
    data = file.readlines()


with open("aoc/2025/day07/resources/test.txt", "r") as file:
    test = file.readlines()


def count_splits(lines: list[str]) -> int:
    todo = {lines[0].index("S")}
    current = 0
    for line in lines[1:]:
        for idx in [idx for idx in todo if line[idx] == "^"]:
            todo.remove(idx)
            todo |= {idx + 1, idx - 1}
            current += 1
    return current


def count_qsplits(lines: list[str]) -> int:
    todo = {lines[0].index("S"): 1}
    for line in lines[1:]:
        for idx, val in [(idx, val) for idx, val in todo.items() if line[idx] == "^"]:
            todo.pop(idx)
            todo[idx - 1] = todo.get(idx - 1, 0) + val
            todo[idx + 1] = todo.get(idx + 1, 0) + val
    return sum(todo.values())


print("-- Part 1--")
print(f"Splits in the test data:         {count_splits(test):15}")
print(f"Splits in the input data:        {count_splits(data):15}")
print("-- Part 2--")
print(f"Active timelines for test data:  {count_qsplits(test):15}")
print(f"Active timelines for input data: {count_qsplits(data):15}")

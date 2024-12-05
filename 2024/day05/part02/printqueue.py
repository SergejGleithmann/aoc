from typing import List, Tuple
from functools import cmp_to_key


with open("aoc/2024/day05/resources/data.txt", "r") as file:
    data = file.read()
""" 
with open("aoc/2024/day05/resources/test.txt", "r") as file:
    data = file.read()
 """

# preprocessing
rules_raw, updates_raw = data.split("\n\n")
rules: List[Tuple[int]] = list(
    map(lambda x: tuple(map(int, x.split("|"))), rules_raw.split("\n"))
)
updates: List[List[int]] = list(
    map(lambda x: list(map(int, x.split(","))), updates_raw[:-1].split("\n"))
)


def get_pre_post(update, page: int) -> Tuple[List[int], int, List[int]]:
    unknown = []
    pre = []
    post = []
    for other_page in update:
        rule_found = False
        for rule in rules:
            if rule[0] == other_page and rule[1] == page:
                pre.append(other_page)
                rule_found = True
                break
            elif rule[1] == other_page and rule[0] == page:
                post.append(other_page)
                rule_found = True
                break
        # obsolete
        if not rule_found:
            unknown.append(other_page)
    # obsolete
    for u in unknown:
        for pre_page in pre:
            if (u, pre_page) in rules:
                pre.append(u)
                break
        post.append(u)

    return pre, post


def repair_update(update: List[int]) -> List[int]:
    if len(update) <= 1:
        return update
    else:
        pre, post = get_pre_post(update[1:], update[0])
        return repair_update(pre) + [update[0]] + repair_update(post)


def check_update(update: List[int]) -> bool:
    l = len(update)
    for i in range(l):
        for j in range(i + 1, l):
            if (update[j], update[i]) in rules:
                return False
    return True


def handle_update(update: List[int]) -> bool:
    return update if check_update(update) else repair_update(update)


def sum_of_middle_printed_repaired(updates: List[List[int]]) -> int:
    return sum(
        [
            repair_update(update)[len(update) // 2]
            for update in updates
            if not check_update(update)
        ]
    )


print(sum_of_middle_printed_repaired(updates))

""" 
res = []
for update in updates:
    for page in update:
        count = 0
        for rule in rules:
            if page == rule[0] or page == rule[1]:
                found = True
                count += 1
        res.append(count)
print(res) 
"""

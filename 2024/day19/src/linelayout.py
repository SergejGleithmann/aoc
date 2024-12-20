import heapq
import re

from copy import copy
from typing import Self

import numpy as np


with open("aoc/2024/day19/resources/data.txt", "r") as file:
    data = file.read()


""" with open("aoc/2024/day19/resources/test.txt", "r") as file:
    data = file.read() """


towels_str, combinations_str = data.split("\n\n")

towels = towels_str.strip().split(", ")

combinations = [comb for comb in combinations_str.strip().split("\n")]

# print(towels, combinations)

cache = {}


def check(combination, towels):
    if (c := cache.get(combination)) is not None:
        return c
    if len(combination) == 0:
        return True
    for towel in towels:
        if towel == combination[: len(towel)]:
            if check(combination[len(towel) :], towels):
                return True
    return False


def check_all(combinations, towels):
    res = 0
    for i, combination in enumerate(combinations):
        print(i)
        if check(combination, towels):
            res += 1
    return res


def check_all_w_tree(combinations, towels):
    tree = get_tree(towels)
    res = 0
    for i, combination in enumerate(combinations):
        if check_w_tree(combination, tree):
            res += 1
    return res


def get_tree(towels):
    start = {"stop": True}
    for towel in towels:
        curr = start
        for i, color in enumerate(towel):
            if color not in curr.keys():
                new = {}
                curr[color] = new
            """ if i == len(towel) - 1:
                print(curr, start)
                curr[color] = start | curr[color] """
            curr = curr[color]
        curr["stop"] = True
    return start


def check_w_tree(combination, tree: dict):
    curr = tree
    for l in combination:
        v = curr.get(l, None)
        if v is None:
            return False
        else:
            curr = v
        if "stop" in curr.keys():
            curr = tree
    return "stop" in curr.keys()


# print(sum([int(check(combination, towels)) for combination in combinations]))
# print([int(check(combination, towels)) for combination in combinations])
# print(check_w_tree("bwurrg", get_tree(towels)))
print(check_all(combinations, towels))
# print(check_w_tree("wrbwgruugbbgwwurggwrgrrrurbgwbgggwbbgwgbrwggwur", get_tree(towels)))

# print(check_all_w_tree(combinations, towels))
# print(get_tree(towels))

# tree = get_tree(towels)
# print(tree["b"]["w"]["u"]["r"]["r"])

# print(get_tree(["r", "rw", "s"]))

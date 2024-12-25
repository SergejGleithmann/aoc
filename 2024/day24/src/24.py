import copy
import re


def parse_input(file) -> tuple[dict[str, bool], dict[str, tuple[str, str, str]]]:
    init, rules = file.split("\n\n")
    return {
        s[0]: bool(int(s[1]))
        for line in init.split("\n")
        if len((s := line.split(": "))) == 2
    }, {
        m.group("res"): m.group("op1", "op", "op2")
        for rule in rules.split("\n")
        if (
            m := re.match(
                r"(?P<op1>(\w|\d){3}) (?P<op>(?:\w|\d){2,3}) (?P<op2>(\w|\d){3}) -> (?P<res>(\w|\d){3})",
                rule,
            )
        )
    }


with open("aoc/2024/day24/resources/data.txt", "r") as file:
    INIT, RULES = parse_input(file.read())

INLEN = 45
OUTLEN = 46


def get_var_len(var: str = "z") -> int:
    return len([line for line in (RULES.keys() | INIT.keys()) if line[0] == var])


def apply(op1: bool, op: str, op2: bool) -> bool:
    match op:
        case "AND":
            return op1 and op2
        case "OR":
            return op1 or op2
        case "XOR":
            return op1 ^ op2
        case _:
            raise ValueError("Operator must be one of AND, OR, XOR")


def derive(
    key: str,
    init: dict[str, bool] = INIT,
    rules: dict[str, tuple[str, str, str]] = RULES,
) -> bool:
    if key in rules.keys():
        op1, op, op2 = rules[key]
        return apply(derive(op1, init, rules), op, derive(op2, init, rules))
    else:
        return init.get(key, False)


def get(
    var: str = "z",
    init: dict[str, bool] = INIT,
    rules: dict[str, tuple[str, str, str]] = RULES,
) -> str:
    res = []
    for i in range(get_var_len(var)):
        res = [derive(f"{var}{i:02d}", init, rules)] + res
    return "".join(map(lambda x: "1" if x else "0", res))


print(RULES)
print(int(get("z"), 2))
x = get("x")
print(f"x={x}, {int(x,2)}")
y = get("y")
print(f"y={y}, {int(y,2)}")
correct_res = int(x, 2) + int(y, 2)
print(f"expected: {bin(correct_res)[2:]}, {correct_res}")
z = get("z")
print(f"got: {z}, {int(z,2)}")


def faulty_bits(
    x: int | None = None,
    y: int | None = None,
    init: dict[str, bool] = INIT,
    rules: dict[str, tuple[str, str, str]] = RULES,
) -> list[str]:
    if x is None or y is None:
        x = int(get("x", init, rules), 2)
        y = int(get("y", init, rules), 2)
        z_str = get("z", init, rules)
    else:
        z_str = add(x, y, rules)
    res = x + y
    res_str = bin(res)[2:]
    faulty: list[str] = []
    for i in range(1, len(res_str) + 1):
        if res_str[-i] != z_str[-i]:
            faulty.append(f"z{len(res_str) - i - 1:02d}")
    return faulty


def add(
    x: int,
    y: int,
    rules: dict[str, tuple[str, str, str]] = RULES,
) -> str:
    init = {
        f"{varname}{idx:02d}": bool(int(bit))
        for varname, var in [("x", x), ("y", y)]
        for idx, bit in enumerate(bin(var)[2:])
    }
    return get(init=init, rules=rules)


def swap(swaps: list[tuple[str, str]]):
    rules = copy.copy(RULES)
    for s1, s2 in swaps:
        rules[s1], rules[s2] = RULES[s2], RULES[s1]
    return rules


def check_connections(rules: dict[str, tuple[str, str, str]]) -> list[str]:
    res: set[str] = set()
    for k, v in rules.items():
        op1, op, op2 = v
        if k[0] == "z" and op != "XOR" and k != "z45":
            res.add(k)
        if (
            op == "XOR"
            and k[0] not in "xyz"
            and op1[0] not in "xyz"
            and op2[0] not in "xyz"
        ):
            res.add(k)
        if op == "AND" and "x00" not in [op1, op2]:
            for subv in rules.values():
                subop1, subop, subop2 = subv
                if (k == subop1 or k == subop2) and subop != "OR":
                    res.add(k)
        if op == "XOR":
            for subv in rules.values():
                subop1, subop, subop2 = subv
                if (k == subop1 or k == subop2) and subop == "OR":
                    res.add(k)
    res_list = list(res)
    res_list.sort()
    return res_list


print(get())


t1 = faulty_bits()
print(faulty_bits(), len(t1))

swap_list = [("z24", "fpq"), ("srn", "z32"), ("nqk", "z07"), ("fgt", "pcp")]
fix = swap(swap_list)
t2 = faulty_bits(rules=fix)
print(t2, len(t2))

### Z Digit ohne XOR
print("Z-no XOR", [(k, v) for k, v in fix.items() if k[0] == "z" and v[1] != "XOR"])

###
print(
    "Middle XOR",
    [
        (k, v)
        for k, v in fix.items()
        if k[0] not in "xyz" and v[1] == "XOR" and v[0][0] not in "xyz"
    ],
)

print(",".join(check_connections(RULES)))

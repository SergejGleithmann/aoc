import re

from copy import copy


with open("aoc/2024/day17/resources/data.txt", "r") as file:
    data = file.read()


""" with open("aoc/2024/day17/resources/test.txt", "r") as file:
    data = file.read() """

str_reg, str_program = data.split("\n\n")


def parse_data(data):
    reg = {
        m.group(1): int(m.group(2))
        for reg in str_reg.split("\n")
        if (m := re.match(r"Register ([A-Z]): (\d+)", reg))
    }
    program = [
        int(val)
        for val in ((re.match(r"Program: (.*)", str_program)).group(1)).split(",")
    ]
    return program, reg


def combo(operand, reg):
    if 0 <= operand <= 3:
        return operand
    elif 4 <= operand <= 6:
        return reg[chr(ord("A") + operand - 4)]
    else:
        raise ValueError("Combo operand expects Values from 1-6")


def adv(reg, operand, output, cnt):
    reg["A"] = reg["A"] // (1 << combo(operand, reg))
    return output, cnt + 2


def bxl(reg, operand, output, cnt):
    reg["B"] = reg["B"] ^ operand
    return output, cnt + 2


def bst(reg, operand, output, cnt):
    reg["B"] = combo(operand, reg) % 8
    return output, cnt + 2


def jnz(reg, operand, output, cnt):
    return output, (cnt + 2 if reg["A"] == 0 else operand)


def bxc(reg, operand, output, cnt):
    reg["B"] = reg["B"] ^ reg["C"]
    return output, cnt + 2


def out(reg, operand, output, cnt):
    output.append(combo(operand, reg) % 8)
    return output, cnt + 2


def bdv(reg, operand, output, cnt):
    reg["B"] = reg["A"] // (1 << combo(operand, reg))
    return output, cnt + 2


def cdv(reg, operand, output, cnt):
    reg["C"] = reg["A"] // (1 << combo(operand, reg))
    return output, cnt + 2


def execute(program, reg):
    cnt = 0
    output = []
    while cnt < len(program):
        opcode, operand = program[cnt], program[cnt + 1]

        # print(reg, opcode, operand, output, cnt)
        try:
            function = [adv, bxl, bst, jnz, bxc, out, bdv, cdv][opcode]
        except IndexError:
            raise ValueError("Invalid opcode.")
        output, cnt = function(reg, operand, output, cnt)
    return output


program, reg = parse_data(data)

#### PART 1:
output = execute(program, copy(reg))
print(output)
print(",".join(map(str, output)))
input()


def get_output(a):
    output = []
    registers = copy(reg)
    registers["A"] = a
    length = len(program)
    cnt = 0
    while cnt < length:
        opcode, operand = program[cnt : cnt + 2]
        try:
            function = [adv, bxl, bst, jnz, bxc, out, bdv, cdv][opcode]
        except IndexError:
            raise ValueError("Invalid opcode.")
        output, cnt = function(registers, operand, output, cnt)
    return output


#### PART 2
valid = [0]
for length in range(1, len(program) + 1):
    oldValid = valid
    valid = []
    for num in oldValid:
        for offset in range(8):
            newNum = 8 * num + offset
            if get_output(newNum) == program[-length:]:
                valid.append(newNum)

answer = min(valid)
print(answer)
# print(get_output(2))

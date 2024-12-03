import functools
from test import safe_removal

with open("aoc/2024/day02/resources/data.txt", "r") as file:
    data = file.read()


def is_level_transition_safe(x, y, asc) -> bool:
    return not ((x < y and not asc) or (x > y and asc) or abs(x - y) > 3 or x == y)


def is_report_safe(rep: list, asc=None) -> bool:
    if len(rep) <= 1:
        return True
    else:
        if asc is None:
            asc = rep[1] - rep[0] > 0
        for i in range(len(rep) - 1):
            if not is_level_transition_safe(rep[i], rep[i + 1], asc):
                return False
        return True


def is_report_recover_safe(rep: list) -> bool:
    # flag for encountered error
    error = False
    if len(rep) <= 1:
        return True
    else:
        # guess ascending/descending
        asc = (rep[1] - rep[0]) > 0

        for i in range(len(rep) - 1):
            # error means encountered violation at i-1 -> i
            # and that it was tried to fix this by removing i-1
            # but this failed, so we have to fix it by removing i
            if error:
                # try to omit i by checking i-1 -> i+1 and the rest of the array without recovery and current asc
                # or check if we used the wrong asc/desc by removing 0 index
                return (
                    is_report_safe(rep[i + 1 :], asc)
                    and is_level_transition_safe(rep[i - 1], rep[i + 1], asc)
                    or is_report_safe(rep[1:])
                )
            # if no violation was encountered but we now get one
            # check if we can remove current index
            # otherwise raise violation flag
            if not is_level_transition_safe(rep[i], rep[i + 1], asc):
                temp_asc = (rep[2] - rep[0] > 0) if i == 1 else asc
                error = True
                if (i == 0 and is_report_safe(rep[1:])) or (
                    is_level_transition_safe(rep[i - 1], rep[i + 1], temp_asc)
                    and is_report_safe(rep[i + 1 :], temp_asc)
                ):
                    return True
            # otherwise everything is fine
        return True


df = list(map(lambda x: list(map(int, x.split(" "))), data[:-1].split("\n")))


print(sum(map(lambda x: 1 if is_report_recover_safe(x) else 0, df)))

print(is_report_recover_safe([2, 2, 1]))

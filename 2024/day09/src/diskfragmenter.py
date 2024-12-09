from typing import List, Tuple


with open("aoc/2024/day09/resources/data.txt", "r") as file:
    data = file.readline()

record = [int(d) for d in data if d != "\n"]
# print(data)


def extend(record: List[int]) -> List[int | None]:
    file = True
    id = 0
    res = []
    for r in record:
        res.extend([id if file else None for _ in range(r)])
        if file:
            id += 1
        file = not file
    # print(res)
    return res


def compact_blockwise(record: List[int | None]) -> List[int | None]:
    i, j = 0, len(record) - 1
    while True:
        while record[i] != None:
            i += 1
        while record[j] == None:
            j -= 1
        if i < j:
            record[i], record[j] = record[j], record[i]
        else:
            break
    return record


def get_next_space(record: List[int | None], index: int) -> Tuple[int, int | None]:
    while record[index] != None:
        index += 1
        if index >= len(record):
            return -1, None
    end_index = index + 1
    while end_index < len(record) and record[end_index] == None:
        end_index += 1
    return index, end_index


def get_previous_file(record: List[int | None], index: int) -> Tuple[int, int | None]:
    if index < 0:
        return -1, None
    while record[index - 1] == None:
        index -= 1
        if index < 0:
            return -1, None
    start_index = index
    while start_index > 0 and record[start_index - 1] == record[index - 1]:
        start_index -= 1
    return start_index, index


def compact_filewise(record: List[int | None]) -> List[int | None]:
    sf = len(record)
    while True:
        sf, ef = get_previous_file(record, sf)
        # print(sf, ef)
        if ef == None or ef == 0:
            break
        else:
            es = 0
            while True:
                ss, es = get_next_space(record, es)
                if ss > sf or es is None:
                    break
                elif es - ss >= ef - sf:
                    record[ss : ss + ef - sf] = record[sf:ef]
                    record[sf:ef] = [None for _ in range(ef - sf)]
                    # print(record, len(record), es - ss, ef - sf)
                    # input()
                    break
    # print(record)
    return record


def compact_filewise_unextended(record: List[int | None]) -> List[int | None]:
    file_index = ((len(record) - 1) // 2) * 2
    while file_index > 0:
        for space_index in range(1, 2, file_index):
            space = record[space_index]
            file_size = record[file_index]
            if file_size <= space:
                record[space_index:space_index] = [
                    0,
                    file_size,
                    space_index - file_size,
                ]
                record[file_index - 1 : file_index + 2] = [
                    record[file_index - 1] + file_size + record[file_index + 1]
                ]
        file_index -= 2
    return record


def checksum(record: List[int | None]) -> int:
    return sum([idx * value for idx, value in enumerate(record) if value != None])


# print(extend([2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2]))
# print(compact(extend([2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2])))
# print(
#    checksum(compact(extend([2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2])))
# )

# print(checksum(compact_blockwise(extend(record))))
# print(checksum(extend(compact_filewise_unextended(record))))
""" test = extend([2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2])
print("Ext", test, len(test))
print(get_previous_file(test, len(test)))
t1, t2 = get_previous_file(test, 40)
print(test[t1:t2], test[40:42])
print(get_next_space(test, 0))
print(
    checksum(
        compact_filewise(
            extend([2, 3, 3, 3, 1, 3, 3, 1, 2, 1, 4, 1, 4, 1, 3, 1, 4, 0, 2])
        )
    )
) """


print(checksum(compact_filewise(extend(record))))

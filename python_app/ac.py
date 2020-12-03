import math
from itertools import combinations
import re
import functools

def eat_input(input_file):
    with open('../inputs/' + input_file) as f:
        return f.read().splitlines()


# PROBLEM 1

input_1 = [int(entry) for entry in eat_input("1.txt")]
solver = lambda x: ([math.prod(list(permutation)) for permutation in combinations(input_1, x) if sum(list(permutation))==2020])[0]

#1.1
print("1.1")
print(solver(2))
#1.2
print("1.2")
print(solver(3))

# PROBLEM 2

input_2 = eat_input("2.txt")

transformer = lambda expr: re.match(r"(?P<min>\d+)-(?P<max>\d+)\s(?P<letter>[a-z]+):\s(?P<word>[a-z]+)", expr).groupdict()

#2.1
print("2.1")
print(
    functools.reduce(
        lambda acc, val: acc + (
            0 if val["word"].count(val["letter"]) not in range(int(val["min"]), int(val["max"]) +1) else
            1
        ),
        [transformer(entry) for entry in input_2],
        0
    )
)

#2.2
print("2.2")
print(
    functools.reduce(
        lambda acc, val: acc + (
            0 if (
                    val["letter"] != val["word"][int(val["min"])-1] and
                    val["letter"] != val["word"][int(val["max"])-1]
                ) or (
                    val["letter"] == val["word"][int(val["min"])-1] and
                    val["letter"] == val["word"][int(val["max"])-1]
                ) else
            1
        ),
        [transformer(entry) for entry in input_2],
        0
    )
)

# PROBLEM 3

input_3 = eat_input("3.txt")

def row_modifier(row, numerator, denominator, index):
    if (index > 0) and (index % numerator == 0):
        return (
            row[: (index * denominator // numerator) % (len(row))] +
            ("X" if row[(index * denominator // numerator) % (len(row))] == "#" else "O") +
            row[(index * denominator // numerator) % (len(row)) + 1:]
        )
    else:
        return row

#3.1
print("3.1")
print(
    "".join([ row_modifier(row,1,3,index) for index, row in enumerate(input_3)]).count("X")
)

#3.2
print("3.2")
print(
    "".join([ row_modifier(row,1,1,index) for index, row in enumerate(input_3)]).count("X")
    * "".join([ row_modifier(row,1,3,index) for index, row in enumerate(input_3)]).count("X")
    * "".join([ row_modifier(row,1,5,index) for index, row in enumerate(input_3)]).count("X")
    * "".join([ row_modifier(row,1,7,index) for index, row in enumerate(input_3)]).count("X")
    * "".join([ row_modifier(row,2,1,index) for index, row in enumerate(input_3)]).count("X"),
)
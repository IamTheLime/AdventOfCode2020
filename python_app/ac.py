import math
from itertools import combinations
import re
import functools

def eat_input(input_file):
    with open('../inputs/' + input_file) as f:
        return f.read().splitlines()

def eat_raw_input(input_file):
    with open('../inputs/' + input_file) as f:
        return f.read()

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

# PROBLEM 3

input_4 = eat_raw_input("4.txt")
transformer = lambda expr: re.match(
    r"((byr:(?P<byr>.+?)|iyr:(?P<iyr>.+?)|eyr:(?P<eyr>.+?)|hgt:(?P<hgt>.+?)|hcl:(?P<hcl>.+?)|ecl:(?P<ecl>.+?)|pid:(?P<pid>.+?)|cid:(?P<cid>.+?))(\s|\n))+",
    expr
).groupdict()

num_nones = lambda passport: functools.reduce(lambda acc, value: 1 + acc if not value else acc, passport.values(),0)

def passport_rules(passport, part):
    if num_nones(passport) == 0 or ( num_nones(passport) == 1 and not passport['cid']):
        if part == 1:
            return True
        if re.match(r"(\d+)(in|cm)", passport['hgt']) is None:
            return False
        hgt = re.match(r"(?P<hgt>\d+)(?P<unit>(in|cm))", passport['hgt']).groupdict()
        hcl = re.match(r"^#[a-f0-9]{6}$",passport['hcl'])
        pid = re.match(r"(^[0-9]{9}$)", passport['pid'])
        return all([
            int(passport['byr']) >= 1920 and int(passport['byr']) <= 2002,
            int(passport['iyr']) >= 2010 and int(passport['iyr']) <= 2020,
            int(passport['eyr']) >= 2020 and int(passport['eyr']) <= 2030,
            (int(hgt['hgt']) >= 150 and int(hgt['hgt']) <= 193 ) if hgt["unit"]=="cm" else (int(hgt['hgt']) >= 59 and int(hgt['hgt']) <= 76),
            hcl is not None,
            pid is not None,
            passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
        ])
    else:
        return False

print("4.1")
print(
    len([
        transformer(passport+"\n") for passport in re.split( r"\n{2}", input_4) if passport_rules(transformer(passport+"\n"), 1)
    ])
)
print("4.2")
print(
    len([
        transformer(passport+"\n") for passport in re.split( r"\n{2}", input_4) if passport_rules(transformer(passport+"\n"), 2)
    ])
)

# PROBLEM 3

input_4 = eat_raw_input("4.txt")
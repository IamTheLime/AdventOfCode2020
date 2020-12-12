import math
from itertools import combinations
import re
import functools
from pprint import pp

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

# PROBLEM 5

input_5 = eat_input("5.txt")

print("5.1")

seat_tuples = [
    (
        row := sum([(2 ** abs(index - 6)) * int(bit) for index, bit in enumerate(seat[:7].replace("F","0").replace("B","1"))]),
        column := sum([(2 ** abs(index - 2)) * int(bit) for index, bit in enumerate(seat[7:].replace("L","0").replace("R","1"))]),
        row * 8 + column
    )
    for seat in input_5
]

print(
    functools.reduce( lambda acc, seat: seat[2] if seat[2] > acc else acc, seat_tuples, 0)
)

print("5.2")

seat_ids = [seat[2] for seat in seat_tuples]
print(
    functools.reduce( lambda acc, seat_id: (seat_id + 1) if (seat_id + 1) not in seat_ids and (seat_id + 2) in seat_ids else acc, seat_ids, -1)
)

# PROBLEM 6

input_6 = eat_raw_input("6.txt")

group_splitter = lambda group_string: re.split("\n", group_string)
answer_list = [
    [ person for person in group_splitter(answers)] for answers in re.split( r"\n{2}", input_6)
]

print("6.1")
print(
    sum([len(set([answer for person in group for answer in person])) for group in answer_list])
)

print("6.2")
print(
    sum([
        functools.reduce(
            lambda acc, answer: acc + 1 if all([answer in person for person in group]) else acc,
            group[0],
            0
        ) for group in answer_list
    ])
)

# PROBLEM 7

input_7 = eat_input("7.txt")

transformer = lambda expr: {
    re.compile(
        r"(?P<container>[a-zA-zZ]+\s[a-zA-Z]+)\sbags\scontain\s.+"
    ).findall(expr)[0]:
    [
        bag_description.groupdict() for bag_description in
        re.compile(
            r"((?P<num_bags>\d+)\s(?P<bag>[a-zA-zZ]+\s[a-zA-Z]+)\sbag(s?)(,|\.)\s?)"
        ).finditer(expr)
    ]
}

def shiny_gold_bag_exists(bag_content):
    if len(bag_content) == 0:
        return False
    for sub_bag in bag_content:
        if sub_bag['bag'] == "shiny gold" and int(sub_bag['num_bags']) > 0:
            return True
    for sub_bag in bag_content:
        if shiny_gold_bag_exists(structured_input[sub_bag['bag']]):
            return True
    return False

structured_input = functools.reduce( lambda acc, bag: {**acc, **bag}, [transformer(result) for result in input_7], {})

print("7.1")
print(
    functools.reduce(
        lambda acc, bag: acc + 1 if shiny_gold_bag_exists(bag[1]) else acc,
        structured_input.items(),
        0
    )
)

def bag_calculator(bag_content):
    if len(bag_content) == 0:
        return 1
    return functools.reduce(
        lambda acc, sub_bag: acc + int(sub_bag['num_bags']) * bag_calculator(structured_input[sub_bag['bag']]),
        bag_content,
        0
    ) + 1

print("7.2")
print(
    bag_calculator(structured_input["shiny gold"]) - 1 #subracting one as bag calculator will include the holder bag
)

# PROBLEM 8

input_8 = eat_input("8.txt")

transformer = lambda expr: re.match(
    r"(?P<op>(nop|acc|jmp))\s(?P<value>(-|\+)\d+)",
    expr
).groupdict()


instructions = [transformer(instruction) for instruction in input_8]

def executor(instructions):
    index = 0
    acc = 0
    stack = []

    while index not in stack and index < len(instructions):
        instruction = instructions[index]
        stack.append(index)
        if instruction['op'] == 'jmp':
            index += int(instruction['value'])
        elif instruction['op'] == 'acc':
            acc += int(instruction['value'])
            index += 1
        else:
            index += 1

    if index == len(instructions):
        return ("OK", acc)
    return ("ERROR", acc)

print("8.1")
print(executor(instructions))

def generate_new_instruction_stack(instruction_stack, index):
    import copy
    new_stack = copy.deepcopy(instruction_stack)
    new_stack[index]['op'] = 'nop' if new_stack[index]['op'] == 'jmp' else 'jmp'
    return new_stack

print("8.1")

def solver(instructions):
    for instruction_stack in [generate_new_instruction_stack(instructions, index) for index, operation in enumerate(instructions) if operation['op'] in ['jmp', 'nop']]:
        if result := executor(instruction_stack):
            if result[0] == "OK":
                return result

print(solver(instructions))

# PROBLEM 9

input_9 = [ int(number) for number in eat_input("9.txt")]

def no_preamble_matches(start, stop, number, inpt):
    return all([ False if number-preamble_number in inpt[start:stop] else True for preamble_number in inpt[start:stop]])

def sum_finder(inpt, preamble):
    return [number for index, number in enumerate(inpt[preamble:]) if no_preamble_matches(index, index+preamble, number, inpt)]

print("9.1")
print(
    sum_finder(input_9, 25)[0]
)

def search_matches(input_9, start_index, inv_number):
    for stop_index in range(start_index,len(input_9)):
        if (result := sum(input_9[start_index:stop_index])) > inv_number:
            return
        elif result == inv_number:
            return input_9[start_index:stop_index]


def contiguous_search(input_9, inv_number):
    for index, pivot in enumerate(input_9):
        if found_match := search_matches(input_9, index, inv_number):
            return found_match

print("9.2")
print(
    contiguous_interval := contiguous_search(input_9, sum_finder(input_9, 25)[0]),
    max(contiguous_interval) + min(contiguous_interval)
)

# PROBLEM 9

input_10 = [0] + ( tmp_inpt := sorted([int(charger) for charger in eat_input("10.txt")])) + [tmp_inpt[-1] + 3]

print("10.1")
print(
    [ input_10[index+1] - input_10[index] for index, charger in enumerate(input_10[:-1])].count(1) *
    [ input_10[index+1] - input_10[index] for index, charger in enumerate(input_10[:-1])].count(3)
)

print("10.2")
# This will take infinite time to run in the final example
def count_combinations(jmp_idx_map, vertice, memo_cache = {}):
    if vertice in memo_cache.keys():
        return memo_cache[vertice]

    if vertice == list(jmp_idx_map.keys())[-1]:
        count = 1
    else:
        count = functools.reduce(
            lambda acc, idx: acc + count_combinations(jmp_idx_map, idx, memo_cache),
            jmp_idx_map[vertice],
            0
        )

    memo_cache[vertice] = count

    return count

def get_jump_list(input_10):
    jmp_idx_map = {}
    for index, value in enumerate(input_10):
        jumping_idxs = [sub_idx for sub_idx, sub_value in enumerate(input_10[index+1:], start=index + 1) if sub_value <= value + 3]
        jmp_idx_map[index] = jumping_idxs

    jolt_combinations = count_combinations(jmp_idx_map, list(jmp_idx_map.keys())[0])
    return jolt_combinations


pp(
    get_jump_list(input_10)
)
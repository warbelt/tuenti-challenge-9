import operator
from itertools import permutations


operations_dict = {
    operator.add: '+',
    operator.sub: '-',
    operator.mul: '*'
}
k2w_dict = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000
}


def get_possible_numbers_from_unordered_kanji(kanji: str) -> list:
    """
    Returns all possible (valid) roman numbers that can be created from reordering the given kanji
    :param kanji:
    :return:
    """
    western_numbers = [k2w_dict[x] for x in kanji]
    possible_numbers = []

    # Since numbers from 1 to 9 can be at last position, we need to add "1" to the possible multipliers
    multipliers = sorted([number for number in western_numbers if number in (10, 100, 1000, 10000)] + [1], reverse=True)
    simples = [number for number in western_numbers if number in (1, 2, 3, 4, 5, 6, 7, 8, 9)]

    # If there are more multipliers than simple numbers, add Nones to represent the multiplier by itself
    len_difference = len(multipliers) - len(simples)
    if len_difference > 0:
        for _ in range(len_difference):
            simples.append(None)

    # Try every possible combination of simple numbers and add it to the possible numbers list if it is legal
    for perm in permutations(simples):
        number = 0
        # 10000 must be preceded by a number between 1..9, it would be illegal if there was a 10000 by itself
        if multipliers[0] == 10000:
            if perm[0] is None:
                continue
        for multiplier, simple in zip(multipliers, perm):
            if simple == 1 and multiplier not in [1, 10000]:
                continue
            elif simple is not None:
                # If simple were a none, the multiplier (10,100...) would be by itself (next elif)
                number += multiplier * simple
            elif multiplier > 1:
                # If multiplier is 1 and simple is None, don't add anything since there is no "1" at that position
                number += multiplier

        possible_numbers.append(number)

    return possible_numbers


def find_correct_operation(first: list, second: list, third: list) -> tuple:
    """
    Returns the first combination of operands from first, second and third such as third can be obtained by applying
    one of the operators. Also returns the operator
    :param first: list possible first operands
    :param second: list possible second operands
    :param third: list possible results
    :return: tuple (first operand, operator, second operand, result)
    """
    # Try every possible combination of operands and operator until a result is in the possible results
    for first_possible_number in first:
        for second_possible_number in second:
            for op in operations_dict.keys():
                result = op(first_possible_number, second_possible_number)
                if result in third:
                    return first_possible_number, op, second_possible_number, result


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r', encoding="utf8") as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for i, case in enumerate(range(n_cases)):
        operation = input_data.pop(0).strip()
        # Split line in the three japanese numbers
        first_kanji, second_kanji, third_kanji = operation.replace("=", "OPERATOR").split(" OPERATOR ")

        # Create a list of all valid roman numbers that can be created from the unordered kanji
        first_possible_numbers, second_possible_numbers, third_possible_numbers = map(
            get_possible_numbers_from_unordered_kanji,
            [first_kanji, second_kanji, third_kanji]
        )

        # Guess the actual combination of operands and operator, from trying every possibility
        actuals = find_correct_operation(first_possible_numbers,
                                         second_possible_numbers,
                                         third_possible_numbers)

        # write real operation to file
        real_operation = f"{actuals[0]} {operations_dict[actuals[1]]} {actuals[2]} = {actuals[3]}"
        f_out.write(f"Case #{i + 1}: {real_operation}\n")

import math


def go_shopping_for_tortillas(with_onion: int, without_onion: int) -> int:
    """
    Returns the total of tortillas needed to satisfy both onion lovers and heathens
    :param with_onion: number of people that like tortilla with onion
    :param without_onion: number of people that like tortilla without onion
    :return: total number of tortillas needed
    """
    return math.ceil(with_onion / 2) + math.ceil(without_onion / 2)


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f:
    lines = f.readlines()
n_cases = int(lines[0])
cases = lines[1:n_cases + 1]  # In case more than {n_cases} lines follow the first one, we take only {n_cases}

with open(output_file, "w+") as f:
    for index, case in enumerate(cases):
        case_as_list_of_int = list(map(int, case.split()))
        tortillas = go_shopping_for_tortillas(*case_as_list_of_int)

        f.write(f'Case #{index + 1}: {tortillas}\n')

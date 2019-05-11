from functools import reduce
from math import gcd


def reduce_fraction(dividend: int, divisor: int) -> tuple:
    """
    Returns an irreducible fraction of both dividend and divisor
    :param dividend:
    :param divisor:
    :return: tuple of int dividend and divisor of the irreductible fraction
    """
    greatest_common_divisor = gcd(divisor, dividend)
    return int(dividend/greatest_common_divisor), int(divisor/greatest_common_divisor)


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for index, case in enumerate(range(n_cases)):
        number_of_elements = int(input_data.pop(0))
        elements = list(map(int, input_data.pop(0).split()))  # Load fragment of list of candies as a List of ints

        # By multiplying every number in the list, we assure that the result is a multiple of every number in the list
        # This way we have calculated a multiple of X.
        # We don't need to compute the exact number X, since we are calculating an average, the result will be the same
        repetitions = reduce(lambda x, y: x * y, elements)

        # As a given number 'n' of candies is repeated n times, each of those repetitions is worth one candy
        candies = number_of_elements * repetitions

        # An element of value N, in a list repeated Y times, is going to also appear Y times
        # Dividing Y/N gives the number of groups of N of that element, which is the number of people that ate N candies
        people = sum([int(repetitions/element) for element in elements])

        # Get the irreducible fraction
        reduced_candies, reduced_people = reduce_fraction(candies, people)

        # Save in file
        f_out.write(f"Case #{index+1}: {reduced_candies}/{reduced_people}\n")


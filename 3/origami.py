def unfold(punches: list, direction: str, w: int, h: int) -> list:
    """
    Returns a list of resultant punches after unfolding a paper with a given set of punches, in a given direction
    :param punches: list coords for all punches in [x, y] format
    :param direction: str direction in which the paper is unfolded, must be in ('T', 'B', 'R', 'L')
    :param w: int width of the paper before unfolding
    :param h: height of the paper before unfolding
    :return:
    """
    unfolded_punches = []  # this is where the punches after unfolding are saved
    for punch in punches:
        x, y = punch  # unpack coordinates for legibility purposes
        if direction == "T":
            # Each punch is mirrored on top, then new (0, 0) point is updated by adding h to y axis
            unfolded_punches.append([x, h - 1 - y])
            unfolded_punches.append([x, y + h])
        if direction == "B":
            # Each punch is mirrored on bottom, (0,0) stays the same
            unfolded_punches.append([x, y])
            unfolded_punches.append([x, h*2 - 1 - y])
        if direction == "R":
            # Each punch is mirrored on right, (0,0) stays the same
            unfolded_punches.append([x, y])
            unfolded_punches.append([w*2 - 1 - x, y])
        if direction == "L":
            # Each punch is mirrored on left, then new (0, 0) point is updated by adding w to x axis
            unfolded_punches.append([w - 1 - x, y])
            unfolded_punches.append([x + w, y])

    return unfolded_punches


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for index, case in enumerate(range(n_cases)):
        # Initial attributes
        wide, tall, folds, punches = list(map(int, input_data.pop(0).split()))
        # Folds as a list of chars
        folds_list = [input_data.pop(0).strip() for _ in range(folds)]
        # Punches as a list of ints
        punches_list = [list(map(int, input_data.pop(0).split())) for _ in range(punches)]

        for fold in folds_list:
            punches_list = unfold(punches_list, fold, wide, tall)
            # update paper dimensions
            if fold in ['T', 'B']:
                tall *= 2
            else:
                wide *= 2

        # punches list is unordered, sort it first by x and then by y axis
        punches_list.sort(key=lambda punch: (punch[0], punch[1]))

        f_out.write(f"Case #{index+1}:\n")
        for x, y in punches_list:
            f_out.write(f"{x} {y}\n")

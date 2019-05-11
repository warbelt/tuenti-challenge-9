keyboard = [
    ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
    ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
    ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
    ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '-']
]


def calculate_shift(base_keyboard: dict, code: str, base_char: str) -> tuple:
    """
    Retruns the vertical and horizontal shift on a keyboard needed to transform the code character back into the base
    :param base_keyboard: list of list representation of the keyboard in rows of characters
    :param code: str character that is the result of shifting base char
    :param base_char: str character that has been shifted into code
    :return: tuple shift in terms of down, right
    """
    code_pos_x, code_pos_y = get_position_in_keyboard(base_keyboard, code)
    base_pos_x, base_pos_y = get_position_in_keyboard(base_keyboard, base_char)

    shift = (base_pos_x - code_pos_x, base_pos_y - code_pos_y)

    return shift


def get_position_in_keyboard(keyboard: dict, character: str) -> tuple:
    """
    Returns the position in the keyboard that the character occupies
    :param keyboard:
    :param character:
    :return: tuple containing position in terms of (x, y)
    """
    for y_index, row in enumerate(keyboard):
        if character in row:
            return row.index(character), y_index


def shift_keyboard(base_keyboard: dict, down: int, right: int) -> dict:
    """
    Returns a dictionary which maps the keys of a shifted keyboard to the keys of the original keyboard
    :param base_keyboard: list of list representation of the keyboard in rows of characters
    :param down: int number of positions down that the keyboard has been shifted
    :param right: int number of positions to the right that the keyboard has been shifted
    :return: dict map of shifted keys to new keys
    """
    # Whitespaces remain unchanged
    shifting_map = {' ': ' '}

    for y_index, row in enumerate(keyboard):
        for x_index, character in enumerate(row):
            new_x_index = (x_index - right) % 10
            new_y_index = (y_index - down) % 4

            shifting_map[base_keyboard[new_y_index][new_x_index]] = keyboard[y_index][x_index]

    return shifting_map


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for index, case in enumerate(range(n_cases)):
        sender = input_data.pop(0).strip()
        message = input_data.pop(0).strip()

        # Get the shift tneeded to apply to the keyboard to decrypt the message
        shift = calculate_shift(keyboard, message[-1], sender)

        # Create a map to shift back the message
        shifted_keyboard = shift_keyboard(keyboard, shift[1], shift[0])

        # Shift the message back
        message = ''.join([shifted_keyboard[character] for character in message])

        f_out.write(f"Case #{index+1}: {message}\n")


import math


ENCODING = "ISO_8859_1"
MIN_CHAR = 48
MAX_CHAR = 122
HASH_LENGTH = 16


def hash_message(message: str) -> list:
    """
    Returns the hash of a string, represented as a list of integers corresponding to the ascii codes of its characters
    :param message: str message to hash
    :return: list hashed message as list of ints
    """
    # Create bytearray of zeroes as base for the hash
    int_hash = [0 for _ in range(HASH_LENGTH)]
    encoded_message = bytearray(message.encode(ENCODING))
    int_encoded_message = [c for c in encoded_message]

    for position, character in enumerate(int_encoded_message):
        int_hash[position % HASH_LENGTH] = (int_hash[position % HASH_LENGTH] + character) % 256

    return int_hash


def shift_list_right(l: list, positions: int) -> list:
    """
    Shifts all members of a list one position to the right, and moves the last item to the first position
    :param l:
    :param positions:
    :return:
    """
    temp = l[:]  # so that l remains unchanged
    for _ in range(positions):
        temp.insert(0, temp.pop())
    return temp


def is_distance_within_range(distance: int, min_advance: int, max_advance: int) -> bool:
    """
    Returns true if distance can be expressed as a sum of integers between min_advance and max_advance
    :param distance:
    :param min_advance:
    :param max_advance:
    :return: bool
    """
    if distance > max_advance:
        return False
    if distance < min_advance:
        return is_distance_within_range(distance + 256, min_advance, max_advance)
    return True


def are_hashes_within_range(base_hash: list, target_hash: list, shift: int, padding: int) -> bool:
    """
    Returns true if a given base hash, can be converted into target_hash when its origin string is added
    a number "shift" of characters. Those characters must be between MIN_CHAR and MAX_CHAR in the ascii table
    :param base_hash: list
    :param target_hash: list
    :param shift: int number of characters that can be added
    :param padding: int padding of NULL character that was prepended to the string that created base_hash
    :return: bool
    """
    # If {shift} characters are added to the string, the hash is shifted that many positions to the right
    shifted_base_hash = shift_list_right(base_hash, shift)
    # Calculate distances between the shifted hash and the target hash.
    # This are the distances that need to be covered with the added characters
    distances_list = [(x - y) % 256 for x, y in zip(target_hash, shifted_base_hash)]

    # We need to know the position where the characters are going to start being added
    # To do this, we undo the padding added to the string
    # Then, we get the actual distances starting from the first character added by shifting the distances list
    shift_needed_to_counter_padding = HASH_LENGTH - padding
    distances_list_with_reversed_padding = shift_list_right(distances_list, shift_needed_to_counter_padding)

    # Check, position by position, if the distance can be covered with a number of characters
    # The {shift characters} is the total, so each position has an equal share of them
    for index, distance in enumerate(distances_list_with_reversed_padding):
        min_advance = MIN_CHAR * math.ceil((shift-index)/HASH_LENGTH)
        max_advance = MAX_CHAR * math.ceil((shift-index)/HASH_LENGTH)
        if is_distance_within_range(distance, min_advance, max_advance) is False:
            return False

    return True


def find_lowest_characters_to_cover_distance(amount: int, distance: int):
    """
    Returns a list of characters that cover {distance} when hashed
    Characters are ordered so that the string is of lowest value alphabetically (i.e., lowest characters first)
    :param amount: int number of characters that need to be added
    :param distance: int distance to be covered
    :return: list characters that need to be added to cover a distance
    """
    characters = []
    for index, _ in enumerate(range(amount)):
        # Since at least every position needs a MIN_CHAR, add 256 to distance if needed
        if distance < (amount-index) * MIN_CHAR:
            distance += 256
        # Take a MAX_CHAR if it leaves enough distance left for every other member to take at least a MIN CHAR
        if distance >= (((amount-index-1) * MIN_CHAR) + MAX_CHAR):
            characters.insert(0, chr(MAX_CHAR))
            distance -= MAX_CHAR
        # If not, just take what is available leaving a MIN CHAR for the rest
        else:
            char_to_take = distance - ((amount-index-1) * MIN_CHAR)
            characters.insert(0, chr(char_to_take))
            distance -= char_to_take

    return characters


def zip_lists_of_chars_into_string(lists_of_chars: list) -> str:
    """
    Zips the characters of all lists inside {lists_of_chsrs} into a single string
    :param lists_of_chars: list of list of char each list contais the characters to be added into the same position
    :return: str ziped characters
    """
    result = []
    total_chars = sum([len(l) for l in lists_of_chars])
    number_of_lists = len(lists_of_chars)

    for index in range(total_chars):
        result.append(lists_of_chars[index % number_of_lists].pop(0))

    return "".join(result)


def find_print_section(original: str, modified: str) -> str:
    """
    Returns the string that has to be added inside the print section, so that hash of {original} = hash of {modified}
    :param original:
    :param modified:
    :return:
    """
    original_hash = hash_message(original)
    # Find the index where the print section is going to be added
    print_section_position = modified.find("---") + 3
    # Calculate the hash of everything before the print section position for the fake message
    # The hash of that section can not be changed, so the hash of the rest of the message summed to this hash,
    # must equal the hash of the original hashed
    modified_pre_print_section_hash = hash_message(modified[:print_section_position])

    # This is the hash that the second part of the message should have, so that summed to the hash of the first part
    # would equal the hash of the original string
    post_print_needed_hash = [(x - y) % 256 for x, y in zip(original_hash, modified_pre_print_section_hash)]

    # In order to properly calculate hashes, the second part must start at the index where the first part ends
    # For this, a padding of Null characters is added (those have 0 value for hashing purposes)
    padding = '\0' * (print_section_position % HASH_LENGTH)
    padded_post_print_section_message = padding + modified[print_section_position:]
    padded_post_print_section_message_hash = hash_message(padded_post_print_section_message)

    # Find the minimum amount of characters that need to be added to the print section in order to do the hash collision
    # This is done by iteratively checking if it's possible with a certain number of chars, starting by 0
    found = False
    shift = 0

    while found is False:
        if are_hashes_within_range(padded_post_print_section_message_hash, post_print_needed_hash, shift, len(padding)):
            found = True
        else:
            shift += 1

    # Shift the second part of the message (without the print section) to the position it will be
    # after adding the print the print section
    shifted_post_print_section_to_final_position = shift_list_right(padded_post_print_section_message_hash, shift)

    # We know the number of characters that will be added to the print section
    # Now calculate the distance that needs to be covered in each modified_hash position so that both hashes are equal
    final_distances = [(x - y) % 256 for x, y in zip(post_print_needed_hash,
                                                     shifted_post_print_section_to_final_position)]

    # For every hash position, calculate the characters to be added to the print section
    # Those characters will be {HASH_LEN} positions apart in the final string and will be summed into the
    # same position of the hash
    starting_position = len(padding)
    print_section_lists = []

    for index in range(HASH_LENGTH):
        position = (starting_position + index) % HASH_LENGTH
        number_of_chars_added_to_hash_position = math.ceil((shift-index)/HASH_LENGTH)
        distance_to_cover = final_distances[position]

        print_section_lists.append(find_lowest_characters_to_cover_distance(number_of_chars_added_to_hash_position,
                                                                            distance_to_cover))

    # Finally create a string, interpolating the characters of each position
    print_section = zip_lists_of_chars_into_string(print_section_lists)
    return print_section


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for i, case in enumerate(range(n_cases)):
        n_lines_original = int(input_data.pop(0))
        card_original = ''.join([input_data.pop(0).strip() for _ in range(n_lines_original)])
        n_lines_modified = int(input_data.pop(0))
        card_modified = ''.join([input_data.pop(0).strip() for _ in range(n_lines_modified)])

        print_section_message = find_print_section(card_original, card_modified)

        f_out.write(f"Case #{i + 1}: {print_section_message}\n")

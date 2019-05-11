def infer_rules(words, ruleset):
    """
    Recursively infer character order rules based on order of words.
    After generating all possible rules with the words recieved, it will infer_rules on groups
    of words that start with the same character
        dad   -  first infer rules for      -     c(ab)    -   infer rules for
        bad   -  whole words, then make     -     c(da)    -   [ab, da]
        cab   -  subgroups
        cda
    :param words: list Ordered words found on the documents
    :param ruleset: dict Rules of order in which key is a character and value is a set of all characters of higher value
    :return:
    """
    # Different characters hat appear in first place of words, ordered from lower value to higher
    ordered_first_level_characters = []

    # Traverse list of words to fill the first level characters list. Could be done with a set and a comprehensive list
    # but order is important
    for word in words:
        if word[0] not in ordered_first_level_characters:
            ordered_first_level_characters.append(word[0])

    # Traverse ordered list of characters and add rules to dictionary
    # For a certain character in the list, a rule will be that every character that appears after it has a higher value
    for index, character in enumerate(ordered_first_level_characters):
        higher_chars_set = ordered_first_level_characters[index + 1:]
        ruleset[character] = ruleset[character].union(higher_chars_set)

        # If there are more than one word starting with this character, more rules can be infered
        # by removing the first character
        children_words = [word[1:] for word in words if (word[0] == character and len(word) > 1)]
        if len(children_words) > 1:
            infer_rules(children_words, ruleset)


def add_characters_to_alphabet(ruleset, alphabet):
    """
    Order all characters in the alphabet based on the infered ruleset.
        - Looks for the character that has no other character of a higher value (i.e.: it's ruleset is empty)
        - Add that character to the alphabet at last position
        - Remove the character rules from the ruleset, and from the rules of other characters
        - Recursive call to get next character

        - If there is not exactly ONE character with no characters of higher value there is a tie (no solution)
    :param ruleset:
    :param alphabet:
    :return:
    """
    last_character = [key for key, value in ruleset.items() if value == set()]
    # There must obly be one character without characters greater than it. If there are more or 0, there is no solution
    if len(last_character) == 1:
        ruleset.pop(last_character[0])
        for key, value in ruleset.items():
            try:
                ruleset[key].remove(last_character[0])
            except KeyError:
                pass
        if len(ruleset) > 0:
            # Recursive call. If it returns ambiguous, bubble it to the top
            if add_characters_to_alphabet(ruleset, alphabet) == "AMBIGUOUS":
                return "AMBIGUOUS"

        alphabet.append(last_character[0])

    else:  # if there are more than 1 characters without greater characters, it's a tie
        return "AMBIGUOUS"


input_file = "submitInput.txt"
output_file = input_file.replace("Input", "Output")

with open(input_file, 'r') as f_in:
    input_data = f_in.readlines()

n_cases = int(input_data.pop(0))

with open(output_file, 'w+') as f_out:
    for index, case in enumerate(range(n_cases)):
        number_of_words = int(input_data.pop(0))
        words = [input_data.pop(0).strip() for _ in range(number_of_words)]

        # Create a set of all different characters used
        characters = set([char for word in words for char in word])
        # Empty dictionary of rules. Key is a character, value (the rule) is a set of the character with higher value
        rules_dict = {character: set() for character in characters}

        # Fill the dictionary entries with the rules that can be inferred from the input
        infer_rules(words, rules_dict)

        # Try to order the alphabet based on inferred rules
        alphabet = []
        status = add_characters_to_alphabet(rules_dict, alphabet)

        if status == "AMBIGUOUS":
            f_out.write(f"Case #{index+1}: AMBIGUOUS\n")
        else:
            alphabet_string = " ".join(alphabet)
            f_out.write(f"Case #{index+1}: {alphabet_string}\n")

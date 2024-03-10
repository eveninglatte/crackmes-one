import random


def check_key(key: list[int]) -> bool:
    if ((key[19] ** key[1]) - (key[0] ** key[2]) < 0 and
        key[0] - key[19] > 0 and
        key[12] + key[7] < 140 and
        key[10] * key[8] <= key[16] * key[4]):
        return True


def get_final_check_value(key: list[int]) -> int:
    final_check = 0
    last = 1

    for letter in key:
        final_check += letter * last
        last = letter

    return final_check


# generate a random key that passes the checks in check_key
# and whose final_check value is in range [153_000 - (253 + 33), 153_000 - 33]
def gen_random_key() -> list[int]:
    unsafe_letters = [0, 1, 2, 4, 7, 8, 10, 12, 16, 19]
    safe_letters = [3, 5, 6, 9, 11, 13, 14, 15, 17, 18, 20, 21, 22, 23, 24]
    rand_key = [33 for i in range(25)]

    attempts = 0
    while True:
        for index in unsafe_letters:
            rand_key[index] = random.randint(33, 126)
        if check_key(rand_key) and get_final_check_value(rand_key) < 153_000:
            break
        else:
            attempts += 1

    for index in safe_letters:
        for i in range(33, 126):
            rand_key[index] += 1
            # 253 is the biggest change in the value of final_check
            # that adding a 1 to a letter can make (126 ** 2 - 125 ** 2)
            # this is to ensure we don't go over 153_000
            # 33 is the lowest value of username[0] * multiplier
            # this is to ensure we are able to pass the check afterwards
            if get_final_check_value(rand_key) > 153_000 - (251 + 33):
                return rand_key


def gen_username(final_check_value: int) -> list[int]:
    username_len = 4
    multiplier = -1

    username_1st_lett = 153_000 - final_check_value
    # if we're not able to fit everything into username[0] we need to change the multiplier
    if username_1st_lett > 126:
        # check every possible username[0] and find a matching multiplier to equal final_check_value
        for i in range(33, 126):
            if (username_1st_lett / i).is_integer():
                multiplier = username_1st_lett // i
                username_1st_lett = i
                break
        # if we weren't able to find any suitable matches, we need to generate a new key
        if multiplier == -1:
            return []
    else:
        # we don't need any multiplier tweaking
        multiplier = 1

    # generate a username that matches the multiplier value
    while True:
        username = [random.randint(33, 126) for i in range(username_len)]
        if username[2] > username[-1]:
            if (username[1] + (username[2] / username_len) - username[-1]) == multiplier:
                break
        elif username[2] < username[-1]:
            if (username[1] + (username[-1] / username_len) - username[2]) == multiplier:
                break
        else:
            if username[1] + username_len == multiplier:
                break

    username[0] = username_1st_lett

    return username


# returns a valid username and serial key pair
def gen_credentials():
    rand_key = gen_random_key()

    username = gen_username(get_final_check_value(rand_key))
    while not username:
        # need to generate a new key
        rand_key = gen_random_key()
        username = gen_username(get_final_check_value(rand_key))

    username = "".join(chr(i) for i in username)
    serial_key = "".join(chr(i) for i in rand_key)

    return serial_key, username


key, username = gen_credentials()
print(f"Key is {key}")
print(f"Username is {username}")

import string
import random


def get_pass(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    big_letters = string.ascii_uppercase
    punct = string.punctuation
    result_str = "".join(random.choice(letters) for i in range(length))
    result_str += "".join(random.choice(big_letters) for i in range(length))
    result_str += "".join(random.choice(punct) for i in range(length))
    return result_str

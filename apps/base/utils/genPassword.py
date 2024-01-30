import string
import random


def genPassword(length):
    letters    = string.ascii_lowercase
    result     = ''.join(random.choice(letters) for i in range(length))
    return result
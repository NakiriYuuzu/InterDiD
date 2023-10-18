import random


def generate_unique_code():
    return "{:06d}".format(random.randint(0, 999999))
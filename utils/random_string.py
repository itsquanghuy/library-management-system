import random
import string


def generate_random_string(size=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=size))

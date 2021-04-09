from hashlib import sha256


def hash256(text):
    return str(sha256(text.encode()).hexdigest())

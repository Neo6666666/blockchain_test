import json
from hashlib import sha256


def hash_string_256(string):
    """
    Hashed given string.
    Params:
        -string: str
    Return:
        -str
    """
    return sha256(string).hexdigest()

def hash_block(block):
    """Return hash of given block.
    Params:
        -block: dict()
    """
    return hash_string_256(json.dumps(block, sort_keys=True).encode())  #return string from json converted block
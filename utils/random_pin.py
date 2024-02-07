# Depreciated
import string
from random import choice

chars = string.digits

def randomPin(length: int) -> str:
    return ''.join(choice(chars) for _ in range(length))
import random


def generate_invite_token(length: int = 4) -> str:
    return ''.join(random.choices('0123456789', k=length))

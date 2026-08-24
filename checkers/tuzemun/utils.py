import random
import string

def generate_str(length=None):
    """Generate a random string of fixed length."""
    if not length:
        length = random.randint(10, 20)
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_extended_str(length=None):
    """Generate a random string of fixed length."""
    if not length:
        length = random.randint(10, 20)
    letters = string.ascii_letters + string.digits + r'!#$%&()*+,-./:;<=>?@[]^_`{|}~'
    return ''.join(random.choice(letters) for _ in range(length))

def generate_email(length1=None, length2=None):
    if not length1:
        length1 = random.randint(7, 15)
    if not length2:
        length2 = random.randint(5, 15)
    a = generate_str(length=length1)
    c = random.choice(['ru', 'com', 'net', 'org', 'io', 'it', 'test', 'lol'])
    b = generate_str(length=length2)
    return f'{a}@{b}.{c}'

def generate_passport():
    return ''.join(random.choice('1234567890') for _ in range(10))

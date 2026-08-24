import random
import string
import time


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))


def random_date(start='1/1/1970 12:00 PM', end='1/1/2032 12:00 PM'):
    return str_time_prop(start, end, '%d/%m/%Y %I:%M %p', random.random())


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


def generate_passport():
    return ''.join(random.choice('1234567890') for _ in range(10))

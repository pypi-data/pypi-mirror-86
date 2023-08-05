import binascii
import os
import random

from rest_framework_simplejwt.settings import api_settings


def generate_token(min_length=30, max_length=40):
    length = random.randint(min_length, max_length)

    return binascii.hexlify(
        os.urandom(max_length)
    ).decode()[0:length]


def generate_code(length=6):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return random.randint(range_start, range_end)


def set_up_signing_key(key):
    api_settings.SIGNING_KEY = key

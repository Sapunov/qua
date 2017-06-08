#!/usr/bin/env python3

import string
import random


chars = ''.join([
    string.ascii_letters,
    string.digits,
    '!#$%&()*+,-.:;<=>?@[]^_`{|}~'
])

secret_key = ''.join(
    [random.SystemRandom().choice(chars) for i in range(50)]
)

print(secret_key)

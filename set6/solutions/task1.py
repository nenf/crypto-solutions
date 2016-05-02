#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from checker import sha1
from gmpy2 import isqrt, is_square, invert, is_even
from itertools import izip


def multiplicative_inverse(a, b):
    return invert(long(a), long(b))


def fermat_factorization(n):
    if is_even(n):
        return 2, n / 2
    a = int(isqrt(n))
    while not is_square(pow(a, 2) - n):
        a += 1
    b = isqrt(pow(a, 2) - n)
    return a - b, a + b


def checker_rsa(value, hash_value):
    value = str(value)
    if hash_value != sha1(value):
        print "value {0} is incorrect".format(value)
        print "hash : {0} != {1}".format(hash_value, sha1(value))
        return False
    print "value {0} is correct".format(value)
    return True


if __name__ == "__main__":
    e = 739
    n = 850706101864878285731846786674155199

    p, q = fermat_factorization(n)
    phi = (p - 1) * (q - 1)
    d = multiplicative_inverse(e, phi)

    ph = "9b8d8099f56f0fa5fad115bb2ec75fa410733cc1"
    qh = "8b6ba85e0b30da318f2db808e67b2fe48a2a974c"
    dh = "e7c17d92198b74e15ae0feb4d47379e2e9c27643"

    for v, h in izip([p, q, d], [ph, qh, dh]):
        checker_rsa(v, h)

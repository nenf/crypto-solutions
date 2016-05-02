#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from itertools import izip
from gmpy2 import isqrt
from task1 import checker_rsa, multiplicative_inverse


def factorization(n):
    lim = int(isqrt(n))
    for p in xrange(2, lim):
        if n % p == 0:
            return p, n / p
    return None


if __name__ == "__main__":
    e = 281
    n = 328453897657

    p, q = factorization(n)
    phi = (p - 1) * (q - 1)
    d = multiplicative_inverse(e, phi)

    ph = "26d51a80cb5a14ea9a84f320fcf94cd41be61d58"
    qh = "98e6ef2fb038b2a9d94aa928a2211dc425687e8f"
    dh = "e689220495055aad7b25c29f2f210c3f4313d681"
    for v, h in izip([p, q, d], [ph, qh, dh]):
        checker_rsa(v, h)

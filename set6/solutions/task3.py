#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from gmpy2 import powmod


def cycle_attack(c, e, n):
    pow_attack = 1
    attack_c = 0
    while c != attack_c:
        prev_c = attack_c
        attack_c = powmod(c, pow(e, pow_attack), n)
        pow_attack += 1
    return prev_c


if __name__ == "__main__":
    e = 281
    n = 4355017067
    c = 1622284030

    m = cycle_attack(c, e, n)
    print "Message is : {0}".format(m)

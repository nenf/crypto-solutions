#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import checker_rsa, multiplicative_inverse
from sympy.solvers import solve
from sympy import Symbol
from itertools import izip



def solve_quadratic(a, b, c):
    x = Symbol('x')
    return solve(a * x ** 2 + b * x + c, x)


def make_next_fraction(fraction):
    (a, b) = fraction
    res = b / a
    a1 = b % a
    b1 = a
    return res, (a1, b1)


def make_continued_fraction(fraction):
    (a, b) = fraction
    v = [0]
    while not a == 1:
        r, fraction = make_next_fraction(fraction)
        (a, b) = fraction
        v.append(r)
    v.append(b)
    return v


def make_indexed_convergent(sequence, index):
    (a, b) = (1, sequence[index])
    while index > 0:
        index -= 1
        (a, b) = (b, sequence[index] * b + a)
    return (b, a)


def make_convergents(sequence):
    return [make_indexed_convergent(sequence, i) for i in range(len(sequence))]


def wiener_attack(n, e):
    d = 0
    conv = make_convergents(make_continued_fraction((e, n)))
    for frac in conv:
        (k, d) = frac
        if k == 0:
            continue
        phi = ((e * d) - 1) / k
        roots = solve_quadratic(1, -(n - phi + 1), n)
        if len(roots) == 2:
            p, q = roots[0] % n, roots[1] % n
            if p * q == n:
                return p, q


if __name__ == "__main__":
    e = 16251074822983150405499488256792777159
    n = 75847237140497705400017161474506490943

    p, q = wiener_attack(n, e)
    phi = (p - 1) * (q - 1)
    d = multiplicative_inverse(e, phi)

    ph = "01482f21d3547694b98626c7ba3ab486db60df60"
    qh = "d39f1ee974b0454dc63c40003f28eee28c493e5b"
    dh = "0b4313743091f97b0d1ef07fea2fc2270380c016"

    for v, h in izip([p, q, d], [ph, qh, dh]):
        checker_rsa(v, h)

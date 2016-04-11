#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from fractions import Fraction
from gmpy2 import gamma


class BlockFreqAnalyzer:
    def __init__(self, bit_string, block_size):
        self.bit_string = bit_string
        self.block_size = block_size
        self.len_bit_string = len(bit_string)
        self.count_blocks = self.len_bit_string / self.block_size

    @staticmethod
    def __split_nth_number(data, block_size):
        return [data[i:i + block_size] for i in range(0, len(data), block_size)]

    def __pi_compute(self):
        bit_list = self.__split_nth_number(self.bit_string, self.block_size)
        return [Fraction(sum(block), self.block_size) for block in bit_list]

    def __hi_compute(self, pi):
        summ = 0
        for i in range(self.count_blocks):
            summ += pow((pi[i] - Fraction(1, 2)), 2)
        return float(4 * self.block_size * summ)

    @staticmethod
    def __igamc(a, b):
        # integral from 0 to x (e^(-t) * t^(a-1) dt
        gamma_value = gamma(float(a) / 2.0) - gamma(float(b) / 2.0)

        # integral from 0 to inf (t^(z-1) * e^(-t) dt
        gamma_function = gamma(float(a) / 2.0)

        return 1 - (gamma_value / gamma_function)

    def analyze(self):
        pi = self.__pi_compute()
        hi = self.__hi_compute(pi)
        p_value = self.__igamc(float(self.count_blocks)/2, float(hi) / 2)

        if p_value < 0.01:
            print "Sequence is non-random"
            return False
        else:
            print "Sequence is random"
            return True

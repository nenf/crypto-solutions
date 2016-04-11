#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from random import randint
from numpy import roll


class Generator:
    def __init__(self, len_gamma):
        self.len_gamma = len_gamma
        self.len_first_lfsr = 17
        self.len_second_lfsr = 16
        self.len_third_lfsr = 15

    @staticmethod
    def __majority_function(b1, b2, b3):
        return (b1 & b2) ^ (b1 & b3) ^ (b2 & b3)

    @staticmethod
    def __rev_index(index, len_lfsr):
        return len_lfsr - index

    @staticmethod
    def __shift(stats):
        return list(roll(stats, 1))

    @staticmethod
    def __gen_bit_list(len_list):
        return [randint(0, 1) for _ in range(len_list)]

    def __step_first_lfsr(self, stats):
        n, k = self.len_first_lfsr, 3
        f = stats[self.__rev_index(n, self.len_first_lfsr)] ^ stats[self.__rev_index(k, self.len_first_lfsr)] ^ 1
        stats = self.__shift(stats)
        stats[self.__rev_index(n, self.len_first_lfsr)] = f
        return stats, stats[self.__rev_index(1, self.len_first_lfsr)]

    def __step_second_lfsr(self, stats):
        n, k, l, m = self.len_second_lfsr, 2, 3, 5
        f = stats[self.__rev_index(n, self.len_second_lfsr)] ^ stats[self.__rev_index(k, self.len_second_lfsr)] ^ stats[
            self.__rev_index(l, self.len_second_lfsr)] ^ stats[self.__rev_index(m, self.len_second_lfsr)] ^ 1
        stats = self.__shift(stats)
        stats[self.__rev_index(n, self.len_second_lfsr)] = f
        return stats, stats[self.__rev_index(1, self.len_second_lfsr)]

    def __step_third_lfsr(self, stats):
        n, k = self.len_third_lfsr, 1
        f = stats[self.__rev_index(n, self.len_third_lfsr)] ^ stats[self.__rev_index(k, self.len_third_lfsr)] ^ 1
        stats = self.__shift(stats)
        stats[self.__rev_index(n, self.len_third_lfsr)] = f
        return stats, stats[self.__rev_index(1, self.len_third_lfsr)]

    def threshold(self, tick):
        empty_stats_first_lfsr = self.__gen_bit_list(self.len_first_lfsr)
        empty_stats_second_lfsr = self.__gen_bit_list(self.len_second_lfsr)
        empty_stats_third_lfsr = self.__gen_bit_list(self.len_third_lfsr)

        stats_first_lfsr, b1 = self.__step_first_lfsr(empty_stats_first_lfsr)
        stats_second_lfsr, b2 = self.__step_second_lfsr(empty_stats_second_lfsr)
        stats_third_lfsr, b3 = self.__step_third_lfsr(empty_stats_third_lfsr)

        out = [self.__majority_function(b1, b2, b3)]
        for i in range(tick - 1):
            stats_first_lfsr, b1 = self.__step_first_lfsr(stats_first_lfsr)
            stats_second_lfsr, b2 = self.__step_second_lfsr(stats_second_lfsr)
            stats_third_lfsr, b3 = self.__step_third_lfsr(stats_third_lfsr)
            out.append(self.__majority_function(b1, b2, b3))
        return out
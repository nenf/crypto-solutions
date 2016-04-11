#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from frequency_analysis import BlockFreqAnalyzer
from gamma_generator import Generator


if __name__ == "__main__":
    block_size = 64
    len_bit_string = block_size * 10

    generator = Generator(len_bit_string)
    sequence = generator.threshold(len_bit_string)

    sequence_s = "".join(str(b) for b in sequence)
    print "Sequence is : {0}".format(sequence_s)

    print "Count 0 bits is : {0}".format(sequence_s.count("0"))
    print "Count 1 bits is : {0}".format(sequence_s.count("1"))

    freq_analyze = BlockFreqAnalyzer(sequence, block_size)
    freq_analyze.analyze()

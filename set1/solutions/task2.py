#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from itertools import izip


def xor_byte_array(l_hex1, l_hex2):
    return "".join([chr(ord(b1) ^ ord(b2)) for b1, b2 in izip(l_hex1, l_hex2)])


if __name__ == "__main__":
    hex_string1 = "8f29336f5e9af0919634f474d248addaf89f6e1f533752f52de2dae0ec3185f818c0892fdc873a69"
    hex_string2 = "bf7962a3c4e6313b134229e31c0219767ff59b88584a303010ab83650a3b1763e5b314c2f1e2f166"
    ascii_result = xor_byte_array(hex_string1.decode("hex"), hex_string2.decode("hex"))
    print ascii_result.encode("hex")

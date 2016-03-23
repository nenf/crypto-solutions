#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from itertools import cycle, izip


def xor_repeat_key(text, key):
    return "".join([chr(ord(c1) ^ ord(c2)) for c1, c2 in izip(text, cycle(key))])

if __name__ == "__main__":
    text = "Never trouble about trouble until trouble troubles you!"
    key = "ICE"
    print xor_repeat_key(text, key).encode("hex")

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from enchant import Dict
from string import printable

dict_eng = Dict("en_US")


def is_eng_text(text, limit=90):
    if not all(word in printable for word in text):
        return False
    text_split = text.split()
    count_words = len(text_split)
    count_eng_words = 0
    for word in text_split:
        if dict_eng.check(word):
            count_eng_words += 1
    if count_eng_words == 0:
        return False
    percentage = (100 * count_eng_words) / float(count_words)
    if percentage >= limit:
        return True
    return False


def brute_one_symbole_xor(s_hex):
    for key in range(0, 255):
        byte_key = hex(key)[2:].zfill(2).decode("hex")
        message = "".join([chr(ord(byte_ct) ^ ord(byte_key)) for byte_ct in s_hex.decode("hex")])
        if is_eng_text(message):
            print message.rstrip()


if __name__ == "__main__":
    hex_string = "191f1911160b0c580c101d581d0e1114583f1914191b0c111b583d1508110a1d56"
    brute_one_symbole_xor(hex_string)

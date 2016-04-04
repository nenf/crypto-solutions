#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os import path
from string import printable
from task5 import xor_repeat_key

frequency = {"a": 834, "b": 154, "c": 273, "d": 414, "e": 1260, "f": 203, "g": 192, "h": 611, "i": 671, "j": 23,
             "k": 87, "l": 424, "m": 253, "n": 680, "o": 770, "p": 166, "q": 9, "r": 568, "s": 611, "t": 937, "u": 285,
             "v": 106, "w": 234, "x": 20, "y": 204, "z": 6, " ": 2320}


def score(text):
    ret = 0
    for c in text.lower():
        if c in frequency:
            ret += frequency[c]
    return ret


def single_xor_decode(string, skip_len):
    string = string.encode("hex")
    cur_best = 0
    cur_best_key = 0
    for i in range(256):
        c = "%x" % (int(string, 16) ^ int((hex(i)[2:]) * len(string), 16))
        if len(c) % 2 != 0:
            c = "0" + c
        c = c.decode("hex")[skip_len:]
        if not all(word in printable for word in c):
            continue
        if score(c) > cur_best:
            cur_best = score(c)
            cur_best_key = i
    return chr(cur_best_key)


def normalized_hamming_distance(data, length):
    ham_sum = 0
    numbers_blocks = len(data) / length - 1
    for i in range(numbers_blocks):
        # get blocks size length and exec hamming_distance
        ham_sum += hamming_distance(data[(i + 0) * length:(i + 1) * length], data[(i + 1) * length:(i + 2) * length])
    ham_avg = float(ham_sum) / numbers_blocks
    return ham_avg / length


def hamming_distance(hex_data1, hex_data2):
    xor_res = int(hex_data1.encode("hex"), 16) ^ int(hex_data2.encode("hex"), 16)
    return bin(xor_res)[2:].count("1")


def guess_key_size_xor_cipher(data_bytes, min_key_size, max_key_size):
    best_hamming_dist = 99999.0
    guess_key_size = None
    for key_size in range(min_key_size, max_key_size):
        ham = normalized_hamming_distance(data_bytes, key_size)
        if ham < best_hamming_dist:
            best_hamming_dist = ham
            guess_key_size = key_size
    return guess_key_size


if __name__ == "__main__":
    path_to_task = path.join("..", "Lab0_app", "Lab0_Tasks", "breakRepeatedKeyXor.txt")
    with open(path_to_task, "r") as detect_xor_file:
        data = detect_xor_file.read().decode("base64").rstrip()

    # Read this http://trustedsignal.blogspot.ru/2015/06/xord-play-normalized-hamming-distance.html
    key_size = guess_key_size_xor_cipher(data, 2, 40)

    # elements - every i bytes in data, every block key_size size
    split_data = [data[i::key_size] for i in range(key_size)]

    key = "".join([single_xor_decode(d, len(d)) for d in split_data])
    print "Key is: {0}\n".format(key)

    print xor_repeat_key(data, key)

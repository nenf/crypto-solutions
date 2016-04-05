#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7
from task3 import AESCipher
from random import randint
from task3 import split_nth_chars

cipher_mode = ""
block_size = 16


def rand_data(length=16):
    return "".join(chr(randint(0, 255)) for _ in range(length))


def encryption_oracle(data):
    global cipher_mode
    pkcs7 = PKCS7(block_size)
    key = rand_data()
    data = pkcs7.padding(rand_data(randint(5, 10)) + data + rand_data(randint(5, 10)))
    if randint(0, 1) == 0:
        cipher_mode = "CBC"
        iv = rand_data()
        aes = AESCipher(key)
        return aes.cbc_encrypt(data, iv)
    else:
        cipher_mode = "ECB"
        aes = AESCipher(key)
        return aes.ecb_encrypt(data)


def is_repeat_blocks(cipher_text):
    blocks = split_nth_chars(cipher_text, block_size)
    if len(set(blocks)) != len(blocks):
        return True
    return False


def run_tests(tests_count=10, count_blocks=5):
    plain_text = chr(randint(0, 255)) * (count_blocks * block_size)
    for i in range(tests_count):
        cipher_text = encryption_oracle(plain_text)
        if is_repeat_blocks(cipher_text):
            print "Probably mode is ECB (Actually mod is {0})".format(cipher_mode)
        else:
            print "Probably mode is CBC (Actually mod is {0})".format(cipher_mode)


if __name__ == "__main__":
    run_tests()

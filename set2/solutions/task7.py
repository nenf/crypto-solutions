#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7
from task3 import AESCipher, split_nth_chars
from task4 import rand_data
from random import randint
from fractions import gcd


base64_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBj" \
                "YW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBo" \
                "aQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
add_data = base64_string.decode("base64")

key = rand_data()
aes = AESCipher(key)


def formatting_data(data):
    pkcs7 = PKCS7()
    data = pkcs7.padding(rand_data(randint(16, 100)) + data + add_data)
    return data


def oracle_encryption(data):
    return aes.ecb_encrypt(formatting_data(data))


def get_block_size():
    length = 0
    for i in range(100):
        attack_cipher_text = aes.ecb_encrypt(formatting_data("A" * randint(0, i)))
        length = gcd(len(attack_cipher_text), length)
    return length


def encrypt_and_purification(data, block_size=16):
    while True:
        cipher_text = oracle_encryption("\xFF" * 3 * block_size + data)
        block_cipher_text = split_nth_chars(cipher_text, block_size)
        for i in range(len(block_cipher_text) - 2):
            if block_cipher_text[i] == block_cipher_text[i + 1] \
                    and block_cipher_text[i + 1] == block_cipher_text[i + 2]:
                return cipher_text[(i + 3) * block_size:]


def brute_one_symbol(block_size, plain_text):
    attack_prefix_len = (block_size - (1 + len(plain_text))) % block_size
    attack_prefix = "A" * attack_prefix_len

    block_len_for_test = len(attack_prefix) + len(plain_text) + 1
    block_for_test = encrypt_and_purification(attack_prefix)[:block_len_for_test]

    for byte in range(256):
        attack_text = attack_prefix + plain_text + chr(byte)
        brute_block = encrypt_and_purification(attack_text)[:block_len_for_test]
        if block_for_test == brute_block:
            return chr(byte)
    return ""

if __name__ == "__main__":
    block_size = get_block_size()
    pkcs7 = PKCS7(block_size)
    len_cipher_text = len(encrypt_and_purification("", block_size))

    plain_text = ""
    for i in range(len_cipher_text):
        plain_text += brute_one_symbol(block_size, plain_text)
        print "{0}/{1}".format(i, len_cipher_text)
    print pkcs7.unpadding(plain_text)

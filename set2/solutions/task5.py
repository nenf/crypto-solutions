#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7
from task3 import AESCipher
from task4 import rand_data

base64_string = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBj" \
                "YW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBo" \
                "aQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
add_data = base64_string.decode("base64")

key = rand_data()
aes = AESCipher(key)


def formatting_data(data):
    pkcs7 = PKCS7()
    return pkcs7.padding(data + add_data)


def get_block_size():
    data_for_attack = ""
    previous_len = None
    while True:
        encrypted_data = aes.ecb_encrypt(formatting_data(data_for_attack))
        data_for_attack += "A"
        encrypted_data_len = len(encrypted_data)
        if previous_len and encrypted_data_len > previous_len:
            return encrypted_data_len - previous_len
        else:
            previous_len = encrypted_data_len


def brute_one_symbol(block_size, plain_text):
    attack_prefix_len = (block_size - (1 + len(plain_text))) % block_size
    attack_prefix = "A" * attack_prefix_len

    block_len_for_test = len(attack_prefix) + len(plain_text) + 1
    block_for_test = aes.ecb_encrypt(formatting_data(attack_prefix))[:block_len_for_test]

    for byte in range(256):
        attack_text = attack_prefix + plain_text + chr(byte)
        brute_block = aes.ecb_encrypt(formatting_data(attack_text))[:block_len_for_test]
        if block_for_test == brute_block:
            return chr(byte)
    return "\n"

if __name__ == "__main__":
    block_size = get_block_size()
    pkcs7 = PKCS7(block_size)
    len_cipher_text = len(aes.ecb_encrypt(formatting_data("")))

    plain_text = ""
    for i in range(len_cipher_text):
        plain_text += brute_one_symbol(block_size, plain_text)
    print pkcs7.unpadding(plain_text)

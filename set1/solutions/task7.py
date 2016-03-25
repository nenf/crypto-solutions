#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os import path
from Crypto.Cipher import AES
from hashlib import md5


def original_key(key_string, salt, key_length):
    sum_digest = ""
    while len(sum_digest) < key_length + AES.block_size:
        sum_digest += md5(sum_digest + key_string + salt).digest()
    return sum_digest[:key_length]


def aes_ecb_decrypt(ct, key_string):
    salt = ct[:AES.block_size][len('Salted__'):]
    key = original_key(key_string, salt, len(key_string))
    aes_obj = AES.AESCipher(key, AES.MODE_ECB)
    return aes_obj.decrypt(ct)


if __name__ == "__main__":
    path_to_task = path.join("..", "Lab0_app", "Lab0_Tasks", "decryptAesEcb.txt")
    with open(path_to_task, "r") as decrypt_aes_ecb:
        base64_string = decrypt_aes_ecb.read().rstrip()
    print aes_ecb_decrypt(base64_string.decode("base64"), "YELLOW SUBMARINE")

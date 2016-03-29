#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7
from Crypto.Cipher import AES
from itertools import izip
from re import sub, search


def split_nth_chars(string, size_block):
    return [string[i:i + size_block] for i in range(0, len(string), size_block)]


class AESCipher:
    block_size = 16

    def __init__(self, key):
        self.key = self.get_valid_data(key)
        self.pkcs7 = PKCS7(self.block_size)

    def get_valid_data(self, data):
        if len(data) >= 16:
            data = data[:16]
        else:
            data = self._padding(data)
        return data

    def _padding(self, data):
        return self.pkcs7.padding(data)

    def _unpadding(self, data):
        return self.pkcs7.unpadding(data)

    def _xor_blocks(self, block1, block2):
        return "".join(chr(ord(b1) ^ ord(b2)) for b1, b2 in izip(block1, block2))

    def ecb_encrypt(self, data):
        aes_obj = AES.new(self.key, AES.MODE_ECB)
        return aes_obj.encrypt(data)

    def ecb_decrypt(self, data):
        aes_obj = AES.new(self.key, AES.MODE_ECB)
        return aes_obj.decrypt(data)

    def cbc_encrypt(self, data, iv):
        data = self._padding(data)
        encrypted_data = ""
        prev_block = iv
        blocks = split_nth_chars(data, self.block_size)
        for block in blocks:
            encrypted_block = self.ecb_encrypt(self._xor_blocks(block, prev_block))
            encrypted_data += encrypted_block
            prev_block = encrypted_block
        return encrypted_data

    def cbc_decrypt(self, data, iv):
        decrypted_data = ""
        prev_block = iv
        blocks = split_nth_chars(data, self.block_size)
        for block in blocks:
            decrypted_block = self.ecb_decrypt(block)
            decrypted_data += self._xor_blocks(decrypted_block, prev_block)
            prev_block = block
        return self._unpadding(decrypted_data)


def strip_data(data, regexp):
    return sub(regexp, "", data)


def change_role(plain_text, user_data, encrypted_data, aes, iv):
    user_data_block_number = (plain_text.find(user_data) / AESCipher.block_size)
    brute_block_number = user_data_block_number - 1

    plain_text_blocks = split_nth_chars(plain_text, AESCipher.block_size)
    encrypted_data_blocks = split_nth_chars(encrypted_data, AESCipher.block_size)

    brute_block = encrypted_data_blocks[brute_block_number]
    index_brute = plain_text_blocks[user_data_block_number].find("^")

    suffix_encrypt = "".join(data for data in encrypted_data_blocks[:brute_block_number])
    prefix_encrypt = "".join(data for data in encrypted_data_blocks[brute_block_number + 1:])

    for byte in range(256):
        attack_block = brute_block[:index_brute] + chr(byte) + brute_block[index_brute + 1:]
        attack_encrypted_data = suffix_encrypt + attack_block + prefix_encrypt
        attack_plain_text = aes.cbc_decrypt(attack_encrypted_data, iv)
        if search(r"admin=true", attack_plain_text):
            print attack_plain_text
            return True
    return False

if __name__ == "__main__":
    key = "YELLOW SUBMARINE"
    iv = "\x00" * 16

    user_data = "admin^true"
    suffix = "comment1=cooking%20MCs;userdata="
    prefix = ";comment2=%20like%20a%20pound%20of%20bacon"
    plain_text = "{0}{1}{2}".format(suffix, strip_data(user_data, ";|="), prefix)

    aes = AESCipher(key)
    encrypted_data = aes.cbc_encrypt(plain_text, iv)
    decrypted_data = aes.cbc_decrypt(encrypted_data, iv)

    print "Plain text is : {0}\n".format(plain_text)
    print "Result encrypt function in hex is: {0}\n".format(encrypted_data.encode("hex"))
    print "Result decrypt function: {0}\n".format(decrypted_data)

    print "Changing encrypted data..."
    change_role(plain_text, user_data, encrypted_data, aes, iv)

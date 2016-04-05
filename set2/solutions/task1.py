#!/usr/bin/env python2
# -*- coding: utf-8 -*-

class PKCS7():

    class PKCS7Exception(Exception):
        pass

    def __init__(self, block_size=16):
        if block_size < 2 or block_size > 255:
            raise PKCS7.PKCS7Exception("Incorrect block size")
        self.block_size = block_size

    def unpadding(self, data):
        data_len = len(data)
        padding_len = ord(data[-1])
        if padding_len > self.block_size:
            raise PKCS7.PKCS7Exception("PKCS7 padding is incorrect")
        return data[:(data_len - padding_len)]

    def padding(self, data):
        data_len = len(data)
        amount_to_pad = self.block_size - (data_len % self.block_size)
        if amount_to_pad == 0:
            amount_to_pad = self.block_size
        padding = chr(amount_to_pad) * amount_to_pad
        return data + padding


if __name__ == "__main__":
    test_string = "YELLOW SUBMARINE"

    pkcs7 = PKCS7(20)
    pkcs7_data = pkcs7.padding("YELLOW SUBMARINE")

    print pkcs7_data
    print pkcs7.unpadding(pkcs7_data)


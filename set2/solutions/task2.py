#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7


def check_valid_pkcs7_padding(pkcs7_block):
    padding_len = ord(pkcs7_block[len(pkcs7_block)-1])
    padding = pkcs7_block[-padding_len:]
    for byte in padding:
        if ord(byte) != padding_len:
            raise PKCS7.PKCS7Exception("PKCS7 padding is incorrect")
    return True


def test_pkcs7_padding(pkcs7_block):
    try:
        check_valid_pkcs7_padding(pkcs7_block)
    except PKCS7.PKCS7Exception as e:
        print "[-]: {0}, {1}".format(pkcs7_block, e)
        return False
    else:
        print "[+]: {0}, PKCS7 padding is correct".format(pkcs7_block)
        return True


if __name__ == "__main__":
    test_padding1 = "YELLOW SUBMARINE\x04\x04\x04\x04"
    test_padding2 = "YELLOW SUBMARINE\x05\x05\x05\x05"
    test_padding3 = "YELLOW SUBMARINE\x01\x02\x03\x04"

    test_pkcs7_padding(test_padding1)
    test_pkcs7_padding(test_padding2)
    test_pkcs7_padding(test_padding3)

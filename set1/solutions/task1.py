#!/usr/bin/env python2
# -*- coding: utf-8 -*-

base64_alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"


def split_nth_chars(string, size_block):
    return [string[i:i + size_block] for i in range(0, len(string), size_block)]


def base64_encode(string_to_encode):
    encode_string = ""
    left = 0
    for i in range(len(string_to_encode)):
        if left == 0:
            encode_string += base64_alp[ord(string_to_encode[i]) >> 2]
            left = 2
        else:
            if left == 6:
                encode_string += base64_alp[ord(string_to_encode[i - 1]) & 63]
                encode_string += base64_alp[ord(string_to_encode[i]) >> 2]
                left = 2
            else:
                index1 = ord(string_to_encode[i - 1]) & (2 ** left - 1)
                index2 = ord(string_to_encode[i]) >> (left + 2)
                index = (index1 << (6 - left)) | index2
                encode_string += base64_alp[index]
                left += 2
    if left != 0:
        encode_string += base64_alp[(ord(string_to_encode[len(string_to_encode) - 1]) & (2 ** left - 1)) << (6 - left)]
    encode_string += "=" * ((4 - len(encode_string) % 4) % 4)
    return encode_string


def base64_decode(base64_string):
    decode_string = ""
    base64_string = base64_string.replace("=", "")
    left = 0
    for i in range(len(base64_string)):
        if left == 0:
            left = 6
        else:
            value1 = base64_alp.index(base64_string[i - 1]) & (2 ** left - 1)
            value2 = base64_alp.index(base64_string[i]) >> (left - 2)
            value = (value1 << (8 - left)) | value2
            decode_string += chr(value)
            left -= 2
    return decode_string


def ascii_to_hex(char):
    return format(ord(char), "x")


def hex_to_ascii(hex_b):
    chars_in_reverse = []
    while hex_b != 0x0:
        chars_in_reverse.append(chr(hex_b & 0xFF))
        hex_b >>= 8
    chars_in_reverse.reverse()
    return "".join(chars_in_reverse)


def hex_to_base64(s_hex):
    split_s_hex = split_nth_chars(s_hex, 2)
    char = "".join([hex_to_ascii(int(byte, 16)) for byte in split_s_hex])
    return base64_encode(char)


def base64_to_hex(s_base64):
    s_bytes = base64_decode(s_base64)
    return "".join([ascii_to_hex(char) for char in s_bytes])


if __name__ == "__main__":
    hex_string = "faea8766efd8b295a633908a3c0828b22640e1e9122c3c9cfb7b59b7cf3c9d448bf04d72cde3aaa0"
    print hex_to_base64(hex_string)
    print base64_to_hex(hex_to_base64(hex_string))

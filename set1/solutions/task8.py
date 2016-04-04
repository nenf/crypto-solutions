#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os import path
from task1 import split_nth_chars


def is_repeat_blocks(ct):
    ct_blocks = split_nth_chars(ct, 16)
    if len(set(ct_blocks)) != len(ct_blocks):
        return True
    return False


if __name__ == "__main__":
    path_to_task = path.join("..", "Lab0_app", "Lab0_Tasks", "detectEcb.txt")
    with open(path_to_task, "r") as detect_ecb_file:
        hex_enc_lines = [s_hex.rstrip() for s_hex in detect_ecb_file.readlines()]
    for enc in hex_enc_lines:
        if is_repeat_blocks(enc.decode("hex")):
            print enc

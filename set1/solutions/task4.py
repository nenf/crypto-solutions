#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from os import path
from task3 import brute_one_symbole_xor

if __name__ == "__main__":
    path_to_task = path.join("..", "Lab0_app", "Lab0_Tasks", "detectSingleCHXor_tasks", "detectSingleXor05")
    with open(path_to_task, "r") as detect_xor_file:
        hex_lines = [s_hex.rstrip() for s_hex in detect_xor_file.readlines()]
    for s_hex in hex_lines:
        brute_one_symbole_xor(s_hex)

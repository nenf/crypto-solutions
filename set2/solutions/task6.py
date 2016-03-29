#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from task1 import PKCS7
from task3 import AESCipher, strip_data
from task4 import rand_data, split_nth_chars
from urllib import urlencode, unquote

key = rand_data()
aes = AESCipher(key)


def get_dict_from_get_request(get_request):
    dict_data = {}
    data = get_request.split("&")
    for pair in data:
        value, data = pair.split("=")[0], pair.split("=")[1]
        dict_data[value] = data
    return dict_data


def profile_for(email):
    email = strip_data(email, r"&|=")
    profile_object = [("email", email), ("uid", 10), ("role", "user")]
    return urlencode(profile_object)


def print_profile_info(profile_object):
    print "email: {0}".format(unquote(profile_object["email"]))
    print "uid: {0}".format(profile_object["uid"])
    print "role: {0}".format(profile_object["role"])


if __name__ == "__main__":
    test_string = "foo=bar&baz=qux&zap=zazzle"
    print get_dict_from_get_request(test_string)

    pkcs7 = PKCS7()
    attack_message = ""

    data = profile_for("sasha@ya.ru")
    data = pkcs7.padding(data)
    blocks = split_nth_chars(aes.ecb_encrypt(data), 16)
    attack_message += blocks[0] + blocks[1]

    data = profile_for("my@ya.ruadmin")
    data = pkcs7.padding(data)
    blocks = split_nth_chars(aes.ecb_encrypt(data), 16)
    attack_message += blocks[1]

    data = profile_for("tester@ya.ru")
    data = pkcs7.padding(data)
    blocks = split_nth_chars(aes.ecb_encrypt(data), 16)
    attack_message += blocks[2]

    profile_request = aes.ecb_decrypt(attack_message)
    profile_object = get_dict_from_get_request(profile_request)
    print_profile_info(profile_object)

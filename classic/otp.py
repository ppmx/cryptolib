#!/usr/bin/env python3

""" This is an implementation of algorithms of the vernam group including the
one-time-pad.
"""

import argparse
import unittest
import os

def generate_key(target_string):
    """ Generates a random key that fits the length of the
    given target string. Uses os.urandom.
    """

    return os.urandom(len(target_string))


def otp(string_a, string_b, comb=lambda x, y: (x ^ y)):
    """ This function returns the result of applying the given function on each
    symbol of the passed two arrays.

    The passed vectors a and b have to be of type bytes and the result is also
    of type bytes. The argument comb is expected to be a function expecting two
    byte values returning a single byte value.
    """

    return bytes([comb(x, y) for x, y in zip(string_a, string_b)])


class TestOTP(unittest.TestCase):
    """ Tests this package: the gcd toolchain. """

    def test_otp(self):
        """ Tests the otp function. """

        vectors = [
            [
                bytes.fromhex("1c0111001f010100061a024b53535009181c"),
                bytes.fromhex("686974207468652062756c6c277320657965"),
                bytes.fromhex("746865206b696420646f6e277420706c6179")
            ]
        ]


        for string_a, string_b, expected_result in vectors:
            self.assertEqual(otp(string_a, string_b), expected_result)


def cli():
    """ Provides a command line interface. Pass -h as argument to get some
    information.
    """

    parser = argparse.ArgumentParser(description='Tool to compute the one time pad of a and b.')

    parser.add_argument('string_a', type=bytes.fromhex, help='string a - hexadecimal encoded')
    parser.add_argument('string_b', type=bytes.fromhex, help='string b - hexadecimal encoded')

    args = parser.parse_args()

    result = otp(args.string_a, args.string_b)
    print(result.hex())


if __name__ == "__main__":
    cli()

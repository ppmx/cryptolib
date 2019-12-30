#!/usr/bin/env python3

""" Package to compute the hamming distance.

The hamming distance between two strings of equal length is the number of
of positions at which the corresponding symbols are different.
"""

import argparse
import unittest

def hamming(string_a, string_b):
    """ This function returns the hamming distance as the number of different
    bits for the given two byte arrays.
    """

    return sum([bin(a ^ b).count('1') for a, b in zip(string_a, string_b)])


class TestHamming(unittest.TestCase):
    """ Some unittests for this package. """

    def test_hamming(self):
        """ Tests the hamming function. """

        string_a, string_b = b'this is a test', b'wokka wokka!!!'
        self.assertEqual(hamming(string_a, string_b), 37)


def cli():
    """ Provides a command line interface. Pass -h as argument to get some information.

    Example:

    $ ./hamming.py "crypto is fun" "beer is tasty"
    The hamming distance is: 34
    """

    parser = argparse.ArgumentParser(
        description='Tool to compute the hamming distance of both passed strings.'
    )

    parser.add_argument('string_a', type=lambda c: c.encode())
    parser.add_argument('string_b', type=lambda c: c.encode())
    args = parser.parse_args()

    result = hamming(args.string_a, args.string_b)
    print("The hamming distance is:", result)


if __name__ == "__main__":
    cli()

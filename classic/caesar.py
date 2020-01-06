#!/usr/bin/env python3

""" The caesar cipher is a special case of the substitution cipher. The permutation is restricted to
a cyclic shift of the alphabet. The cipher was first used by Caesar (100-44 BC) during the Gallic
Wars. A machine-assisted version of this cipher was constructed by Leon Battista Alberti in the 15th
century. The Latin alphabet {a,b,...,z} is mapped to the set {0,1,...,25} = Z26. We then apply
arithmetic modulo 26 (”normal“ arithmetic, but remainder when dividing by 26) on this set.
"""


import unittest
import string


class CaesarCipher:
    """ Implementation of the caesar cipher providing an encryption and a decryption routine.

    Example:
    --------
    >>> key = 23
    >>> suite = CaesarCipher(key)
    >>> suite.encrypt("FOOBAR")
    CLLYXO
    >>> suite.decrypt("CLLYXO")
    'FOOBAR'
    """

    def __init__(self, key, alphabet=string.ascii_uppercase):
        """ key has to be a natural number with 0 <= key < len(alphabet) """

        self.alphabet = alphabet
        self.key = key

    def encrypt(self, plaintext):
        """ Encrypts a message using the caesar cipher and returns the corresponding ciphertext. """

        # enc is a helper function that computes the corresponding index of the ciphertext
        # character for the passed index of a plaintext character based on self.key.
        enc = lambda i: (i + self.key) % len(self.alphabet)
        return ''.join([self.alphabet[enc(self.alphabet.index(m))] for m in plaintext])

    def decrypt(self, ciphertext):
        """ Decrypts a message using the caesar cipher and returns the corresponding plaintext. """

        # dec is a helper function that computes the corresponding index of the plaintext
        # character for the passed index of a ciphertext character based on self.key.
        dec = lambda i: (i + len(self.alphabet) - self.key) % len(self.alphabet)
        return ''.join([self.alphabet[dec(self.alphabet.index(m))] for m in ciphertext])


class TestCaesarSuite(unittest.TestCase):
    """ Tests the implementation of the caesar cipher. """

    def test_known_vectors(self):
        """ Tests the caesar cipher implementation with well known test vectors. """

        test_vectors = [
            {
                'key': 1,
                'plaintext': 'HELLO',
                'ciphertext': 'IFMMP'
            }
        ]

        for vector in test_vectors:
            suite = CaesarCipher(vector['key'])

            self.assertEqual(suite.encrypt(vector['plaintext']), vector['ciphertext'])
            self.assertEqual(suite.decrypt(vector['ciphertext']), vector['plaintext'])

    def test_random(self):
        """ Tests the caesar cipher implementation using randomly generated values. """

        import random

        # do 100 testing random rounds:
        for _ in range(100):
            # generate a random alphabet (0 <= length <= 99) with printable symbols:
            alph = list(set(random.choice(string.printable) for _ in range(random.randint(1, 100))))

            # generate a random key:
            key = random.randint(0, len(alph))

            # generate a random message (0 <= length of it <= 99) over the generated alphabet:
            message = ''.join(random.choice(alph) for _ in range(random.randint(1, 100)))

            suite = CaesarCipher(key, alph)

            self.assertEqual(suite.encrypt(suite.decrypt(message)), message)
            self.assertEqual(suite.decrypt(suite.encrypt(message)), message)


def cli():
    """ Provides a command line interface. Pass -h as argument to get some information.


    Example to encrypt a string:
    ----------------------------
    $ python3 caesar.py -e 23 "HELLOWORLD"
    EBIILTLOIA


    Example to decrypt a string:
    ----------------------------
    $ python3 caesar.py -d 23 "EBIILTLOIA"
    HELLOWORLD


    Example how to work with another alphabet:
    ------------------------------------------
    $ python3 caesar.py --alphabet="abcdefghijklmnopqrstuvwxyz" -e 4 "hello"
    lipps

    $ python3 caesar.py --alphabet="abcdefghijklmnopqrstuvwxyz" -d 4 "lipps"
    hello
    """

    import argparse

    parser = argparse.ArgumentParser(
        description='Tool to encrypt or decrypt messages using the caesar cipher.'
    )

    parser.add_argument(
        '--decrypt', '-d', action='store_true', help='invoke the decryption routine'
    )

    parser.add_argument(
        '--encrypt', '-e', action='store_true', help='invoke the encryption routine'
    )

    parser.add_argument(
        '--alphabet', default=string.ascii_uppercase, help='define the alphabet, default is A-Z'
    )

    parser.add_argument('key', type=int, help='key to be used (between 0 and 25)')
    parser.add_argument('text', type=str, help='help to encrypt or decrypt')

    args = parser.parse_args()
    suite = CaesarCipher(args.key, args.alphabet)

    if args.encrypt:
        print(suite.encrypt(args.text))
    elif args.decrypt:
        print(suite.decrypt(args.text))


if __name__ == "__main__":
    cli()

#!/usr/bin/env python3

""" Common functions to convert stuff """

import unittest

def message_to_indexlist(string, alphabet):
    """ Converts a message to a list of indexes regarding the given alphabet.

    Example:
    >>> message_to_indexlist("HELLO", string.ascii_uppercase)
    [7, 4, 11, 11, 14]
    """

    return [alphabet.index(s) for s in string]


def indexlist_to_message(stream, alphabet, seperator):
    """ Converts a list of indexes to the corresponding message.

    >>> indexlist_to_message([7, 4, 11, 11, 14], string.ascii_uppercase, '')
    'HELLO'
    """

    return seperator.join(alphabet[c] for c in stream)


class TestHamming(unittest.TestCase):
    """ Some unittests for this package. """

    def test_message_to_indexlist(self):
        """ Tests message_to_indexlist() """

        self.assertEqual(message_to_indexlist("abec", "abcde"), [0, 1, 4, 2])

    def test_indexlist_to_message(self):
        """ Tests the indexlist_to_message() function """

        self.assertEqual(indexlist_to_message([0, 1, 4, 2], "abcde", ''), "abec")

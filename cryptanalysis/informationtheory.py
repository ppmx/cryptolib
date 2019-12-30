#!/usr/bin/env python3

""" Collection of basic but useful methods of the information theory (e.g. entropy).

Hint: It is highly recommended for computer scientists to read at least one of
the great books about information and coding theory.
"""

import math

def compute_information_content(probability, log_base=2):
    """ Computes and returns the value of the information content for the event
    with the given probability (float, 0 <= p <= 1) regarding the given base.

    This definition for valuing the information content is common in the field
    of information and coding theory.
    """

    return -math.log(probability, log_base)

def compute_entropy(probabilities, information_content=compute_information_content):
    """ This function computes and returns the entropy of a system with the
    given probabilities regarding the passed logarithm base. The argument
    probabilities has to be a mapping (dict) of events for the system to their
    probability p (0 <= p <= 1).

    The entropy is a measure of uncertainty of a system. The entropy is least
    when there is no uncertainty about the events in the system, so that no
    information is conveyed when an event occurs. The entropy is greatest, and
    the most information is conveyed, when there is the greatest uncertainty
    about the events.
    """

    return sum(p * information_content(p) for p in probabilities.values())


def compute_redundancy(alphabet, entropy, log_base):
    """ This function computes and returns the redundancy of a system over the
    given alphabet with the given entropy regarding the base of the underlying
    logarithm.

    The redundancy is the expected amount of symbols without information.
    """

    return 1 - (entropy / math.log(len(alphabet), log_base))

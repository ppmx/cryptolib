#!/usr/bin/env python3

""" Implements the RSA factorize attack for a known n and known phi(n).

n = pq, where p and q are two prime numbers while phi(n) = (p-1)*(q-1)

   phi(n) = pq - q - p + 1
=> p+q = pq + 1 - phi(n) = n + 1 - phi(n)

    x^2 - (p+q) * x + pq = (x - p)(x - q)
<=> x^2 - (pq + 1 - phi(n)) * x + pq = (x - p)(x - q)

And on the left side of this formula we apply the pq-formula to calculate points
of zero.
"""

import math
import sys

def int_sqrt(n):
    """ Calculates and returns the square root for a given
    integer without converting to float (for large ints).
    """

    x, y = n, (n + 1) // 2

    while y < x:
        x = y
        y = (x + n // x) // 2

    return x

def factorize(n, phi):
    """ Factorize n with a known phi(n) """

    # those p and q are the ones for the pq-formula:
    p, q = n + 1 - phi, n

    a = (p // 2)
    b = int_sqrt(pow(p // 2, 2) - q)

    return a + b, a - b

def main():
    try:
        n, phi = int(sys.argv[1]), int(sys.argv[2])
    except IndexError:
        print("Usage:", sys.argv[0], "<n> <phi>")
        return

    print(f"[+] apply attack on n = {n}, phi(n) = {phi}")
    print(factorize(n, phi))

def example():
    n = 399081846921783573731969706872899710332479570669182598636878020544545498500095879706861915957763765677589271148544418027556897638123898650694905659699388027447329186567543669719056963934478907484470299975070884228881176791374833064981004136947342827784345106988800086071486535280883930849129956794812392496934540555767897685178133034313801007825526945491955390972816804087486190979770576016075456226669814508584111976115292015873914100495003509657724170377980833036834209651934046247242851210899152712215029291780647726641180724779799987396580312898896726502886323838513051112374864699777289381818747410721416544692008823061323004855133180373097904302215709173980719604124931552278155654881363712418244600042558077449111260172950537541679740953643124072108823653101336984482418977965548839966796825427469248953717368992453221758211069815998323467745433076440816218770134280148474654871865154874107896295277715856661495807558451423177301616266015627951159478809210586119547055672009526622844688457854956041456424573298569136603966508921141528661224225597464851189943714670790624246047603859474880886165025053072930864742536612129544210602896637521568724195304418687224790830444695979862424243638949764703980358968979360303879802689391

    phi = 399081846921783573731969706872899710332479570669182598636878020544545498500095879706861915957763765677589271148544418027556897638123898650694905659699388027447329186567543669719056963934478907484470299975070884228881176791374833064981004136947342827784345106988800086071486535280883930849129956794812392496934540555767897685178133034313801007825526945491955390972816804087486190979770576016075456226669814508584111976115292015873914100495003509657724170377980833036834209651934046247242851210899152712215029291780647726641180724779799987396580312898896726502886323838513051112374864699777289381818747410721416544691968606548929161082091315994421083137060778534748076222828623799585450725081719305886649391804890131180040576844561636116182210936205910651596361299174406892176843145195873685508586635737872962951104541625228338310007560694781259110348285712599970334887412504135754455876224100828319831585234168455266537438464899005338202245310667740774896345142897604317418058899050594525448035580777087353972133993664016636341614315641999238958712056868291841241367607147377815039070514381955147729642477607988053631301605401377374356033549269018846062037404082653673553476484059406406721489158886664745860024822991895076750438630392

    print("bitsize(n) =", len(format(n, "b")))
    print("bitsize(phi(n)) =", len(format(phi, "b")))

    p, q = factorize(n, phi)
    assert(p * q == n)

    print("p =", p)
    print("q =", q)

if __name__ == "__main__":
    main()

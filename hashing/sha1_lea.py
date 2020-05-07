#!/usr/bin/env python3

""" Length Extension Attack on Merkle-Damgard-Constructions (here SHA1) """

import struct
import sys
import textwrap

class SHA1:
    """ SHA 1 implementation providing an interface to reassign internal hashing state """

    def __init__(self, state=[0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]):
        self.h = state

        self.hashed_bytes = 0
        self.buffer = bytes()

    @staticmethod
    def compress(chunk, h0, h1, h2, h3, h4):
        """ Compress the given chunk considering the current state [h0, ..., h4]
        and returns the new state after compression.
        """

        assert len(chunk) == 64

        # 32 bit circular left shift of w by b bits:
        leftrot = lambda w, b: ((w << b) | (w >> (32 - b))) & 0xffffffff

        x = [0] * 80

        for i in range(16):
            x[i] = struct.unpack('>I', chunk[4*i:4*i+4])[0]

        for i in range(16, 80):
            x[i] = leftrot(x[i - 3] ^ x[i - 8] ^ x[i - 14] ^ x[i - 16], 1)

        a, b, c, d, e = h0, h1, h2, h3, h4

        for i in range(80):
            if 0 <= i <= 19:
                y = 0x5A827999
                z = (b & c) | ((b ^ 0xffffffff) & d)
            elif 20 <= i <= 39:
                y = 0x6ED9EBA1
                z = b ^ c ^ d
            elif 40 <= i <= 59:
                y = 0x8F1BBCDC
                z = (b & c) | (b & d) | (c & d)
            elif 60 <= i <= 79:
                y = 0xCA62C1D6
                z = b ^ c ^ d

            t = (leftrot(a, 5) + z + e + x[i] + y) & 0xffffffff
            a, b, c, d, e = (t, a, leftrot(b, 30), c, d)

        return [
            (h0 + a) & 0xffffffff,
            (h1 + b) & 0xffffffff,
            (h2 + c) & 0xffffffff,
            (h3 + d) & 0xffffffff,
            (h4 + e) & 0xffffffff,
        ]

    def update(self, data):
        """ Updates the current hashing state with data (bytes) """

        self.buffer += data

        # do compression for all available blocks:
        while len(self.buffer) >= 64:
            chunk, self.buffer = self.buffer[:64], self.buffer[64:]
            self.h = self.compress(chunk, *self.h)
            self.hashed_bytes += 64

        # in contrast to hashlib daisy chaining is allowed here:
        return self

    @staticmethod
    def finalize_pad_message(prefix_length, data):
        """ This function returns a padded data block to finalize the hashsum.

        The last block to compute the final hashsum for the consumed data needs
        a padding. This is added as postfix to hashed data M:

        length of zero pad to fill up the block: d = (447 - |M|) mod 512
        length of consumed data: l = binary repr. of b mod 2^64
        message padded: M = M || 1 || 0^d || l
        """

        m = data
        hashed_bytes = prefix_length + len(m)

        # add bit 1, seven zeroes and remaining zeroes (d - 7):
        m += b'\x80' + b'\00' * ((56 - (hashed_bytes + 1) % 64) % 64)

        # add l = binary representation of b mod pow(2, 64):
        m += struct.pack('>Q', hashed_bytes * 8)

        return m

    def finalize(self, remainder):
        """ Pads the remaining data and computes it into the current state """

        m = self.finalize_pad_message(self.hashed_bytes, remainder)

        finalized_h = self.h

        # compute remaining bytes into hash sum:
        while m:
            finalized_h = self.compress(m[:64], *finalized_h)
            m = m[64:]

        return finalized_h

    def digest(self):
        """ Return the digest of the bytes passed to the update() method so
        far as a bytes object.
        """
        return b''.join(struct.pack('>I', h) for h in self.finalize(self.buffer))

    def hexdigest(self):
        """ Return the digest of the bytes passed to the update() method
        so far as a string containing the hexadecimal representation of digest.
        """
        return ''.join(format(h, "08x") for h in self.finalize(self.buffer))

    @staticmethod
    def hexdigest_to_state(hexdigest):
        return [struct.unpack('>I', bytes.fromhex(b))[0] for b in textwrap.wrap(hexdigest, 8)]

def test():
    assert SHA1().update(b"").hexdigest() == "da39a3ee5e6b4b0d3255bfef95601890afd80709"
    assert SHA1().update(b"nanana batman").hexdigest() == "acc505b782afe56238322ef8f583f4f3686b27ca"
    assert SHA1().update(b'A' * 1234).hexdigest() == "6f52ff28c54c02bf33008c855b4eec36d5bede4f"

    assert SHA1().update(b"nanana batman").digest() == bytes.fromhex("acc505b782afe56238322ef8f583f4f3686b27ca")
    assert SHA1().update(b"nanana batman").digest() != bytes.fromhex("bcc505b782afe56238322ef8f583f4f3686b27ca")

    # try out continuous update function:
    session = SHA1()
    assert session.update(b"nanana").hexdigest() == "ebd936ea94d4d7ef22edefad4d1a9f53c07daada"
    assert session.update(b" ").hexdigest() == "427029b0d3c8e2701b2123287fea802218236508"
    assert session.update(b"batman").hexdigest() == "acc505b782afe56238322ef8f583f4f3686b27ca"

def sha1_lea(hexdigest, data, appendix, prefixlength):
    # convert hex digest to sha1 state:
    session = SHA1(SHA1.hexdigest_to_state(hexdigest))

    # compute the padded data blob. the unknown prefix will be considered by adding the length of it:
    padded_data = session.finalize_pad_message(prefixlength, data)
    session.hashed_bytes = prefixlength + len(padded_data)
    session.buffer = appendix

    return session.hexdigest(), padded_data + appendix

def cli():
    try:
        hexdigest = sys.argv[1]
        payload = sys.argv[2].encode()
        appendix = sys.argv[3].encode()
        prefixlength = int(sys.argv[4])
    except:
        print("Usage:", sys.argv[0], "<hexdigest> <payload> <appendix> <length of unknown prefix>")
        return

    newsum, newpayload = sha1_lea(hexdigest, payload, appendix, prefixlength)

    print("[+] new hashsum:", newsum)
    print("[+] new payload:", newpayload)

if __name__ == "__main__":
    cli()

# By Bartłomiej Wujec

import hashlib

with open('personalconcat.txt', 'rb') as p1:
    text1: bytes = p1.read()

with open('personal_concat.txt', 'rb') as p2:
    text2: bytes = p2.read()

hex2binary = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15
}


def my_hash(type: str, string: bytes):
    hash = hashlib.new(type, string)
    hex = hash.hexdigest()

    return hex


def h2b(type: str, string: bytes):
    hash = hashlib.new(type, string)
    hex = hash.hexdigest()
    binary = ""
    for char in hex:
        binary += bin(hex2binary[char])[2:].rjust(4, '0')

    return binary


def diff(seq1, seq2):
    _diff = 0
    for i in range(len(seq1)):
        if seq1[i] != seq2[i]:
            _diff += 1
    return _diff


with open("diff.txt", "w", encoding="utf-8") as diff_file:
    for hashing in ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b"]:
        h2b(hashing, text1)
        diff_file.write(hashing + "\n")
        diff_file.write(my_hash(hashing, text1) + "\n")
        diff_file.write(my_hash(hashing, text2) + "\n")
        d = diff(h2b(hashing, text1), h2b(hashing, text2))
        l = len(h2b(hashing, text1))
        diff_file.write(f"Różnica {d} z {l} bitów. Procentowo: ")
        percent = "{0:.4}".format(str(d/l))
        diff_file.write(percent + "\n\n")

# By Bartłomiej Wujec

import hashlib

with open('personal.txt', 'r', encoding="utf-8") as p1:
    text1: str = p1.read()

with open('personal_.txt', 'r', encoding="utf-8") as p2:
    text2: str = p2.read()


# print(hashlib.md5(text1).hexdigest())
# print(hashlib.md5(text2).hexdigest())

def my_hash(type: str, string: str):
    hash = hashlib.new(type, string.encode("utf-8"))
    hex = hash.hexdigest()

    return hex


def h2b(type: str, string: str):
    hash = hashlib.new(type, string.encode("utf-8"))
    hex = hash.hexdigest()

    binary = ""
    for char in hex:
        binary += bin(ord(char))[2:]

    return binary


def diff(seq1, seq2):
    _diff = 0
    for i in range(min(len(seq1), len(seq2))):
        if seq1[i] != seq2[i]:
            _diff += 1
    return _diff


with open("diff.txt", "w", encoding="utf-8") as diff_file:
    for hashing in ["md5", "sha1", "sha224", "sha256", "sha384", "sha512", "blake2b"]:
        diff_file.write(hashing + "\n")
        diff_file.write(my_hash(hashing, text1) + "\n")
        diff_file.write(my_hash(hashing, text2) + "\n")
        diff_file.write(f"Różnica bitów: {diff(h2b(hashing, text1), h2b(hashing, text2))} z {len(h2b(hashing, text1))}."
                        f"Procentowo {diff(h2b(hashing, text1), h2b(hashing, text2))/len(h2b(hashing, text1))}\n\n")

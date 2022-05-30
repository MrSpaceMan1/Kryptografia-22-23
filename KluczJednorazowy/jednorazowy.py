#
# By Bartłomiej Wujec
#
import sys


def xor(s1, s2):
    if len(s1) > len(s2):
        s1.ljust(len(s2), '0')
    else:
        s2.ljust(len(s1), '0')

    for i in range(2, len(s1)):
        print(s1[i], s2[i])


def char2bin(s):
    return bin(ord(s[:1]))


def prepare():
    with open("orig.txt", 'r') as orig_file:
        original_text = orig_file.read().lower()

    prepared_text = ""
    prepared_line = ""
    for i in original_text:
        if i in [",", ".", "(", ")", "\"", "\'", "-"]:
            continue
        prepared_line += i
        if len(prepared_line) % 64 == 0:
            prepared_text += f"{prepared_line}\n"
            prepared_line = ""

    with open("plain.txt", "w") as plain_file:
        plain_file.write(prepared_text)


def encrypt():
    with open("key.txt", "br") as key_file, open("plain.txt", "br") as plain_file:
        key = list(filter(lambda l: l not in [44, 46, 40, 41, 34, 39, 45], key_file.read().lower()))[:64]
        lines = list(map(lambda l: l[:-2], plain_file.readlines()))

    with open("crypto.txt", "bw") as crypto_file:
        encrypted_line = ""
        for line in lines:
            for i in range(len(line)):
                encrypted_line += chr(line[i] ^ key[i])
            crypto_file.write(bytes(encrypted_line, "utf-8"))


def cryptanalysis():
    with open("crypto.txt", "br") as crypto_file:
        while True:
            print(crypto_file.read(8))


def main():
    args = sys.argv

    options = {
        "-p": prepare,
        "-e": encrypt,
        "-k": cryptanalysis
    }

    options[args[1]]()


if __name__ == "__main__":
    main()

import random
import sys


# By Bartłomiej Wujec

def create_private_key(p):
    return random.randint(10000000, p-1)


def create_public_key(g, p, private):
    beta = pow(g, private, p)
    return beta


def generate_pair_of_keys():
    with open('elgamal.txt', 'r') as elgamal:
        p = int(elgamal.readline())
        g = int(elgamal.readline())

    private_k = create_private_key(p)
    public_k = create_public_key(g, p, private_k)

    with open("private.txt", "w") as private_f:
        private_f.write(str(p) + "\n")
        private_f.write(str(g) + "\n")
        private_f.write(str(private_k) + "\n")

    with open("public.txt", "w") as public_f:
        public_f.write(str(p) + "\n")
        public_f.write(str(g) + "\n")
        public_f.write(str(public_k) + "\n")


def encrypt():
    with open("public.txt", "r") as public_f:
        p, g, public_k = [
            int(public_f.readline()),
            int(public_f.readline()),
            int(public_f.readline())
        ]

    with open("plain.txt", "r") as plain_f:
        message = plain_f.read()

    number_message = ""

    for char in message:
        number_message += str(ord(char)).rjust(3, "0")

    if int(number_message) > p:
        raise ValueError("Message to long")

    k = random.randint(10000000, p - 1)

    c1 = pow(g, k, p)
    c2 = (int(number_message) * (public_k ** k)) % p

    with open("crypto.txt", "w") as crypto_f:
        crypto_f.write(str(c1) + "\n")
        crypto_f.write(str(c2) + "\n")


def decrypt():
    with open("crypto.txt", "r") as crypto_f:
        c1, c2 = [
            int(crypto_f.readline()),
            int(crypto_f.readline())
        ]

    with open("private.txt", "r") as private_f:
        p, g, private_k = [
            int(private_f.readline()),
            int(private_f.readline()),
            int(private_f.readline())
        ]

    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

    def modinv(a, m):
        g, x, y = egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    x = pow(c1, private_k, p)

    inverse_x = modinv(x, p)  # pow(x, -1, p)

    decrypted_number = (inverse_x * c2) % p

    if len(str(decrypted_number)) % 3 != 0:
        decrypted_number = "0" + str(decrypted_number)

    message = ""
    for triplet in range(0, len(decrypted_number), 3):
        char = chr(int(decrypted_number[triplet:triplet + 3]))
        message += char

    with open("decrypt.txt", "w", encoding="utf-8") as decrypt_f:
        decrypt_f.write(str(message))


def main():
    args = sys.argv[1:]
    # args = ['-d']
    choice = {
        '-k': generate_pair_of_keys,
        '-e': encrypt,
        '-d': decrypt
    }

    choice[args[0]]()


if __name__ == "__main__":
    main()

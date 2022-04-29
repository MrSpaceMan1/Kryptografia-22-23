import sys
from abc import ABC, abstractmethod


class CryptoMethod(ABC):
    @abstractmethod
    def compare_sign(self, sign: str) -> bool:
        pass

    @abstractmethod
    def encrypt(self, line, key):
        pass

    @abstractmethod
    def decrypt(self, line, key):
        pass

    @abstractmethod
    def plaintext_cryptoanalysis(self, encrypted, plain):
        pass

    @abstractmethod
    def encrypted_cryptoanalysis(self, encrypted):
        pass


class Affine(CryptoMethod):
    def compare_sign(self, sign: str) -> bool:
        return "-a" == sign

    def inverse_in_mode(self, val, mode):
        for i in range(1, mode+1):
            if (val * i) % mode == 1:
                return i

    def encrypt(self, line, key):
        a, b = key
        encrypted = ""
        for i in line:
            if i == " ":
                encrypted += " "
                continue
            encrypted += chr(((((ord(i) - ord('A')) * a + b) % 26) + ord('A')))
        return encrypted

    def decrypt(self, line, key):
        a, b = key
        a = self.inverse_in_mode(a, 26)
        if a is None:
            return ""
        decrypted = ""
        for i in line:
            if i == " ":
                decrypted += " "
                continue
            decrypted += chr(((ord(i) - ord('A') - b) * a % 26) + ord('A'))
        return decrypted

    def plaintext_cryptoanalysis(self, encrypted, plain):
        y1, y2 = encrypted[:2]
        x1, x2 = plain
        y1, y2 = ord(y1) - ord('A'), ord(y2) - ord('A')
        x1, x2 = ord(x1) - ord('A'), ord(x2) - ord('A')
        try:
            a = int(((y2 - y1) / (x1 - x2))**-1 % 26)
            for i in range(1, 26):
                if self.encrypt(chr(x1+ord('A')), (a, i)) == chr(y1+ord('A')):
                    return a, i
        except:
            raise Exception('Nie można odnaleźć klucza')

    def encrypted_cryptoanalysis(self, encrypted):
        encrypted_lines = ""
        for i in range(1, 26):
            for j in range(0, 26):
                decrypted = self.decrypt(encrypted, (i, j))
                encrypted_lines += decrypted + "\n" if decrypted != "" else ""

        return encrypted_lines


class Caesar(CryptoMethod):

    def compare_sign(self, sign: str) -> bool:
        return "-c" == sign

    def encrypt(self, line, key):
        key, _ = key

        if 1 < key > 25:
            raise ValueError("Klucz z poza zakresu")

        encrypted = ""
        for i in line:
            if i == " ":
                encrypted += " "
                continue
            encrypted += chr((((ord(i) - ord('A') + key) % 26) + ord('A')))
        return encrypted

    def decrypt(self, line, key):
        key, _ = key

        if 1 < key > 25:
            raise ValueError("Klucz z poza zakresu")

        decrypted = ""
        for i in line:
            if i == " ":
                decrypted += " "
                continue
            decrypted += chr((((ord(i) - ord('A') - key) % 26) + ord('A')))
        return decrypted

    def plaintext_cryptoanalysis(self, encrypted, plain):
        en = ord(encrypted[0]) - ord('A')
        pl = ord(plain[0]) - ord('A')
        for i in range(1, 25):
            if (en - i) % 26 == pl:
                return i
        raise Exception('Nie można odnaleźć klucza')

    def encrypted_cryptoanalysis(self, encrypted):
        decrypted_lines = ""
        for i in range(1, 26):
            for j in encrypted:
                if j == " ":
                    decrypted_lines += " "
                    continue
                decrypted_lines += chr((ord(j) - ord('A') - i) % 26 + ord('A'))
            decrypted_lines += '\n'
        return decrypted_lines


class CryptographicTool:

    def __init__(self):
        self.methods = []

    def add(self, method: CryptoMethod):
        if method not in self.methods:
            self.methods.append(method)
        return self

    def encrypt(self, option: str):
        for i in self.methods:
            if i.compare_sign(option):
                line_to_encrypt = ""
                encrypted_line = ""
                key = None

                with open('./plain.txt', 'r') as plain:
                    line_to_encrypt = plain.readline().upper()
                    plain.close()

                with open('./key.txt', 'r') as key_file:
                    key = key_file.readline().split(" ")
                    key_file.close()

                for a in range(0, len(key)):
                    key[a] = int(key[a])

                encrypted_line = i.encrypt(line_to_encrypt, key)

                with open('./encrypted.txt', 'w') as encrypted_file:
                    encrypted_file.write(encrypted_line)
                    encrypted_file.close()

    def decrypt(self, option: str):
        for i in self.methods:
            if i.compare_sign(option):
                encrypted_line = ""
                key = None

                with open('./encrypted.txt', 'r') as encrypted:
                    line_to_encrypt = encrypted.readline().upper()
                    encrypted.close()

                with open('./key.txt', 'r') as key_file:
                    key = key_file.readline().split(" ")
                    key_file.close()

                for a in range(0, len(key)):
                    key[a] = int(key[a])

                encrypted_line = i.decrypt(line_to_encrypt, key)

                with open('./decrypted.txt', 'w') as decrypted:
                    decrypted.write(encrypted_line)
                    decrypted.close()

    def plaintext_cryptoanalysis(self, option: str):
        for i in self.methods:
            if i.compare_sign(option):
                encrypted_line = ""
                plaintext_line = ""

                with open('./encrypted.txt', 'r') as encrypted:
                    encrypted_line = encrypted.readline()
                    encrypted.close()

                with open('./extra.txt', 'r') as extra:
                    plaintext_line = extra.readline().upper()
                    extra.close()

                key = i.plaintext_cryptoanalysis(encrypted_line, plaintext_line)
                tmp = ""
                for i in key:
                    tmp+=f"{i} "
                key = tmp
                with open('./key-found.txt', 'w') as key_found:
                    key_found.write(str(key))
                    key_found.close()

    def encrypted_cryptoanalysis(self, option: str):
        for i in self.methods:
            if i.compare_sign(option):
                encrypted_line = ""

                with open('./encrypted.txt', 'r') as encrypted:
                    encrypted_line = encrypted.readline()
                    encrypted.close()

                proposed_solutions = i.encrypted_cryptoanalysis(encrypted_line)

                with open('./key-found.txt', 'w') as key_found:
                    key_found.write(proposed_solutions)
                    key_found.close()


def main():
    args = sys.argv
    crypto_tool = CryptographicTool()
    crypto_tool\
        .add(Caesar())\
        .add(Affine())

    if args[2] == "-e":
        crypto_tool.encrypt(args[1])
    elif args[2] == "-d":
        crypto_tool.decrypt(args[1])
    elif args[2] == "-j":
        crypto_tool.plaintext_cryptoanalysis(args[1])
    elif args[2] == "-k":
        crypto_tool.encrypted_cryptoanalysis(args[1])


if __name__ == "__main__":
    main()

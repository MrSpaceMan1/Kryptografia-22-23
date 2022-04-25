import sys
from abc import ABC, abstractmethod


class CryptMethod(ABC):
    @abstractmethod
    def compare_sign(self, sign: str) -> bool:
        pass

    @abstractmethod
    def encrypt(self):
        pass

    @abstractmethod
    def decrypt(self):
        pass

    @abstractmethod
    def plaintext_cryptoanalysis(self):
        pass

    @abstractmethod
    def encrypted_cryptoanalysis(self):
        pass


class Cezar(CryptMethod):

    def compare_sign(self, sign: str) -> bool:
        return "-c" == sign

    def encrypt(self):
        pass

    def decrypt(self):
        pass

    def plaintext_cryptoanalysis(self):
        pass

    def encrypted_cryptoanalysis(self):
        pass


def main():
    args = sys.argv
    crypt_list = [Cezar()]

    for i in crypt_list:
        if i.compare_sign(args[1]):
            if args[2] == "-e":
                i.encrypt()
            elif args[2] == "-d":
                i.encrypt()
            elif args[2] == "-j":
                i.plaintext_cryptoanalysis()
            elif args[2] == "-k":
                i.encrypted_cryptoanalysis()


if __name__ == "__main__":
    main()

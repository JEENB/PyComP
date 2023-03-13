from core.data import *


class SymmetricNumeral(Data):
    def __init__(self, symbols: list, probability: list = None) -> None:
        self.symbols = symbols
        self.prob = probability

    def encode_symbols(self) -> int:
        x = 0
        for i in self.symbols:
            x = 10 * x + i
        return x  # in binary takes ceil(log(x))

    def decode_symbols(self, x):
        decoded_list = []
        while x != int(x) % 10:
            decoded_list.append(int(x) % 10)
            x = x // 10
        decoded_list.append(x)
        return decoded_list


s = SymmetricNumeral([1, 0, 0, 0, 1, 1])
encoded_value = s.encode_symbols()
decoded_value = s.decode_symbols(encoded_value)
print(encoded_value)
print(decoded_value)

from core.data import *
from ANS import *
from utils.bit_array_utils import int_to_bitarray, bitarray_to_int
import bitarray
import math


class sANS(Data):

    def __init__(self, symbols: list, frequency: list) -> None:
        super().__init__(symbols, frequency)
        self.rans = rANS(self.symbols, self.frequency)
        self.__get_interval()
        self.b = bitarray.bitarray()

    def __get_interval(self):
        self.all_interval = {}
        for s in self.symbols:
            self.all_interval[s] = range(
                self.freq_dist[s], 2 * self.freq_dist[s])

    def streaming_rANS_encoding(self, initial_state: int, data: list):
        assert initial_state >= self.M
        x = initial_state

        for s in data:
            s_interval = self.all_interval[s]
            while x not in s_interval:
                self.b.append(x % 2)
                x = x//2
            x = self.rans.rANS_encode_step(s, x)
        return x, self.b

    def streaming_rANS_decoding(self, x: int, bit_array: bitarray.bitarray):
        decoded_symbols = []
        while len(bit_array) != 0:
            s, x = self.rans.rANS_decode_step(x)
            decoded_symbols.append(s)
            while x not in range(self.M, 2*self.M):
                x = 2 * x + int(bit_array[-1])
                bit_array = bit_array[:-1]
        return list(reversed(decoded_symbols))


class sANSDecoder(Data):

    def __init__(self, symbols: list, frequency: list) -> None:
        super().__init__(symbols, frequency)
        self.sans = sANS(self.symbols, self.frequency)

    def decode(self, x: int, bit_array: bitarray.bitarray):
        decoded_symbols = self.sans.streaming_rANS_decoding(x, bit_array)
        return decoded_symbols

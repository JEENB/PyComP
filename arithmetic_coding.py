import os
import math
import tabulate
from utils.ac_utils import *
from core.data import *
from utils.bit_array_utils import float_to_bitarrays, bitarrays_to_float
import bitarray


class ArithmeticCoding(Data):

    def __init__(self, symbols: list, frequency: list, message=None, show_steps: bool = None) -> None:
        super().__init__(symbols, frequency)
        self.message = message
        if self.message != None:
            self.__prob_dist()
            self.__cumul_distribution()
        self.show_steps = True

    def __prob_dist(self):
        self.symbols = []
        self.prob_dist = {}
        self.num_elements = 0
        for i in self.message:
            self.symbols.append(i)
            try:
                self.prob_dist[i] += 1
            except:
                self.prob_dist[i] = 1
            self.num_elements += 1

        for key in self.prob_dist.keys():
            self.prob_dist[key] = self.prob_dist[key]/self.num_elements

    def __cumul_distribution(self):
        self.cum_dist = {}
        temp_freq = 0
        for symbol, freq in self.prob_dist.items():
            self.cum_dist[symbol] = [temp_freq,
                                     (temp_freq + freq)]  # storing high and low
            temp_freq += freq

    def msg_prob(self, symbols):
        '''
        P(x_1, x_2, ...) = p(x_1).p(x_2). ...
        -log2(P(x_1, x_2, ...)) + 1
        returns binary truncation value
        '''
        self.prob = 1
        for s in symbols:
            self.prob *= self.freq_dist[s]/self.M

        self.lx = abs(math.ceil(math.log2(self.prob))) + 1
        return self.prob

    def encode(self, msg: list = None):
        '''
        encodes for a subset of strings as well as the entire file. 
        '''

        if self.show_steps:
            output = []

        low_old = 0
        high_old = 1
        range = 1
        if msg == None:
            msg = self.message
        # self.__symbol_prob(symbols)  ## computes the truncation value
        sym = ''
        output_sym = ''  # output from encoding process
        for i, s in enumerate(msg):
            sym += s
            if s not in self.symbols:
                raise ValueError("Invalid symbol")

            interval = self.cum_dist[s]

            low = low_old + range * interval[0]
            high = low_old + range * interval[1]

            if self.show_steps:
                output.append([sym, (low, high), "Pick Next Symbol"])

            range = high - low

            low_old = low
            high_old = high

        # print(low_old, high_old)
        self.tag = (low_old + high_old)/2
        k = math.ceil(-math.log2(high-low)) + 1
        # tag_to_bin = decToBinConversion(self.tag, self.lx - len(output_sym))
        _, tag_to_bin = float_to_bitarrays(
            self.tag, k)  # binary conversion of 0.5

        self.encoded_value = tag_to_bin

        if self.show_steps:
            output.append(
                [' ', f"Symbols Encoded = {i+1}\nTag = {self.tag}\nCompressed Value = {self.encoded_value}"])
            print("\nEncoding Process")
            print("------------------")
            print(tabulate.tabulate(output, headers=[
                  'Symbol', 'Interval', 'Remark'], tablefmt="pretty", numalign='center'))
        else:
            print("Encoded value \n-------------\n", self.encoded_value)

        return self.encoded_value, len(msg)

    def return_symbol(self, tag):
        ''' 
        Given a tag returns the corresponding symbol
        '''
        for key, value in self.cum_dist.items():

            if tag < value[1]:
                '''
                intervals are disjoints
                '''
                return (key, value)

    def decode(self, encoded_value: bitarray.bitarray, msg_length: int, show_steps: bool = False):
        '''
        check interval, 
        update interval
        pick new 
        repeat
        '''
        if show_steps:
            output = []

        t = bitarrays_to_float(bitarray.bitarray('0'), encoded_value)
        decoded_symbols = ''
        low_old = 0
        high_old = 1
        ran = 1
        for i in range(msg_length):
            t_prime = (t - low_old)/(ran)

            symb, interval = self.return_symbol(t_prime)
            decoded_symbols += symb

            low = low_old + ran * interval[0]
            high = low_old + ran * interval[1]

            ran = high - low

            low_old = low
            high_old = high
            if show_steps:
                output.append([decoded_symbols, encoded_value,
                              t, (low, high), "Pick next\n"])
        # print(low_old, high_old)

        if show_steps:
            print("\nDecoding Process")
            print("------------------")
            print(tabulate.tabulate(output, headers=[
                  'Decoded Symb', 'Encoded Value', 'Tag', 'Range', 'Remark'], tablefmt="pretty", numalign='center'))
            print(f"Decoded Value = {decoded_symbols}\n")
        else:
            print(f"\nDecoded Value\n-------------\n{decoded_symbols}")

        return decoded_symbols


class RangeCoding(ArithmeticCoding):
    def __init__(self, symbols: list, frequency: list, message=None, show_steps: bool = None) -> None:
        super().__init__(symbols, frequency, message, show_steps)

    def __left_scale(self, x: float):
        return 2 * x

    def __right_scale(self, x: float):
        return 2 * x - 1

    def encode(self, msg: list = None):
        '''
        encodes for a subset of strings as well as the entire file. 
        '''

        if self.show_steps:
            output = []
        low_old = 0
        high_old = 1
        range = 1
        msg = self.message if msg == None else msg

        # self.__symbol_prob(symbols)  ## computes the truncation value
        sym = ''
        output_sym = bitarray.bitarray()  # rescaling output
        for i, s in enumerate(msg):
            sym += s
            if s not in self.symbols:
                raise ValueError(
                    "Value symbol not fround in prob distribuiton")

            interval = self.cum_dist[s]

            low = low_old + range * interval[0]
            high = low_old + range * interval[1]
            while (high < 0.5 and low < 0.5) or (high > 0.5 and low > 0.5):
                if low > 0.5 and high > 0.5:
                    output_sym.append(1)
                    if self.show_steps:
                        output.append(
                            [sym, (low, high), "Right Scaling \nOutput = 1"])
                    low = self.__right_scale(low)
                    high = self.__right_scale(high)

                elif high < 0.5 and low < 0.5:
                    output_sym.append(0)
                    if self.show_steps:
                        output.append(
                            [sym, (low, high), "Left Scaling \nOutput = 0"])
                    low = self.__left_scale(low)
                    high = self.__left_scale(high)

            if self.show_steps:
                output.append([sym, (low, high), "Pick Next Symbol"])

            range = high - low

            low_old = low
            high_old = high

        # print(low_old, high_old)
        # since 0.5 always lies between high and low because we rescale even after the last symbol encoding.
        self.tag = 0.5

        # tag_to_bin = decToBinConversion(self.tag, self.lx - len(output_sym))
        tag_to_bin = bitarray.bitarray(1)  # binary conversion of 0.5
        self.encoded_value = output_sym
        self.encoded_value.append(1)

        if self.show_steps:
            output.append(
                [' ', f"Symbols Encoded = {i+1}\nRescaling Output = {output_sym}\nTag = {self.tag}\nCompressed Value = {self.encoded_value}"])
            print("\nEncoding Process")
            print("------------------")
            print(tabulate.tabulate(output, headers=[
                  'Symbol', 'Interval', 'Remark'], tablefmt="pretty", numalign='center'))
        else:
            print("Encoded value \n-------------\n", self.encoded_value)

        return self.encoded_value, len(msg)

    def decode(self, encoded_value: bitarray.bitarray, msg_length: int, show_steps: bool = False):
        '''
        check interval, 
        update interval
        pick new 
        repeat
        '''
        if self.show_steps:
            output = []
        t = bitarrays_to_float(bitarray.bitarray('0'), encoded_value)
        decoded_symbols = ''
        low_old = 0
        high_old = 1
        ran = 1
        for i in range(msg_length):
            t_prime = (t - low_old)/(ran)
            symb, interval = self.return_symbol(t_prime)
            decoded_symbols += symb

            low = low_old + ran * interval[0]
            high = low_old + ran * interval[1]

            while (high < 0.5 and low <= 0.5) or (high > 0.5 and low >= 0.5):

                if low >= 0.5 and high > 0.5:

                    if self.show_steps:
                        output.append(
                            [decoded_symbols, encoded_value, t, (low, high), "Right Scaling\nRemove 1\n"])

                    encoded_value = encoded_value[1:]
                    enc_val_list = encoded_value.tolist()
                    enc = ''.join([str(elem) for elem in enc_val_list])
                    enc = '0.'+enc
                    t = getBinaryFractionValue(enc)

                    low = self.__right_scale(low)
                    high = self.__right_scale(high)

                elif high < 0.5 and low <= 0.5:
                    if self.show_steps:
                        output.append(
                            [decoded_symbols, encoded_value, t, (low, high), "Left Scaling\nRemove 0"])
                    encoded_value = encoded_value[1:]
                    enc_val_list = encoded_value.tolist()
                    enc = ''.join([str(elem) for elem in enc_val_list])

                    enc = '0.'+enc
                    t = getBinaryFractionValue(enc)

                    low = self.__left_scale(low)
                    high = self.__left_scale(high)

            ran = high - low

            low_old = low
            high_old = high
            if self.show_steps:
                output.append([decoded_symbols, encoded_value,
                              t, (low, high), "Pick next\n"])
        # print(low_old, high_old)

        if self.show_steps:
            print("\nDecoding Process")
            print("------------------")
            print(tabulate.tabulate(output, headers=[
                  'Decoded Symb', 'Encoded Value', 'Tag', 'Range', 'Remark'], tablefmt="pretty", numalign='center'))
            print(f"Decoded Value = {decoded_symbols}\n")
        else:
            print(f"\nDecoded Value\n-------------\n{decoded_symbols}")
        return decoded_symbols

# =================================================================================================


dist = {'a': 0.8, 'b': 0.02, 'c': 0.18}
symbols = ['a', 'b', 'c']
freq = [0.8, 0.02, 0.18]

f = RangeCoding(symbols, freq)
encoded_value, number = f.encode('abac')
print(encoded_value)
f.decode(encoded_value, number)
# decoded_symbols = f.decoding(encoded_value, length = number)

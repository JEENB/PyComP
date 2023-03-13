from core.data import *
import os
from utils.utils import *
from utils.file_utils import *
import tabulate

# states are not defined as python allows for infinite integer precision


class rANS(Data):
    '''
    rANS: compressor and decompressor class

    parameters:
    -------------
    symbols: list
            list of all possible symbols
    frequency: list
            list of symbol frequency
    '''

    def __init__(self, symbols: list, frequency: list) -> None:
        super().__init__(symbols, frequency)

    def __find_symbol(self, slot):
        '''
        search function for decoding
        follows: c[s]<= slot < c[s+1]
        '''
        for s in self.symbols:
            l = self.cum_dist[s][0]
            h = self.cum_dist[s][1]
            if slot >= l and slot < h:
                return s

    def rANS_encode_step(self, symbol, x_prev: int) -> int:
        block = x_prev // self.freq_dist[symbol]
        slot = self.cum_dist[symbol][0] + (x_prev % self.freq_dist[symbol])
        x = block * self.M + slot
        return x

    def rANS_encode(self, data: list, start_state: int) -> int:
        '''
        rANS encode function 

        parameters:
        -----------------
        data: list
                data to be encoded. Has to be a list

        returns:
        -----------------
        final_state: int 
                final encoded value
        '''

        output_log = []
        # TODO: output log, check
        x = start_state
        for d in data:
            x = self.rANS_encode_step(d, x)
        return x

    def rANS_decode_step(self, x_next: int) -> tuple:
        block_id = x_next // self.M
        slot = x_next % self.M
        decoded_symb = self.__find_symbol(slot)
        x_prev = block_id * \
            self.freq_dist[decoded_symb] + slot - \
            (self.cum_dist[decoded_symb][0])
        return decoded_symb, x_prev

    def rANS_decode(self, start_state: int, encoded_value: int) -> list:
        '''
        rANS decode function

        Paramters
        -----------
        encoded_value: int
                final state after encoding 
        this function inherits the probability distribuiton of the symbols.
        This function assumes that the probability distribuiton is know and the class is instantiated

        returns
        -------------
        symbols: list
                the decoded symbols in reverse order
        '''
        x_prev = encoded_value
        symbols = []
        while x_prev != start_state:
            block_id = x_prev // self.M
            slot = x_prev % self.M
            decoded_symb = self.__find_symbol(slot)
            symbols.append(decoded_symb)
            x_prev = block_id * \
                self.freq_dist[decoded_symb] + slot - \
                (self.cum_dist[decoded_symb][0])
        return symbols

    def __rANS_encoding_table_for_a_symbol(self, symbol, final_state: int):
        output__log = []
        for i in range(final_state):
            x = self.rANS_encode(data=[symbol], start_state=i)
            output__log.append([symbol, int(i), int(x)])
        return output__log

    def rANS_encoding_table(self, final_state):
        table_elements = []
        symbols = self.freq_dist.keys()
        for s in symbols:
            output = self.__rANS_encoding_table_for_a_symbol(s, final_state)
            for i in output:
                table_elements.append(i)
        table = encoding_table(table_elements)
        return table


class rANSDecoder(Data):
    '''
    rANSDecoder class for decoding given symbols and frequency

    parameters
    -----------------
    symbols: list
            a list of symbols
    frequency: list
            frequency distribuiton list
    '''

    def __init__(self, symbols: list, frequency: list) -> None:
        super().__init__(symbols, frequency)
        self.rans = rANS(self.symbols, self.frequency)

    def decode(self, encoded_value: int):
        '''
        Function to decode, give the correct order

        parameters
        ------------
        encoded_value: int
                final state after encoding
        '''
        symbols = self.rans.rANS_decode(encoded_value)
        return list(reversed(symbols))

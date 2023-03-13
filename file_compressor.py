from ANS import *


class rANSFileCompressor:
    '''
    Compresses a file

    parameter:
    ------------
    file: str
            file location

    returns: 
            final_rANS state

    Note: The decode function can be used given the class has been configured with correct prob distn. 
    '''

    def __init__(self, file):
        self.file = file
        self.__parse_file()
        self.rANS = rANS(self.symbols, self.frequency)

    def file_encode(self):
        self.encoded_value = self.rANS.rANS_encode(self.all_symbols)
        return self.encoded_value

    def __parse_file(self):
        '''
        Function to parse a file. Creates a list of all symbols and computes the frequency distribution of file. 
        : return:
        symbols and frequency as a class instance

        '''
        self.all_symbols = []
        self.symbol_freq = {}
        f = open(self.file, 'r', encoding='utf-8')
        for line in f:
            for i in line:
                self.all_symbols.append(i)
                try:
                    self.symbol_freq[i] += 1
                except:
                    self.symbol_freq[i] = 1
        self.symbols = list(self.symbol_freq.keys())
        self.frequency = list(self.symbol_freq.values())

    def summary(self):
        '''
        function that gives summary of the file
        :
        file_name
        file_size
        file_creation_tiem
        file_modification_time
        total_symbols
        unique_symbols
        frequeency_dist
        shannon_entrory
        compressed_size
        compression_ratio


        '''
        self.name, size, creation, modification = file_summary(self.file)
        entropy = self.rANS.entropy
        compression_size = len(bin(self.encoded_value))/8  # converts to bytes
        compression_ratio = f"{compression_size*100/size}%"
        size_conv = convert_bytes(size)
        compression_size_conv = convert_bytes(compression_size)
        total_symbols = len(self.all_symbols)
        unique_symbols = len(self.symbols)

        summ = [
            ['File Name', self.name],
            ["Total Symbols", total_symbols],
            ['Unique Symbols', unique_symbols],
            ['File Size', size_conv],
            ['File Created', creation],
            ['Last Modified', modification],
            ["Shannon's Entropy", entropy],
            ['Compressed File Size', compression_size_conv],
            ['Compression Ratio', compression_ratio],
        ]
        print(tabulate.tabulate(summ, tablefmt='pretty', numalign='center'))

    def decode(self, encoded_value: int):
        decoded_symbols = self.rANS.rANS_decode(encoded_value)
        output = ''
        for s in decoded_symbols:
            output += s
        return output

    def create_aux_file(self):
        '''
        creates an auxiliary file with symbols and their frequency distribution: for decompressor
        consists of:
                symbols, frequency, file_name
        using this becomes counter intuituve as the aux_file will have size > original file. 
        '''


class rANSFileDecompressor(rANSDecoder):
    '''
    rANS file decompressor class
    inherits the rANSDecoder class
    '''

    def __init__(self, symbols: list, frequency: list, encoded_value: int) -> None:
        super().__init__(symbols, frequency)
        self.encoded_val = encoded_value

    def file_decode(self):
        decoded_symbols = self.decode(self.encoded_val)
        output = ''
        for s in decoded_symbols:
            output += s
        return output

from math import ceil, floor
import tabulate
import numpy as np
from utils.utils import encoding_table


def uABS_encode_step(s: int, p: float, x_prev: int):
    if s == 0:
        x = ceil((x_prev + 1)/(1-p)) - 1
    if s == 1:
        x = floor(x_prev/p)
    return x


def uABS_encoding_table_for_a_symbol(symbol, p: float, show_steps=False):
    '''
    function for creating encoding table
    for each x_prev and symbol, 
            computes the next state
    effectively computes all possible state a symbol s can take
    '''
    output_log = []
    for i in range(15):
        x = uABS_encode_step(s=symbol, p=p, x_prev=i)
        output_log.append(np.array([symbol, i, x]))

    if show_steps:
        print(tabulate.tabulate(output_log, headers=[
              'symbol', 'x_prev', 'x_next']))

    return np.array(output_log)


def uABS_encoding_table(p: float, symbols: list = [0, 1], show_steps=False):
    '''
    table elements is a list of symbol, x_prev, x_new
    encoding_table: matrix (A) of size len(symbol) * max(x_new) where A_{symbol,x_new} = x_prev 
      x|0| 1| 2| 3| 4| 5| 6| 7| 8| 9| 10| 11 | ... -> x_prev
    ------------------------------------------------
    s=0| |  |  |  |  |  |  |  |  |  |  |  | a |    a -> x_new 
    s=1| |  |  |  |  |  |  |  |  |  |  |  |  |
    -----------------------------------------------
    ^
    |
    symbol
    '''
    table_elements = []
    for s in symbols:
        output = uABS_encoding_table_for_a_symbol(s, p)
        for i in output:
            table_elements.append(i)

    table = encoding_table(table_elements)
    return table


# print(uABS_encoding_table(0.3))

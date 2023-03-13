import random
import numpy as np
import pandas as pd

def get_symbols(symbols:list, frequency: list, no_symbols:int) -> list:
	'''
	get arbitrary number of symbols following a particular distribution as determined by the frequency
	Uses inversion sampling for sampling symbols. 
	returns
	-------
	list of symbols following a particular distribution
	'''
	sym = []
	M = sum(frequency)
	prob = [i/M for i in frequency]
	cum_freq = []
	cum = 0
	
	for p in prob:
		cum += p
		cum_freq.append(cum)
	print(cum_freq)
	for _ in range(no_symbols):
		idx = inversion_sampling(cum_freq)
		sym.append(symbols[idx])
	return sym

def inversion_sampling(cum_freq):
	'''
	given a cumulative frequency as a list, returns the index for which r < CF. 
	the index can be used to index the symbols list to get the symbol. 
	'''
	r = random.random()
	print(r)
	for i, f in enumerate(cum_freq):
		if r <= f:
			return i


def encode_symbols_to_integer(symbols:list):
	'''
	encodes each symbol to a integer starting from 0
	encode_symbols: s -> Z^+
	'''

	encoded_list = {}
	for i,s in enumerate(symbols):
		encoded_list[s] = i
	return encoded_list

def encoding_table(table_elements):
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
	table_elements = np.array(table_elements)
	symbols = set(table_elements[:,0])## 0th column is the set of symbols
	encoded_symbols = encode_symbols_to_integer(symbols)
	m = len(symbols)  ## = no.of rows
	n = max(np.array(table_elements[:,2], dtype=np.int32)) + int(1) ## max of 2nd column is the x_new = no.of columns
	A = np.full(shape=(m,n), dtype=object, fill_value='-')
	for i in table_elements:
		i_index = int(encoded_symbols[i[0]])
		j_index = int(i[2])
		A[i_index,j_index] = i[1]
	df = pd.DataFrame(A, index=encoded_symbols.keys())
	return df





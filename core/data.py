import math

class Data:

	def __init__(self, symbols:list, frequency: list) -> None:
		self.symbols = symbols
		self.frequency = frequency
	
		if len(self.frequency) != len(self.symbols):
			raise ValueError("Expected same length")

		self.__freq_distribution()
		self.__cumul_distribution()
		self.entropy()

	def __freq_distribution(self):
		'''
		Computes the frequency distribution
		function for when only symbols are given
		'''
		self.M = sum(self.frequency)
		self.freq_dist = {}
		for i, s in enumerate(self.symbols):
			self.freq_dist[s] = self.frequency[i]
			
	def __cumul_distribution(self):
		'''
		computes the cumulative distribuiton table
		dictionary with range
		{
			s_1:[low, high]
		}
		'''
		temp_freq = 0
		self.cum_dist = {}
		for i, s in enumerate(self.symbols):
			self.cum_dist[s] = [temp_freq, temp_freq + self.frequency[i]]
			temp_freq += (self.frequency[i])

	def entropy(self, show_steps = False) -> float:
		''' 
		Computes the shanon entroy as sum(p(x)log(p(x)))
		TODO: Implement show steps
		'''
		entropy = 0
		
		for p in self.frequency:
			entropy += p*math.log2(p/self.M)/self.M
		self.entropy = (-1) * entropy
		return self.entropy


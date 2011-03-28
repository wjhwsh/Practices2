from interfaces.mutant_operator import MutantOperator
import managers.eth as eth

class EthLayerOperator(MutantOperator):	
	
	group             = 'Ethernet Layer' 
	group_description = '''This mutations are applyed to the Ethernet packets before sending them to the wire'''
	isa_operator      = False  # cannot be instanciated

	def mutate(self, packets):
		return packets
		
	def insert(self):
		eth.DEFAULT_ETH_OPERATORS.append(self)
	
	def remove(self):
		eth.DEFAULT_ETH_OPERATORS.remove(self)

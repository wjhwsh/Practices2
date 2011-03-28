#**********************************************************************
#*                      Sploit Mutation Engine                        *
#**********************************************************************
#* Copyright (C) 2004-2007 Davide Balzarotti                          *
#*                                                                    *
#* This program is free software; you can redistribute it and/or      *
#* modify it under the terms of the GNU General Public License        *
#* version 2.                                                         *
#*                                                                    *
#* This program is distributed in the hope that it will be useful,    *
#* but WITHOUT ANY WARRANTY; without even the implied warranty of     *
#* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.               *
#* See the GNU General Public License for more details.               *
#*                                                                    *
#* You should have received a copy of the GNU General Public License  *
#* along with this program; if not, write to the Free Software        *
#* Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.          *
#*********************************************************************/

# Author: Andrea Beretta and Riccardo Bianchi
# $Id$

'''
TCPBadSeqNumbers
l\'operatore alterna i pacchetti della lista con pacchetti da 1 byte, aventi come numero di sequenza la somma
del campo seq del pacchetto i-esimo ed il parametro offset
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import random
import string

class TCPBadSeqNumbers(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPBadSeqNumbers','Insert TCP packets (payload 1 byte) with bad seq number ')	
		self.add_param(IntParam('seq_offset',120000,'seq number offset for bad tcp segments',1))
									
	def mutate(self, packets):
		result = []
		seq_offset = self.seq_offset
			
		if len(packets) < 2:
			return packets
			
		random.seed()
		
		for i in range(0,len(packets)):
			seq_number = packets[i].seq + seq_offset
			forged = scapy.TCP(seq=seq_number)/random.choice(string.ascii_letters)
			forged.sport = packets[i].sport
			forged.dport = packets[i].dport
			forged.flags = "A"
			forged.window = packets[i].window
			forged.urgptr = packets[i].urgptr
			result.append(packets[i])
			result.append(forged)
				
		return result


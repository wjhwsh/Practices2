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
TCPInterleavedSyn
 The operator add to the packet list a number of SYN packets with wrong sequence number
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import utils

class TCPInterleavedSyn(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPInterleavedSyn','Insert SYN packets')	
		self.add_param(IntParam('seq_offset',527600,'seq number offset for bad syn segments',1))
									
	def mutate(self, packets):
		result = []
		seq_offset = self.seq_offset
		#if real SYN or ACK do nothing
		if utils.check_syn(packets[0]) or utils.check_ack(packets[0]):
			return packets
					
		if len(packets) < 2:
			return packets	
					
		for i in range(0,len(packets)):
			forged = scapy.TCP()			
			forged.seq = packets[0].seq+i*seq_offset
			forged.sport = packets[0].sport
			forged.dport = packets[0].dport
			forged.flags = "S"
			forged.window = packets[0].window
			#forged.urgptr = packets[i].urgptr
			result.append(packets[i])
			result.append(forged)
				
		return result


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
IPWrongProto
-----------------
  It sends a new packet containing random data with a wrong protocol identification 
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPWrongProto(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPWrongProto','IP Fragmenter with wrong Protocol & payload')	
		self.add_param(IntParam('numfrag',3,'Fragment with wrong Proto & payload',1))
		self.add_param(IntParam('protocol',17,'Protocol field for forged packet',1))
		
	def mutate(self, packets):
		numfrag = self.numfrag
		protocol = self.protocol
		
		#if not enough packets, syn or ack return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets  
		
		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		
		#change proto
		forged.proto = protocol
		#insert forged 
		packets.insert (0 ,forged)
		#append original
		packets.append(packets[numfrag])
		del(packets[numfrag])
				
		return packets
		



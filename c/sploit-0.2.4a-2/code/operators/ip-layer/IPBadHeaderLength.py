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
IPHeaderLength
------------
 Copy the numfrag-1 packet, substitute  the payload with random character, and
 set the IP length field to a wrong value.
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPBadHeaderLength(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPBadHeaderLength','Bad Header Length & Payload')	
		self.add_param(IntParam('numfrag',2,'Fragment with bad header length & Payload',1))
		self.add_param(IntParam('ihl',10L,'IP header length (32 bit words)',1L))
		
	def mutate(self, packets):
		numfrag = self.numfrag
		ihl = self.ihl
				
		
		#Not enough fragments, Syn or Ack, return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets
			
		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		
		#modify total length
		forged.ihl = ihl
		
		#insert fragment first pos
		packets.insert(0,forged)
		#move original fragment last pos
		packets.append(packets[numfrag])
		del(packets[numfrag])
			
		return packets
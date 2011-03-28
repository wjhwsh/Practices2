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
IPBadOptionLength
------------
 Copy the first packet changing its payload in a random one, and setting 
 a wrong IP option 
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
from interfaces.hasparameters import StringParam
import managers.ip as ip
import utils

class IPBadOptionLength(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPBadOptionLength','IP Fragmenter with bad option length & payload')	
		self.add_param(StringParam('option','\x44\x64','2 bytes: copyflag-class-number-length'))
		self.add_param(StringParam('data','XXXXX','Ip option data'))
		#timestamp con lungh 100bytes \0x44\0x64
		#Opzione malformata dal pdf di biondi' \x02\x03
	def mutate(self, packets):
				
		#no fragments, syn or ack
		if len(packets) < 2 or utils.check_syn(packets[0].payload) or utils.check_ack(packets[0].payload):	
			return packets
					
		forged = packets[0].copy()
		forged = utils.ip_bad_payload(forged)
		
		#ip options with bad option length
		forged.options = self.option+self.data
		#insert packet first pos
		packets.insert (0,forged)
		#move original fragment last pos
		packets.append (packets[1])
		del(packets[1])
				
		return packets

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
IPBadChecksum
------------
 Copy the numfrag-1 packet, substitute its payload with random characters, and
 set its checksum to a wrong value. It then insert the new packet at the beginnning 
 of the list and the original at the end.
 If the IDS does not check the checksum it will reconstruct the traffic in the wrong way
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPBadCheksum(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPBadChecksum','IP Fragmenter with bad checksum & payload')	
		self.add_param(IntParam('numfrag',2,'Fragment with bad checksum & payload',1))		
		
	def mutate(self, packets):
		numfrag = self.numfrag
		
		#Not enough fragments, Syn or Ack, return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets

		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		#calculate and modify chksum
		forged.chksum = ip.scapy.checksum(forged)+1

		'''
		forged packet will be accepted by snort only if using -k noip option
		'''

		#insert fragment first pos
		packets.insert(0,forged)
		#move original fragment last pos
		packets.append(packets[numfrag])
		del(packets[numfrag])

		return packets


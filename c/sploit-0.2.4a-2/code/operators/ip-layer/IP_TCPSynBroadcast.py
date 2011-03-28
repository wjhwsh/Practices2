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
IP_TCPSynBroadcast
------------
 Insert in the stream fake syn packets with destination address the
 network broadcast address.
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import StringParam
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import utils


class IP_TCPSynBroadcast(IPLayerOperator):	
	isa_operator      = True  

	def __init__(self):
		IPLayerOperator.__init__(self,'IP_TCPSynBroadcast','Insert SYN packets with broadcast address')
		self.add_param(StringParam('broadcast','10.10.0.255','Broadcast address for SYN packets', isMultiValues=False))	
		self.add_param(IntParam('timer', 1,'Timeout for SYN packets',0))

									
	def mutate(self, packets):
		broadcast = self.broadcast
		timer = self.timer
		result = []
		
		#if fragmented or packets too short
		if utils.check_fragmentation(packets[0]) or len(packets)<2:
			return packets

		for i in range(0,len(packets)):
			forged = packets[i].copy()
			#del tcp payload
			forged.payload = utils.tcp_bad_payload(forged.payload, utils.NOPAYLOAD)
			#set fields
			forged.payload.seq += i*527600			
			forged.payload.flags = 'S'
			#broadcast address
			forged.dst = broadcast
			#set timer
			forged.timeout = timer
			#append packets			
			result.append(packets[i])
			result.append(forged)	

		return result		


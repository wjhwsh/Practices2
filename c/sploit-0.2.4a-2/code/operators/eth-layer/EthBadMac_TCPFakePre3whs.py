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
EthBadMac_TCPPre3whs
---------------------
 Insert at the beginning a fake 3WHS with a wrong MAC address
'''

from EthLayerOperator import EthLayerOperator
from interfaces.hasparameters import IntParam
from interfaces.hasparameters import StringParam
import scapy.scapy as scapy
import utils
import managers.tcp as tcp
import managers.ip as ip


class EthBadMac_TCPFakePre3whs(EthLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		EthLayerOperator.__init__(self,'EthBadMac_TCPFakePre3whs','Create fake reset and 3WHS with correct IP address and bad MAC ')	
		self.add_param(StringParam('BADMAC','00:10:26:C0:40:01','Mac address to be used'))
		self.add_param(IntParam('timer', 2,'Timeout after fake 3whs packets',0))
		
	def mutate(self, packets):
		BADMAC = self.BADMAC
		timer = self.timer	
		
		#if packet is fragmented
		if utils.check_fragmentation(packets[0].payload):
			return packets

		#if SYN	
		if utils.check_syn(packets[0].payload.payload):			
			#create fake SYN
			forged_syn = packets[0].copy()
			forged_syn.dst=BADMAC
			forged_syn.payload.payload.flags = 'S'
			forged_syn.payload.payload.seq = 1000
			forged_syn.payload.payload.ack = 0
			#insert fake SYN
			packets.insert(0, forged_syn)
			#create fake SYN/ACK
			forged_synack = packets[0].copy()
			forged_synack.dst=BADMAC
			forged_synack.payload.payload.sport = packets[0].payload.payload.dport
			forged_synack.payload.payload.dport = packets[0].payload.payload.sport
			forged_synack.payload.payload.flags = 'SA'
			forged_synack.payload.payload.seq = 2000
			forged_synack.payload.payload.ack = packets[0].payload.payload.seq + 1
			forged_synack.payload.dst = packets[0].payload.src
			forged_synack.payload.src = packets[0].payload.dst
			#insert fake SYN/ACK
			packets.insert(1, forged_synack)
			#create fake ACK
			forged_ack = packets[0].copy()
			forged_ack.dst=BADMAC
			forged_ack.payload.payload.flags = 'A'
			forged_ack.payload.payload.seq = packets[1].payload.payload.ack
			forged_ack.payload.payload.ack = packets[1].payload.payload.seq + 1
			#insert fake SYN/ACK
			packets.insert(2, forged_ack)
			#set timeout for real SYN
			packets[3].timeout = timer				
							
		return packets


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
TCPFakeRstBadSeq
 It sends a fake reset packet with a wrong sequence number
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import utils

class TCPFakeRstBadSeq(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPFakeRstBadSeq','TCP packet with rst flag & bad seq. number')	
		self.add_param(IntParam('numseg',1,'Position of bad rst segmnet',1))
		self.add_param(IntParam('offset',150000,'offset for seq. number', 1))
		self.add_param(IntParam('timer',2,'Timeout of segment after reset',0))
							
	def mutate(self, packets):
		numseg = self.numseg
		timer = self.timer
		offset = self.offset
		
		#Not enough segments, Syn or Ack, return
		if utils.check_length(numseg, packets) or utils.check_syn(packets[numseg-1]) or utils.check_ack(packets[numseg-1]):
			return packets
			
		forged = packets[numseg-1].copy()
		forged = utils.tcp_bad_payload(forged, utils.NOPAYLOAD)
		forged.flags = 'R'
		#seq. number
		forged.seq += offset
		packets.insert(numseg-1, forged)
		packets[numseg].timeout = timer
						
		return packets


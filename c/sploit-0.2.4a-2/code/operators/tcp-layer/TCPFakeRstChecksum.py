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
TCPFakeRstChecksum
  It sends a fake reset packet with a wrong checksum
'''

from TCPLayerOperator import TCPLayerOperator
from interfaces.hasparameters import IntParam
import scapy.scapy as scapy
import utils

class TCPFakeRstChecksum(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self, size=1):
		TCPLayerOperator.__init__(self,'TCPFakeRstChecksum','TCP packet with rst flag & bad checksum')	
		self.add_param(IntParam('numseg',1,'Position of bad rst segmnet',1))
		self.add_param(IntParam('timer',0,'Timeout of segment after reset',0))
							
	def mutate(self, packets):
		result = []
		numseg = self.numseg
		timer = self.timer
		
		#Not enough segments, Syn or Ack, return
		if utils.check_length(numseg, packets) or utils.check_syn(packets[numseg-1]) or utils.check_ack(packets[numseg-1]):
			return packets
			
		forged = packets[numseg-1].copy()
		forged = utils.tcp_bad_payload(forged, utils.NOPAYLOAD)
		forged.flags = 'R'
		#calculate and modify chksum
		forged.chksum = scapy.checksum(forged)+1
		packets.insert(numseg-1, forged)
		packets[numseg].timeout = timer
		
		return packets


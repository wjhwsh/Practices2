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
TCPSynData
 It enable the TCP manager to send data with the SYN packet
'''

from TCPLayerOperator import TCPLayerOperator
import managers.tcp as tcp
import utils

class TCPSynData(TCPLayerOperator):	
	isa_operator      = True  

	def __init__(self):
		TCPLayerOperator.__init__(self,'TCPSynData','Send data in SYN packet')	

									
	def mutate(self, packets):		
		#find tcp manager reference, otherwise return packetsS
		l4m = utils.check_l4m(packets)
		if not l4m:
			return packets
		
		#if real SYN
		if utils.check_syn(packets[0]) and (packets[0].l4manager.state == tcp.TCPS_SYN_SENT):
			l4m.delay_syn = True
			return []
		
		return packets



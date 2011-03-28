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
TCPno3whs
 It removes the three way handshake packets to the list and
 modifies the TCP manager to switch to the connected state.
 The result is that the traffic is sent without any 3ws at the beginning
'''

from TCPLayerOperator import TCPLayerOperator
import utils
import managers.tcp as tcp

class TCPNo3whs(TCPLayerOperator):	
	isa_operator      = True  

	#lasciare operatore come ultimo della lista
	def __init__(self):
		TCPLayerOperator.__init__(self,'TCPNo3whs','Send TCP packets without 3whs')	
							
	def mutate(self, packets):
		result = []
		
		#find tcp manager reference, otherwise return packetsS
		l4m = utils.check_l4m(packets)
		if not l4m:
			return packets			
		
		#SYN
		if utils.check_syn(packets[0]):
			l4m.no3whs = True
			l4m.change_state(tcp.TCPS_ESTABLISHED)
			return result
		#data
		if ( hasattr(packets[0], "load") ):
			l4m.tcpref.send_packet(packets)
			return result

		return packets


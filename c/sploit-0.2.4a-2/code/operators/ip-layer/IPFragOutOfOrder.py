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
IPFragOutOfOrder
------------
  Switch the position of two packets in the list
'''
from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPFragOutOfOrder(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPFragOutOfOrder','IP Fragmenter out of order (frag3)')	
		self.add_param(IntParam('numfrag',2,'Fragment to send out of order',1))
				
	def mutate(self, packets):
		numfrag = self.numfrag
		
		if len(packets) == 1:
			return packets
		
		#Not enough fragments, Syn or Ack, return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets
								
		frag_out = packets[numfrag-1]
		del(packets[numfrag-1])
		packets.insert(numfrag,frag_out)		
		
		return packets

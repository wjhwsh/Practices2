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
IPDuplicate
------------
 Duplicate a packet in the packet list
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPDuplicate(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPDuplicate','Duplicate an IP fragment')	
		self.add_param(IntParam('numfrag',3,'Fragment to duplicate',1))

		
	def mutate(self, packets):
		numfrag = self.numfrag
		
		#Not enough fragments, Syn or Ack, return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets
		
		packets.insert(numfrag, packets[numfrag-1])
		return packets
		

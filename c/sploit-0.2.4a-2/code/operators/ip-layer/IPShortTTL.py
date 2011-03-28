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
IPShortTTL
------------
 It insert a fake packet whit a short TTL.
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class ShortTTL(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPShortTTL','IP Fragmenter with Short TTL & bad payload')	
		self.add_param(IntParam('numfrag',3,'Fragment with short TTL & payload',1))
		self.add_param(IntParam('shortTTL', 1,'Short value for TTL field',0))
		self.add_param(IntParam('TTL', 5,'Value for TTL fields',0))
		
	def mutate(self, packets):
		numfrag = self.numfrag

		#Not enough elements,  Syn or Ack return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets
		
		#set self.TTL for each packet
		for i,f in enumerate(packets):
			packets[i].ttl=self.TTL		
		#create forged
		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		#set short TTL
		forged.ttl=self.shortTTL
		packets.insert(numfrag-1, forged)
		
		#append numfrag
		packets.append(packets[numfrag])
		del(packets[numfrag])
		
		return packets

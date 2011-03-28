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
IPWrongVersion
-----------------
  Sends a new packet with random payload and wrong IP version field
'''

from IPLayerOperator import IPLayerOperator
from interfaces.hasparameters import IntParam
import managers.ip as ip
import utils

class IPWrongVersion(IPLayerOperator):
	isa_operator      = True  
	
	def __init__(self):
		IPLayerOperator.__init__(self,'IPWrongVersion','IP Fragmenter with wrong version & payload')	
		self.add_param(IntParam('numfrag',3,'Fragment with wrong version & payload',1))
		
	def mutate(self, packets):
		numfrag = self.numfrag
		
		#if not enough packets, syn or ack return
		if utils.check_length(numfrag, packets) or utils.check_syn(packets[numfrag-1].payload) or utils.check_ack(packets[numfrag-1].payload):
			return packets 
		
		forged = packets[numfrag-1].copy()
		forged = utils.ip_bad_payload(forged)
		
		#change IP version
		forged.version = 8
		#insert forged 
		packets.insert (0 ,forged)
		#append original
		packets.append(packets[numfrag])
		del(packets[numfrag])
				
		return packets
		